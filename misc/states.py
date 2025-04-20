from aiogram.fsm.state import StatesGroup, State


class SearchPostForm(StatesGroup):
    category = State()


class AddPostForm(StatesGroup):
    category = State()
    enter_url = State()


class MessageUserForm(StatesGroup):
    enter_message = State()


class EditPostForm(StatesGroup):
    get_user_input = State()
    category = State()


class DeletePostForm(StatesGroup):
    confirm = State()
