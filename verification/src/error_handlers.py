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


def save_fluency_substitution_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    if sample and sample.ok_fluency_source is None:
        sample.ok_fluency_source = True
    sample.ok_fluency_substitution = False
    sample.paraphrased_nl = correction


def save_equivalent_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    if sample and sample.ok_fluency_substitution is None:
        sample.ok_fluency_substitution = True
    sample.ok_equivalent = False
    sample.paraphrased_nl = correction


def save_sql_error(user: User, sample: BotSample, correction: str) -> NoReturn:
    if sample and sample.ok_equivalent is None:
        sample.ok_equivalent = True
    sample.ok_sql = False
    sample.paraphrased_nl = correction


def save_fluency_source_correct(user: User, sample: BotSample, correction: str) -> NoReturn:
    if sample and sample.ok_fluency_source is None:
        sample.ok_fluency_source = True


def save_fluency_substitution_correct(user: User, sample: BotSample, correction: str) -> NoReturn:
    if sample and sample.ok_fluency_substitution is None:
        sample.ok_fluency_substitution = True


def save_equivalent_correct(user: User, sample: BotSample, correction: str) -> NoReturn:
    if sample and sample.ok_equivalent is None:
        sample.ok_equivalent = True


def save_sql_correct(user: User, sample: BotSample, correction: str) -> NoReturn:
    if sample and sample.ok_sql is None:
        sample.ok_sql = True