import telebot

from settings.configuration import *
from settings.content import *
from settings.panels import *
from src.controller import *
from src.sender import *

bot = telebot.TeleBot(API_TOKEN)
controller = Controller()


@bot.message_handler(commands=['start'])
def start_message(message):
    send_info(bot, controller, message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = call.message.chat.id
    if user_id not in controller.users.keys():
        controller.add_new_user(user_id)
    user = controller.users[user_id]
    if call.data == 'estimate':
        send_sample(bot, controller, user_id)
        user.status = Status.IN_PROGRESS
    if call.data == 'correct':
        send_ok_to_correct(bot, controller, user_id)
        send_sample(bot, controller, user_id)
    if call.data == 'incorrect':
        user.status = Status.ERROR_DESCRIBING
        send_whats_wrong(bot, controller, user_id)
    if call.data == 'skip':
        send_sample(bot, controller, user_id)
    if call.data == 'db':
        send_tables(bot, controller, user_id)
    if call.data == 'info':
        send_info(bot, controller, user_id)


@bot.message_handler(content_types=['text'])
def text(message):
    user = controller.users.get(message.chat.id, None)
    if not user:
        pass # TODO
    if user.status is Status.ERROR_DESCRIBING:
        send_ok_to_incorrect(bot, controller, user.id)
        send_sample(bot, controller, message.chat.id)
bot.polling()
