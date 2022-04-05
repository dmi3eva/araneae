import telebot
import logging


from verification.settings.config import *
from verification.utils.common import *
from verification.src.dto import *
from verification.src.storage import *

bot = telebot.TeleBot(API_TOKEN)
controller = Controller()


@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        user_id = message.chat.id
        user = get_user(controller, user_id)
        current_position = POSITIONS[user.status]
        text = current_position.generate_text(controller, user)
        panel = current_position.panel(None)
        sent_msg = bot.send_message(user_id, text, parse_mode="HTML", reply_markup=panel)
        user.last_message = sent_msg
    except RanOutError:
        bot.send_message(user.id, "Sorry, but we don't have any new samples for you!")
        logger.info(f"{user_id}: There is no requests for user.")
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        user_id = call.message.chat.id
        user = get_user(controller, user_id)
        chat_id = call.message.chat.id
        reaction = call.data
        handle(bot, controller, user, chat_id, reaction, logger)
        controller.save()
    except RanOutError:
        bot.send_message(user.id, "Sorry, but we don't have any new samples for you!")
        logger.info(f"{user_id}: There is no requests for user.")
    except:
        pass


@bot.message_handler(content_types=['text'])
def text(message):
    try:
        user_id = message.chat.id
        user = get_user(controller, user_id)
        chat_id = message.chat.id
        reaction = TEXT_TYPED
        handle(bot, controller, user, chat_id, reaction, logger)
        controller.save()
        logger.info(f"{user_id}: inputted \"{message.text}\"")
    except RanOutError:
        bot.send_message(user.id, "Sorry, but we don't have any new samples for you!")
        logger.info(f"{user_id}: There is no requests for user.")
    except:
        pass


bot.polling()
