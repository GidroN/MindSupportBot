from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.button_text import ButtonText as BT
from database.models import User
from keyboards.reply import main_menu_user_kb
from misc.states import RegisterUserForm


router = Router(name="user_state_handlers_register_user_form")


@router.message(RegisterUserForm.agreement, F.text == BT.AGREE_AGREEMENT)
async def user_agree_agreement(message: Message, state: FSMContext):
    user = message.from_user
    tg_id = user.id
    full_name = user.full_name

    await User.create(tg_id=tg_id, name=full_name, username=user.username)
    await message.answer('Ты согласился на условия использования бота.', reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(RegisterUserForm.agreement, F.text != BT.AGREE_AGREEMENT and F.text != '/start')
async def invalid_user_agree_agreement(message: Message):
    await message.answer('Вы не согласился, с условиями использования!')
