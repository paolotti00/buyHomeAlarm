import logging

from apscheduler.scheduler import Scheduler

from service import bot_telegram_service as bot_telegram
from service.config_service import get_config, config_app
from service.scheduler_service import configure_jobs


scheduler = Scheduler()

# start
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.info("start")
config_app()
config = get_config()
scheduler = configure_jobs(scheduler)
scheduler.start()
# start_sched_and_keep_alive(scheduler)
bot_telegram.start_bot()
