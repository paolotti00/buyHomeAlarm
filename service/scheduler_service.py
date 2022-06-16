import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from constant.constants import ACTION_TYPE_SEARCH_HOME
from model.classes import Job
from service.repository_service import Repository
from service.search_service import do_searches


def configure_jobs(scheduler: AsyncIOScheduler) -> AsyncIOScheduler:
    repository = Repository()
    jobs: [Job] = repository.get_active_jobs()
    if len(jobs) > 0:
        callback = None
        logging.info("found %s active jobs", len(jobs))
        for job in jobs:
            # get action
            action = repository.get_action(job.action_id)
            logging.info("action type to configure = %s", action.type)
            if action.type.casefold() == ACTION_TYPE_SEARCH_HOME.casefold():
                callback = do_searches
            else:
                logging.error("error: %s action is not supported", action.type)
            if callback is not None:
                start_date = datetime.now() + timedelta(seconds=5)
                scheduler.add_job(callback, args=[job._id, action], trigger='interval',minutes=job.n_minutes_timer,
                                  start_date=start_date)
                logging.info("job id: %s with action type :%s start date: %s running every %s minutes was configured ",
                             job._id, action.type, start_date, job.n_minutes_timer)
            else:
                logging.info("no supported action found, job was configured")
        logging.info("all jobs was configured")
    else:
        logging.info("no active jobs found")
    return scheduler
