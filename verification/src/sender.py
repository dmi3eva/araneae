from telebot import types



from verification.settings.content import *
from verification.settings.panels_inline import *
from verification.utils import *
from verification.src.controller import *
from verification.src.render import *

from utils.spider_connectors import *


MAX_MESSAGE_LEN = 32000
MAX_ROWS_AMOUNT = 10


def generate_fluency_source_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    if not user.last_sample:
        user.last_sample = controller.generate_sample_for_user(user)
    sample = user.last_sample
    text = FLUENCY_SOURCE_DESCRIPTION.format(nl=sample.source_nl)
    return text, None


def generate_fluency_substitution_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = FLUENCY_SUBSTITUTION_DESCRIPTION.format(nl=sample.substituted_nl)
    return text, None


def generate_equivalent_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = EQV_DESCRIPTION.format(source=sample.substituted_nl, paraphrase=sample.paraphrased_nl)
    return text, None


def generate_sql_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = SQL_DESCRIPTION.format(nl=sample.paraphrased_nl, sql=sample.substituted_sql)
    return text, None


def generate_error_fluency_source_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = FLUENCY_SOURCE_CORRECTION.format(nl=sample.substituted_nl, sql=sample.substituted_sql)
    return text, None


def generate_error_fluency_substitution_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = FLUENCY_SUBSTITUTION_CORRECTION.format(nl=sample.paraphrased_nl, sql=sample.substituted_sql)
    return text, None


def generate_error_equivalent_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = EQUIVALENT_CORRECTION.format(nl=sample.paraphrased_nl, sql=sample.substituted_sql)
    return text, None


def generate_error_sql_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = SQL_CORRECTION.format(nl=sample.paraphrased_nl, sql=sample.substituted_sql)
    return text, None


def generate_choosing_table(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    text = TABLE_TITLE.format(db=sample.db)
    return text, None


def generate_view_table_msg(controller: Controller, user: User) -> Tuple[str, Optional[bytearray]]:
    sample = user.last_sample
    table = user.last_reaction
    table_content = en_spider.show_table(sample.db, table)

    if len(table_content) > 1 and len(table_content[1]) > MAX_ROWS_AMOUNT:
        rows = table_content[1][:MAX_ROWS_AMOUNT]
        last_row = tuple(["..." for _ in table_content[1][0]])
        rows.append(last_row)
        table_content = (table_content[0], rows)
    try:
        text = TABLE_VIEW.format(table=table, view="")
        img = render_table(sample.db, table, table_content)
    except:
        view = prettify_table(table_content)
        if len(view) > MAX_MESSAGE_LEN:
            view = TOO_LONG + view[:MAX_MESSAGE_LEN]
        text = TABLE_VIEW.format(table=table, view=view)
        img = None
    return text, img


def create_text_form_sample(sample: BotSample, text: str):  # TODO
    content = text.format(nl=sample.source_nl.capitalize(), sql=sample.source_sql)
    return content


def prettify_table(table_content):
    if len(table_content) != 2:
        return str(table_content)
    head = table_content[0]
    rows = table_content[1]
    first_row = ' | '.join(list(head))
    view = f'<b>{first_row}</b>\n'
    for _row in rows:
        view += str(_row)
        view += '\n'
    return view

