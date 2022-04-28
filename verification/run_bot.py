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
        if user_id not in controller.users.keys():
            bot.send_message(SIGNAL_ID, f"New user {user_id} was added.", parse_mode="HTML")
        user = get_user(controller, user_id)
        bot.send_message(user_id, VERY_START, parse_mode="HTML")
        current_position = POSITIONS[user.status]
        text = current_position.generate_text(controller, user)
        panel = current_position.panel(None)
        sent_msg = bot.send_message(user_id, text, parse_mode="HTML", reply_markup=panel)
        user.last_message = sent_msg
    except RanOutError:
        bot.send_message(user.id, RAN_OUT)
        logger.info(f"{user_id}: There is no requests for user.")
    except KeyError:
        bot.send_message(user.id, KEY_DOESNT_EXIST)
        logger.info(f"{user_id}: There is no such key in positions.")
    except Exception as e:
        logger.exception(f"Exception: {e.__traceback__}")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        user_id = call.message.chat.id
        user = get_user(controller, user_id)
        chat_id = call.message.chat.id
        reaction = call.data
        bot.send_message(SIGNAL_ID, f"User {user_id} send {reaction}.")
        handle(bot, controller, user, chat_id, reaction)
        controller.save()
    except RanOutError:
        bot.send_message(user.id, RAN_OUT)
        bot.send_message(SIGNAL_ID, f"There is no requests for user {user_id}.")
        logger.info(f"{user_id}: There is no requests for user.")
    except KeyError:
        bot.send_message(user.id, KEY_DOESNT_EXIST)
        logger.info(f"{user_id}: There is no such key in positions.")
    except Exception as e:
        logger.exception(f"Exception: {e.__traceback__}")


@bot.message_handler(content_types=['text'])
def text(message):
    try:
        user_id = message.chat.id
        if user_id not in controller.users.keys():
            bot.send_message(SIGNAL_ID, f"New user {user_id} was added.")
        bot.send_message(SIGNAL_ID, f"User {user_id} inputted \"{message.text}\".")
        user = get_user(controller, user_id)
        chat_id = message.chat.id
        reaction = TEXT_TYPED
        handle(bot, controller, user, chat_id, reaction, typed=message.text)
        controller.save()
        logger.info(f"{user_id}: inputted \"{message.text}\"")
    except RanOutError:
        bot.send_message(user.id, RAN_OUT)
        bot.send_message(SIGNAL_ID, f"There is no requests for user {user_id}.")
        logger.info(f"{user_id}: There is no requests for user.")
    except KeyError:
        bot.send_message(user.id, KEY_DOESNT_EXIST)
        logger.info(f"{user_id}: There is no such key in positions.")
    except Exception as e:
        logger.exception(f"Exception: {e.__traceback__}")


bot.polling()
