import telebot

from verification.settings.config import *
from verification.utils.common import *

bot = telebot.TeleBot(API_TOKEN)
controller = Controller()


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    user = get_user(controller, user_id)
    current_position = POSITIONS[user.status]
    text = current_position.generate_text(controller, user)
    panel = current_position.panel(None)
    sent_msg = bot.send_message(user_id, text, parse_mode="HTML", reply_markup=panel)
    user.last_message = sent_msg


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = call.message.chat.id
    user = get_user(controller, user_id)
    chat_id = call.message.chat.id
    reaction = call.data
    handle(bot, controller, user, chat_id, reaction)


@bot.message_handler(content_types=['text'])
def text(message):
    user_id = message.chat.id
    user = get_user(controller, user_id)
    chat_id = message.chat.id
    reaction = TEXT_TYPED
    handle(bot, controller, user, chat_id, reaction)


bot.polling()


# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     user_id = call.message.chat.id
#     user = get_user(controller, user_id)
#     chat_id = call.message.chat.id
#     sent_msg = None
#
#     if call.data == 'estimate':
#         sent_msg = send_new_sample(bot, controller, user_id)
#         user.status = Status.IN_PROGRESS
#     if call.data == 'correct':
#         user.status = Status.READY
#         just_send_ok_to_correct(bot, controller, user_id)
#         sent_msg = send_new_sample(bot, controller, user_id)
#     if call.data == 'incorrect':
#         user.status = Status.ERROR_DESCRIBING
#         send_whats_wrong(bot, controller, user_id)
#     if call.data == 'skip':
#         sent_msg = send_new_sample(bot, controller, user_id)
#     if call.data == 'db':
#         user.status = Status.DB_EXPLORING
#         sent_msg = send_tables(bot, controller, user_id)
#     if call.data == 'info':
#         user.status = Status.INFO_READING
#         sent_msg = send_info(bot, controller, user_id)
#     if call.data.startswith('TABLE'):
#         current_table = '#'.join(call.data.split('#')[1:])
#         sent_msg = send_view(bot, controller, user_id, current_table)
#     if call.data == 'back_to_estimation':
#         sent_msg = send_last_sample(bot, controller, user_id)
#         user.status = Status.IN_PROGRESS
#     if call.data == 'back_to_tables':
#         sent_msg = send_tables(bot, controller, user_id)
#
#     if user.last_message:
#         last_message_id = user.last_message.message_id
#         last_text = user.last_message.text
#         edited_text = f"<code>{last_text}</code>"
#         bot.edit_message_text(edited_text, chat_id=chat_id, message_id=last_message_id, reply_markup=empty_panel, parse_mode="HTML")
#         # if user.last_message.reply_markup:
#         #     bot.edit_message_reply_markup(chat_id=chat_id, message_id=last_message_id, reply_markup=empty_panel)
#
#     user.last_message = sent_msg