from telebot import types

from verification.settings.content import *
from verification.settings.panels_inline import *
from verification.utils import *
from verification.src.controller import *

from utils.spider_connectors import *


MAX_MESSAGE_LEN = 32000


def generate_fluency_source_msg(controller: Controller, user: User) -> str:
    if not user.last_sample:
        user.last_sample = controller.generate_sample_for_user(user.id)
    sample = user.last_sample
    text = FLUENCY_SOURCE_DESCRIPTION.format(nl=sample.source_nl)
    return text


def generate_fluency_substitution_msg(controller: Controller, user: User) -> str:
    sample = user.last_sample
    text = FLUENCY_SUBSTITUTION_DESCRIPTION.format(nl=sample.substituted_nl)
    return text


def generate_equivalent_msg(controller: Controller, user: User) -> str:
    sample = user.last_sample
    text = EQV_DESCRIPTION.format(source=sample.substituted_nl, paraphrase=sample.paraphrased_nl)
    return text


def generate_sql_msg(controller: Controller, user: User) -> str:
    sample = user.last_sample
    text = SQL_DESCRIPTION.format(nl=sample.paraphrased_nl, sql=sample.substituted_sql)
    return text


def generate_error_fluency_source_msg(controller: Controller, user: User) -> str:
    sample = user.last_sample
    text = FLUENCY_SOURCE_CORRECTION.format(nl=sample.source_nl, sql=sample.source_sql)
    return text


def send_new_sample(bot, controller, user_id):
    user = controller.users.get(user_id, None)
    if user.status is Status.READY or not user.last_sample:
        sample = controller.generate_sample_for_user(user_id)
    else:
        sample = user.last_sample
    text = create_text_form_sample(sample)
    return bot.send_message(user_id, text, parse_mode="HTML", reply_markup=request_panel)


def send_fluency_substituted_sample(bot, controller, user_id):
    user = controller.users.get(user_id, None)
    if user.status is Status.READY or not user.last_sample:
        sample = controller.generate_sample_for_user(user_id)
    else:
        sample = user.last_sample
    text = create_text_form_sample(sample)
    return bot.send_message(user_id, text, parse_mode="HTML", reply_markup=request_panel)


def send_last_sample(bot, controller, user_id):
    user = controller.users.get(user_id, None)
    sample = user.last_sample
    text = create_text_form_sample(sample)
    return bot.send_message(user_id, text, parse_mode="HTML", reply_markup=request_panel)


def just_send_ok_to_correct(bot, controller, user_id):
    bot.send_message(user_id, OK_TO_CORRECT, parse_mode="HTML")


def just_send_ok_to_incorrect(bot, controller, user_id):
    bot.send_message(user_id, OK_TO_INCORRECT, parse_mode="HTML")


def send_whats_wrong(bot, controller, user_id):
    return bot.send_message(user_id, WHATS_WRONG, parse_mode="HTML", reply_markup=error_panel)


def send_tables(bot, controller, user_id):
    user = controller.users[user_id]
    sample = user.last_sample
    en_spider = EnSpiderDB()
    tables = en_spider.get_db_tables(sample.db)
    buttons = []
    for table_title in tables:
        new_btn = types.InlineKeyboardButton(text=f'\U0001F4C3 {table_title}', callback_data=f'TABLE#{table_title}')
        buttons.append(new_btn)
    tables_panel = types.InlineKeyboardMarkup(row_width=2)
    for left_btn, right_btn in zip(buttons[::2], buttons[1::2]):
        tables_panel.add(left_btn, right_btn)
    tables_panel.add(back_to_estimation_btn)
    return bot.send_message(user_id, TABLE_TITLE, parse_mode="HTML", reply_markup=tables_panel)


def send_view(bot, controller, user_id, table):
    user = controller.users[user_id]
    sample = user.last_sample
    en_spider = EnSpiderDB()
    table_content = en_spider.show_table(sample.db, table)
    view = prettify_table(table_content)
    view_panel = types.InlineKeyboardMarkup(row_width=1)
    view_panel.add(back_to_estimation_btn)
    view_panel.add(back_to_tables_btn)
    view_panel.add(info_btn)
    if len(view) > MAX_MESSAGE_LEN:
        view = TOO_LONG + view[:MAX_MESSAGE_LEN]
    bot.send_message(user_id, f"Содержимое таблицы <b>\"{table}\"</b>:", parse_mode="HTML")
    return bot.send_message(user_id, str(view), parse_mode="HTML", reply_markup=view_panel)


def send_info(bot, controller, user_id):
    return bot.send_message(user_id, INSTRUCTIONS, parse_mode="HTML", reply_markup=info_panel)


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
