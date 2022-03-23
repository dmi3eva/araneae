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
    reaction_description = reaction.split('#')
    reaction_tag = reaction_description[0]
    if len(reaction_description) > 1:
        reaction_details = reaction.split('#')[1]
        user.last_reaction = reaction_details

    user.status = last_position.transitions[reaction_tag]
    if user.status is Status.LAST:
        user.status = user.last_status
    current_position = POSITIONS[user.status]
    sample = user.last_sample

    # Текст сообщения
    text, img = current_position.generate_text(controller, user)

    # Кнопки
    panel = current_position.panel(sample)

    # Обрабатываем ошибки
    sample = last_position.handle_error(user, sample, None)

    # Отправляем. Редактируем старые. Сохраняем.
    if img:
        bot.send_photo(user.id, img)
    sent_msg = bot.send_message(user.id, text, parse_mode="HTML", reply_markup=panel)
    if user.last_message:
        last_message_id = user.last_message.message_id
        last_text = user.last_message.text
        edited_text = f"<code>{last_text}</code>"
        bot.edit_message_text(edited_text,
                              chat_id=chat_id,
                              message_id=last_message_id,
                              reply_markup=empty_panel,
                              parse_mode="HTML")
    user.last_message = sent_msg
    if RETURN not in current_position.transitions.keys():
        user.last_status = current_position.current