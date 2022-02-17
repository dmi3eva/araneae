def get_user(controller, user_id):
    if user_id not in controller.users.keys():
        controller.add_new_user(user_id)
    user = controller.users[user_id]
    if not user:
        raise ValueError("Some problem with user")
    return user