import time

from apscheduler.scheduler import Scheduler
import logging

from telegram.error import RetryAfter

from classes import Job, Chat
from fuctions_utility import start_sched_and_keep_alive
from functions_config import get_config, config_app
import functions_bot_telegram as bot_telegram
from functions_email import Mail, render_email_template
from functions_repository import Repository
from functions_scheduler import configure_jobs
from functions_scrape import scrape_data, get_only_the_new_homes_and_rich_them, order_home_by_price

emails_to_send = ["pa.tripodi@hotmail.it", "denisediprima@virgilio.it"]

scheduler = Scheduler()


def main(job_id_mongo):
    repository = Repository()
    research_to_send: [] = []
    n_homes = 0
    job: Job = repository.get_job(job_id_mongo)
    logging.info("start job %s", job_id_mongo)
    searches = scrape_data(job_id_mongo)
    user_config = repository.get_user_config_by_id(job.user_config_id)
    for research in searches:
        research.homes = get_only_the_new_homes_and_rich_them(research.homes, user_config)
        research.homes = order_home_by_price(research.homes)
        if len(research.homes) > 0:
            n_homes = n_homes + len(research.homes)
            research_to_send.append(research)
    if len(research_to_send) > 0:
        logging.info("there are %s searches with result, new mail and/or message in chat will be sent",
                     len(research_to_send))
        if job.send_email:
            logging.info("sending email")
            # send email
            Mail().send(emails_to_send, get_config().email.subject,
                        render_email_template("email_jinja_template.html", searches=research_to_send, n_homes=n_homes))
        if job.send_in_chat:
            chat: Chat = repository.get_chat(job.chat_id)
            logging.info("sending in chat with id %s", chat.telegram_id)
            bot_telegram.send_text("ho trovato {} case".format(n_homes), chat.telegram_id)
            for research in research_to_send:
                try:
                    bot_telegram.send_as_html(text=
                                              "<b>Ricerca:</b>  {} \n <b>Descrizione:</b> {}".format(research.title,
                                                                                                     research.description),
                                              chat_telegram_id=chat.telegram_id, disable_notification=True)
                    for home in research.homes:
                        bot_telegram.send_home(chat_telegram_id=chat.telegram_id, disable_notification=True, home=home,
                                               search=research)
                        time.sleep(1)
                except RetryAfter as r:
                    logging.error("telegram chat id: %s RetryAfter error im waiting for %s", chat.telegram_id,
                                  r.retry_after)
                    time.sleep(r.retry_after)
                    logging.info("telegram chat id: %s time is now i restarted to send message ")
                    # todo check the skipped search - retry
                    continue
            logging.info("message sent correctly in chat %s", chat.telegram_id)
            bot_telegram.send_text("fine! rincotrollerò fra {} minuti <3".format(job.n_minutes_timer), chat.telegram_id)
        # save in db
        # for research in research_to_send:
        #     repository.save_many_homes(research.homes)
    else:
        logging.info("no new search with new result retrieved, no new mail will be sent")
    logging.info("end")


# start
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.info("start")
config_app()
config = get_config()
scheduler = configure_jobs(scheduler, main)
scheduler.start()
# start_sched_and_keep_alive(scheduler)
bot_telegram.start_bot()
