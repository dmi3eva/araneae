from telebot import types
from verification.settings.content import *
from verification.src.controller import *
from utils.spider_connectors import *

MAX_MESSAGE_LEN = 32000
en_spider = EnSpiderDB()

# Request menu
correct_btn = types.InlineKeyboardButton(text='\U0001F44D Все верно!', callback_data=CALL_OK)
incorrect_btn = types.InlineKeyboardButton(text='\U0001F41E Есть ошибки...', callback_data=CALL_WRONG)
skip_btn = types.InlineKeyboardButton(text=f'\U0001F945 {SKIP}', callback_data=CALL_SKIP)
db_btn = types.InlineKeyboardButton(text=f'\U0001F50D {DB}', callback_data=CALL_DB)
info_btn = types.InlineKeyboardButton(text=f'\U0001F4D6 {HELP}', callback_data=CALL_INFO)

request_panel = types.InlineKeyboardMarkup(row_width=2)
request_panel.add(correct_btn, incorrect_btn)
request_panel.add(skip_btn, db_btn)
request_panel.add(info_btn)

# IN_PROGRESS_FLUENCY_SOURCE
fluency_source_correct_btn = types.InlineKeyboardButton(text=f'\U0001F44D {OK_TO_FLUENCY_SOURCE}', callback_data=CALL_OK)
fluency_source_incorrect_btn = types.InlineKeyboardButton(text=f'\U0001F41E {WRONG_TO_FLUENCY_SOURCE}', callback_data=CALL_WRONG)
fluency_source_panel = types.InlineKeyboardMarkup(row_width=2)
fluency_source_panel.add(fluency_source_correct_btn, fluency_source_incorrect_btn)
fluency_source_panel.add(skip_btn, db_btn)
fluency_source_panel.add(info_btn)

# IN_PROGRESS_FLUENCY_SUBSTITUTION
fluency_substitution_correct_btn = types.InlineKeyboardButton(text=f'\U0001F44D {OK_TO_FLUENCY_SUBSTITUTION}', callback_data=CALL_OK)
fluency_substitution_incorrect_btn = types.InlineKeyboardButton(text=f'\U0001F41E {WRONG_TO_FLUENCY_SUBSTITUTION}', callback_data=CALL_WRONG)
fluency_substitution_panel = types.InlineKeyboardMarkup(row_width=2)
fluency_substitution_panel.add(fluency_substitution_correct_btn, fluency_substitution_incorrect_btn)
fluency_substitution_panel.add(skip_btn, db_btn)
fluency_substitution_panel.add(info_btn)

# IN_PROGRESS_EQUIVALENT
equivalent_correct_btn = types.InlineKeyboardButton(text=f'\U0001F44D {OK_TO_EQV}', callback_data=CALL_OK)
equivalent_incorrect_btn = types.InlineKeyboardButton(text=f'\U0001F41E {WRONG_TO_EQV}', callback_data=CALL_WRONG)
equivalent_panel = types.InlineKeyboardMarkup(row_width=2)
equivalent_panel.add(equivalent_correct_btn, equivalent_incorrect_btn)
equivalent_panel.add(skip_btn, db_btn)
equivalent_panel.add(info_btn)

# SQL_PANEL
sql_correct_btn = types.InlineKeyboardButton(text=f'\U0001F44D {OK_TO_SQL}', callback_data=CALL_OK)
sql_incorrect_btn = types.InlineKeyboardButton(text=f'\U0001F41E {WRONG_TO_SQL}', callback_data=CALL_WRONG)
sql_panel = types.InlineKeyboardMarkup(row_width=2)
sql_panel.add(sql_correct_btn, sql_incorrect_btn)
sql_panel.add(skip_btn, db_btn)
sql_panel.add(info_btn)

# Correction fluency error
error_fluency_source_panel = types.InlineKeyboardMarkup(row_width=2)
error_fluency_source_panel.add(skip_btn, db_btn)
error_fluency_source_panel.add(info_btn)

# Correction fluency substitution error
error_fluency_substitution_panel = types.InlineKeyboardMarkup(row_width=2)
error_fluency_substitution_panel.add(skip_btn, db_btn)
error_fluency_substitution_panel.add(info_btn)

# Correction equivalent error
error_equivalent_panel = types.InlineKeyboardMarkup(row_width=2)
error_equivalent_panel.add(skip_btn, db_btn)
error_equivalent_panel.add(info_btn)

# Correction SQL error
error_sql_panel = types.InlineKeyboardMarkup(row_width=2)
error_sql_panel.add(skip_btn, db_btn)
error_sql_panel.add(info_btn)

# Info menu
estimate_btn = types.InlineKeyboardButton(text='Перейти к оцениванию', callback_data=ESTIMATE)
info_panel = types.InlineKeyboardMarkup(row_width=1)
info_panel.add(estimate_btn)

# In progress info panel
return_btn = types.InlineKeyboardButton(text='\U0001F519 Вернуться к оцениванию', callback_data=RETURN)
in_progress_info_panel = types.InlineKeyboardMarkup(row_width=1)
in_progress_info_panel.add(return_btn)

# Error menu
error_btn = types.InlineKeyboardButton(text='Следующий запрос', callback_data='estimate')
error_panel = types.InlineKeyboardMarkup(row_width=2)
error_panel.add(estimate_btn, info_btn)

# Other details
back_to_estimation_btn = types.InlineKeyboardButton(text='\U0001F519 Вернуться к оцениванию', callback_data='back_to_estimation')
back_to_tables_btn = types.InlineKeyboardButton(text='\U0001F5C2 Список таблиц', callback_data='back_to_tables')

# Empty
empty_panel = types.InlineKeyboardMarkup()


# Choosing tables
def generate_tables_panel(sample: BotSample) -> types.InlineKeyboardMarkup:
    tables = en_spider.get_db_tables(sample.db)
    buttons = []
    for table_title in tables:
        new_btn = types.InlineKeyboardButton(text=f'\U0001F4C3 {table_title}', callback_data=f'{TABLE}#{table_title}')
        buttons.append(new_btn)
    tables_panel = types.InlineKeyboardMarkup(row_width=2)
    for left_btn, right_btn in zip(buttons[::2], buttons[1::2]):
        tables_panel.add(left_btn, right_btn)
    tables_panel.add(return_btn)
    return tables_panel


# Choosing columns
return_to_main_btn = types.InlineKeyboardButton(text='\U0001F519 Вернуться к оцениванию', callback_data=RETURN)
return_to_tables_btn = types.InlineKeyboardButton(text=f'\U0001F5C2 Список таблиц', callback_data=RETURN_TO_TABLES)
view_panel = types.InlineKeyboardMarkup(row_width=1)
view_panel.add(return_to_tables_btn)
view_panel.add(return_to_main_btn)
