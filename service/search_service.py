import logging
import time

from telegram.error import RetryAfter

from model.classes import Job, Chat, ActionSearchHome, Search
from service.config_service import get_config
from service.email_service import Mail, render_email_template
from service.repository_service import Repository
from service.scrape_service import scrape_data, get_only_the_new_homes
from service import bot_telegram_service as bot_telegram

emails_to_send = ["pa.tripodi@hotmail.it", "denisediprima@virgilio.it"]  # todo delete it


def do_searches(job_id_mongo, action: ActionSearchHome):
    repository = Repository()
    research_to_send: [] = []
    n_homes = 0
    job: Job = repository.get_job(job_id_mongo)
    logging.info("start job %s", job_id_mongo)
    searches: [Search] = repository.get_searches(action.searches_ids)
    searches = scrape_data(searches)
    for research in searches:
        research.homes = get_only_the_new_homes(research.homes)
        # research.homes = order_home_by_price(research.homes) todo fix TypeError: '<' not supported between instances of 'NoneType' and 'NoneType'
        if len(research.homes) > 0:
            n_homes = n_homes + len(research.homes)
            research_to_send.append(research)
    send_results(research_to_send, n_homes, job, action)
    logging.info("end")


def send_results(research_to_send: [], n_homes: int, job: Job, action: ActionSearchHome):
    repository = Repository()
    if len(research_to_send) > 0:
        logging.info("there are %s searches with result, new mail and/or message in chat will be sent",
                     len(research_to_send))
        if action.send_email:
            logging.info("sending email")
            # send email
            Mail().send(emails_to_send, get_config().email.subject,
                        render_email_template("email_jinja_template.html", searches=research_to_send, n_homes=n_homes))
        if action.send_in_chat:
            chat: Chat = repository.get_chat(action.chat_id)
            logging.info("sending in chat with id %s", chat.telegram_id)
            bot_telegram.send_text("ho trovato {} case".format(n_homes), chat.telegram_id, False)
            for research in research_to_send:
                try:
                    bot_telegram.send_as_html(text=
                                              "<b>Ricerca:</b>  {} \n <b>Descrizione:</b> {}".format(research.title,
                                                                                                     research.description),
                                              chat_telegram_id=chat.telegram_id, disable_notification=True)
                    for home in research.homes:
                        bot_telegram.send_home(chat_telegram_id=chat.telegram_id, disable_notification=True, home=home,
                                               search=research, money_stuff=None)
                        time.sleep(1)
                except RetryAfter as r:
                    logging.error("telegram chat id: %s RetryAfter error im waiting for %s", chat.telegram_id,
                                  r.retry_after)
                    time.sleep(r.retry_after)
                    logging.info("telegram chat id: %s time is now i restarted to send message ")
                    # todo check the skipped search - retry
                    continue
            logging.info("message sent correctly in chat %s", chat.telegram_id)
            bot_telegram.send_text("fine! rincotrollerò fra {} minuti <3".format(job.n_minutes_timer), chat.telegram_id,
                                   False)
        # save in db
        for research in research_to_send:
            repository.save_many_homes(research.homes)
    else:
        if action.send_in_chat:
            chat: Chat = repository.get_chat(action.chat_id)
            logging.info("sending msg in chat with id %s", chat.telegram_id)
            bot_telegram.send_text(
                "Ciao ho controllato ma non ho trovato nessuna nuova casa - rincotrollerò fra {} minuti <3".format(
                    job.n_minutes_timer), chat.telegram_id, True)
            logging.info("no new search with new result retrieved")
