from datetime import datetime, timedelta

from apscheduler.scheduler import Scheduler
import logging
from fuctions_utility import start_sched_and_keep_alive
from functions_config import get_config, config_app
from functions_email import Mail, render_email_template
from functions_repository import Repository
from functions_scrape import scrape_data, get_only_the_new_homes, create_message

emails_to_send = ["pa.tripodi@hotmail.it", "denisediprima@virgilio.it"]

scheduler = Scheduler()


def main():
    research_to_send: [] = []
    n_homes = 0
    logging.info("start")
    searches = scrape_data()
    for research in searches:
        research.homes = get_only_the_new_homes(research.homes)
        if len(research.homes) > 0:
            n_homes = n_homes + len(research.homes)
            research_to_send.append(research)
    if len(research_to_send) > 0:
        logging.info("there are %s searches with result, new mail will be sent", len(research_to_send))
        # create message
        message = create_message(research_to_send)
        # send email
        Mail().send(emails_to_send, get_config().email.subject,
                    render_email_template("email_jinja_template.html", searches=research_to_send, n_homes=n_homes))
        # save in db
        repository = Repository()
        for research in research_to_send:
            repository.save_many_homes(research.homes)
        repository.save_message(message)
    else:
        logging.info("no new search with new result retrieved, no new mail will be sent")
    logging.info("end")


# start
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
config_app()
config = get_config()
scheduler.add_interval_job(main, minutes=config.tech_conf.scheduler_time_minutes,
                           # added 5 seconds in order to do the first run
                           start_date=datetime.now() + timedelta(seconds=5))
scheduler.start()
start_sched_and_keep_alive(scheduler)
