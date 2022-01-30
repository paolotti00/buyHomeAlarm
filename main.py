from apscheduler.scheduler import Scheduler
import logging
from fuctions_utility import start_sched_and_keep_alive
from functions_config import get_config
from functions_email import Mail, render_email_template
from functions_repository import Repository
from functions_scrape import scrape_data, get_only_the_new_homes, create_message

emails_to_send = ["pa.tripodi@hotmail.it"]

scheduler = Scheduler()


def main():
    logging.info("start")
    searches = scrape_data()
    research_to_send: [] = []
    for research in searches:
        homes = get_only_the_new_homes(research.homes)
        if len(homes) > 0:
            research_to_send.append(research)
    if len(research_to_send) > 0:
        # create message
        message = create_message(research_to_send)
        # send email
        Mail().send(emails_to_send, get_config().email.subject,
                    render_email_template("email_jinja_template.html", zones=searches))
        # save in db
        repository = Repository()
        repository.save_many_homes(homes)
        repository.save_message(message)
    logging.info("end")


logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
config = get_config()
scheduler.add_interval_job(main, minutes=config.tech_conf.scheduler_time_minutes)
scheduler.start()
start_sched_and_keep_alive(scheduler)
