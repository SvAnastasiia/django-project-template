import dramatiq
import logging
from periodiq import cron

logger = logging.getLogger(__name__)


# every minute
@dramatiq.actor(periodic=cron("*/1 * * * *"))
def heartbeat():
    logger.info("💓 Periodic heartbeat triggered")