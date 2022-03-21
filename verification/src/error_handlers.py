from telebot import types

from verification.settings.content import *
from verification.settings.panels_inline import *
from verification.utils import *
from verification.src.controller import *

from utils.spider_connectors import *
from dto.sample import *


def save_fluency_source_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    sample.ok_fluency_source = False
    sample.substituted_nl = correction
    user.save(sample)


def save_fluency_substitution_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    sample.ok_fluency_substitution = False
    sample.paraphrased_nl = correction
    user.save(sample)


def save_equivalent_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    sample.ok_equivalent = False
    sample.paraphrased_nl = correction
    user.save(sample)


def save_sql_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    sample.ok_sql = False
    sample.paraphrased_nl = correction
    user.save(sample)