from telebot import types
from verification.settings.callbacks import *

# # Request menu
# correct_btn = types.KeyboardButton(text=CORRECT_BTN)
# incorrect_btn = types.KeyboardButton(text=INCORRECT_BTN)
# skip_btn = types.KeyboardButton(text=SKIP_BTN)
# db_btn = types.KeyboardButton(text=DB_BTN)
# info_btn = types.KeyboardButton(text=INFO_BTN)
#
#
# request_panel = types.ReplyKeyboardMarkup(True, True, row_width=2)
# request_panel.add(correct_btn, incorrect_btn)
# request_panel.add(skip_btn, db_btn)
# request_panel.add(info_btn)
#
# # Info menu
# estimate_btn = types.KeyboardButton(text=ESTIMATE_BTN)
#
# info_panel = types.ReplyKeyboardMarkup(True, True, row_width=1)
# info_panel.add(estimate_btn)
#
# # Error menu
# error_btn = types.KeyboardButton(text=NEXT_REQUEST_BTN)
#
# error_panel = types.ReplyKeyboardMarkup(True, True, row_width=2)
# error_panel.add(estimate_btn, info_btn)
#
# # Other details
# back_to_estimation_btn = types.KeyboardButton(text=BACK_TO_ESTIMATION_BTN)
# back_to_tables_btn = types.KeyboardButton(text=BACK_TO_TABLES_BTN_BTN)