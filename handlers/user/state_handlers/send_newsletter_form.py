from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.button_text import ButtonText as BT
from database.models import User
from keyboards.reply import main_menu_user_kb
from misc.states import SendNewsletterMessageForm


router = Router(name="user_state_handlers_send_newsletter_form")


@router.message(SendNewsletterMessageForm.enter_message)
async def process_send_news_letter_message(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer("Отменено", reply_markup=main_menu_user_kb)
        await state.set_state()
        return

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
