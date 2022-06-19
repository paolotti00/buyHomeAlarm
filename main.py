import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from service.config_service import get_config, config_app
from service.scheduler_service import configure_jobs
import service.telegram_bot_service as telegram_bot
import service.telegram_bot_handler_service as telegram_bot_handler

scheduler = AsyncIOScheduler(timezone="Europe/Berlin")

# start
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.info("start")
config_app()
config = get_config()
scheduler = configure_jobs(scheduler)
scheduler.start()
# create initialize and start bot
telegram_bot.create_bot()
telegram_bot_handler.initialize_handler()
telegram_bot.start_bot()
