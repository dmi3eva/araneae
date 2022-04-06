import logging
from logging import FileHandler
from verification.settings.config import *

_log_format = f"%(asctime)s - %(message)s"
logger = logging.getLogger('logger')
handler = FileHandler(LOG_PATH, mode='a', encoding="utf-8")
handler.setFormatter(logging.Formatter(_log_format))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.info("Restart")