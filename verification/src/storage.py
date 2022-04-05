import logging
from logging import FileHandler
from verification.settings.config import *


logger = logging.getLogger('logger')
handler = FileHandler(LOG_PATH)
logger.addHandler(handler)