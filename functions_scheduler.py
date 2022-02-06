import logging
from apscheduler.scheduler import Scheduler
from datetime import datetime, timedelta
from classes import Job
from functions_repository import Repository


repository = Repository()


def configure_jobs(scheduler: Scheduler, callback) -> Scheduler:
    jobs: [Job] = repository.get_active_jobs()
    if len(jobs) > 0:
        logging.info("found %s active jobs", len(jobs))
        for job in jobs:
            scheduler.add_interval_job(callback, args=[job.id], minutes=job.n_minutes_timer,
                                       start_date=datetime.now() + timedelta(seconds=5))
        logging.info("all jobs was configured")
    else:
        logging.info("no active jobs found", len(jobs))
    return scheduler
