from apscheduler.scheduler import Scheduler

from fuctions_utility import start_sched_and_keep_alive
from functions_config import get_config
from functions_email import Mail, render_email_template
from functions_repository import Repository
from functions_scrape import scrape_data, get_only_the_new_homes, create_message

emails_to_send = ["pa.tripodi@hotmail.it"]

scheduler = Scheduler()


def main():
    zones = scrape_data()
    zones_to_send: [] = []
    for zone in zones:
        homes = get_only_the_new_homes(zone.homes)
        if len(homes) > 0:
            zones_to_send.append(zone)
    if len(zones_to_send) > 0:
        # create message
        message = create_message(zones_to_send)
        # send email
        Mail().send(emails_to_send, get_config().email.subject,
                    render_email_template("email_jinja_template.html", zones=zones))
        # save in db
        repository = Repository()
        repository.save_many_homes(homes)
        repository.save_message(message)
    print("end")


config = get_config()
scheduler.add_interval_job(main, minutes=config.conf.scheduler_time_minutes)
scheduler.start()
start_sched_and_keep_alive(scheduler)
