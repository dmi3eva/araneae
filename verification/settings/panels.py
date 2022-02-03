from telebot import types

# Request menu
correct_btn = types.InlineKeyboardButton(text='\U0001F44D Все верно!', callback_data='correct')
incorrect_btn = types.InlineKeyboardButton(text='\U0001F41E Есть ошибки...', callback_data='incorrect')
skip_btn = types.InlineKeyboardButton(text='\U0001F945 Пропустить', callback_data='skip')
db_btn = types.InlineKeyboardButton(text='\U0001F50D Посмотреть БД', callback_data='db')
info_btn = types.InlineKeyboardButton(text='\U0001F4D6 Инструкции', callback_data='info')

request_panel = types.InlineKeyboardMarkup(row_width=2)
request_panel.add(correct_btn, incorrect_btn)
request_panel.add(skip_btn, db_btn)
request_panel.add(info_btn)

# Info menu
estimate_btn = types.InlineKeyboardButton(text='Перейти к оцениванию', callback_data='estimate')
info_panel = types.InlineKeyboardMarkup(row_width=1)
info_panel.add(estimate_btn)

# Error menu
error_btn = types.InlineKeyboardButton(text='Следующий запрос', callback_data='estimate')
error_panel = types.InlineKeyboardMarkup(row_width=2)
error_panel.add(estimate_btn, info_btn)

# Other
back_btn = types.InlineKeyboardButton(text='\U0001F44D Назад', callback_data=f'back_to_estimation')