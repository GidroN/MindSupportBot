from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.button_text import ButtonText as BT
from database.models import User
from keyboards.reply import main_menu_user_kb
from misc.states import SendNewsletterMessageForm


router = Router(name="user_state_handlers_send_newsletter_form")


@router.message(SendNewsletterMessageForm.enter_message, F.text == BT.CANCEL)
async def cancel_process_send(message: Message, state: FSMContext):
    await message.answer("Отменено", reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(SendNewsletterMessageForm.enter_message)
async def process_send_news_letter_message(message: Message, state: FSMContext):
    users = await User.all()

    for user in users:
        if str(message.from_user.id) == user.tg_id:
            continue

        await message.bot.copy_message(
            chat_id=user.tg_id,
            message_id=message.message_id,
            from_chat_id=message.chat.id
        )

    await message.answer("Рассылка завершена!", reply_markup=main_menu_user_kb)
    await state.set_state()
