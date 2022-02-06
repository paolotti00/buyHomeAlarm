from datetime import datetime, timedelta

from apscheduler.scheduler import Scheduler
import logging

from classes import Job
from functions_config import get_config, config_app
import functions_bot_telegram as bot_telegram
from functions_email import Mail, render_email_template
from functions_repository import Repository
from functions_scheduler import configure_jobs
from functions_scrape import scrape_data, get_only_the_new_homes

emails_to_send = ["pa.tripodi@hotmail.it"]

scheduler = Scheduler()


def main(job_id):
    research_to_send: [] = []
    n_homes = 0
    job: Job = Repository.get_job(job_id)
    logging.info("start job %s", job_id)
    searches = scrape_data(job_id)
    for research in searches:
        research.homes = get_only_the_new_homes(research.homes)
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
            # todo
            logging.info("sending in chat with id s%", job.chatId)
        # save in db
        repository = Repository()
        for research in research_to_send:
            repository.save_many_homes(research.homes)
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
bot_telegram.send_text("test")
bot_telegram.send_text("ciao")
