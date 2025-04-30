from aiogram.fsm.state import StatesGroup, State


class SearchPostForm(StatesGroup):
    category = State()


class AddPostForm(StatesGroup):
    category = State()
    enter_text = State()


class MessageUserForm(StatesGroup):
    enter_message = State()


class EditPostForm(StatesGroup):
    category = State()


class DeletePostForm(StatesGroup):
    confirm = State()


class RegisterUserForm(StatesGroup):
    agreement = State()


class SendNewsletterMessageForm(StatesGroup):
    enter_message = State()
