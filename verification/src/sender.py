from telebot import types

from verification.settings.content import *
from verification.src.controller import *
from verification.settings.panels import *
from utils.spider_connectors import *


def send_sample(bot, controller, user_id):
    user = controller.users.get(user_id, None)
    if user.status is Status.READY or not user.last:
        sample = controller.generate_sample_for_user(user_id)
    else:
        sample = user.last
    text = create_text_form_sample(sample)
    bot.send_message(user_id, text, parse_mode="HTML", reply_markup=request_panel)


def send_ok_to_correct(bot, controller, user_id):
    bot.send_message(user_id, OK_TO_CORRECT, parse_mode="HTML")


def send_ok_to_incorrect(bot, controller, user_id):
    bot.send_message(user_id, OK_TO_INCORRECT, parse_mode="HTML")


def send_whats_wrong(bot, controller, user_id):
    bot.send_message(user_id, WHATS_WRONG, parse_mode="HTML", reply_markup=error_panel)


def send_tables(bot, controller, user_id):
    user = controller.users[user_id]
    sample = user.last
    en_spider = EnSpiderDB()
    tables = en_spider.get_db_tables(sample.db)
    buttons = []
    for table_title in tables:
        new_btn = types.InlineKeyboardButton(text=f'\U0001F44D {table_title}', callback_data=f'TABLE_{table_title}')
        buttons.append(new_btn)

    bot.send_message(user_id, ERROR, parse_mode="HTML", reply_markup=error_panel)


def send_info(bot, controller, user_id):
    bot.send_message(user_id, INSTRUCTIONS, parse_mode="HTML", reply_markup=info_panel)


def create_text_form_sample(sample: Sample):  # TODO
    content = SAMPLE_DESCRIPTION.format(nl=sample.nl.capitalize(), sql=sample.sql)
    return content

