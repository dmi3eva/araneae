from verification.settings.content import *
from verification.src.controller import *
from verification.settings.panels import *


def send_sample(bot, controller, user_id):
    user = controller.users.get(user_id, None)
    if user.status is Status.READY:
        sample = user.generate_sample()
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
    bot.send_message(user_id, ERROR, parse_mode="HTML", reply_markup=error_panel)


def send_info(bot, controller, user_id):
    bot.send_message(user_id, INSTRUCTIONS, parse_mode="HTML", reply_markup=info_panel)


def create_text_form_sample(sample: Sample):  # TODO
    return "This as sample"

