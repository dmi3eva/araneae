from verification.src.sender import *
from verification.utils.common import *
from verification.settings.status_map import *


def get_user(controller, user_id):
    if user_id not in controller.users.keys():
        controller.add_new_user(user_id)
    user = controller.users[user_id]
    if not user:
        raise ValueError("Some problem with user")
    return user


def handle(bot, controller, user: User, chat_id: str, reaction: Optional[str]) -> NoReturn:
    # Разбираемся со статусом
    last_position = POSITIONS[user.status]

    user.status = last_position.transitions[reaction]
    if user.status is Status.LAST:
        user.status = user.last_status
    current_position = POSITIONS[user.status]
    sample = user.last_sample

    # Текст сообщения
    text = current_position.generate_text(controller, user)

    # Кнопки
    panel = current_position.panel

    # Обрабатываем ошибки
    sample = last_position.handle_error(user, sample, None)

    # Отправляем. Редактируем старые. Сохраняем.
    sent_msg = bot.send_message(user.id, text, parse_mode="HTML", reply_markup=panel)
    if user.last_message:
        last_message_id = user.last_message.message_id
        last_text = user.last_message.text
        edited_text = f"<code>{last_text}</code>"
        bot.edit_message_text(edited_text, chat_id=chat_id, message_id=last_message_id, reply_markup=empty_panel,
                              parse_mode="HTML")
    user.last_message = sent_msg
    if current_position.current is not Status.INFO_READING:
        user.last_status = current_position.current