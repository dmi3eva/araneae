from telebot import types

from verification.settings.content import *
from verification.settings.panels_inline import *
from verification.utils import *
from verification.src.controller import *

from utils.spider_connectors import *
from dto.sample import *


def save_fluency_source_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    sample.ok_fluency_source = False
    sample.source_nl = correction
    user.save(sample)