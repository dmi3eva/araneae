import logging
from logging import FileHandler
from verification.settings.config import *


logger = logging.getLogger('logger')
handler = FileHandler(LOG_PATH, mode='a', encoding="utf-8")
logger.addHandler(handler)
logger.info("Restart")