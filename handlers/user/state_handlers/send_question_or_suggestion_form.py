from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.button_text import ButtonText as BT
from keyboards.reply import main_menu_user_kb
from misc.states import SendQuestionOrSuggestionToDeveloper


router = Router(name="user_state_handlers_send_question_or_suggestion_form")

@router.message(SendQuestionOrSuggestionToDeveloper.enter_message, F.text == BT.CANCEL)
async def cancel_send_question(message: Message, state: FSMContext):
    await message.answer("Отменено", reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(SendQuestionOrSuggestionToDeveloper.enter_message)
async def process_send_question_or_suggestion(message: Message, state: FSMContext):
    chat_id = 511952153

    await message.bot.send_message(
        chat_id=chat_id,
        text=f"Тебе пришло сообщение от:\n"
             f"1. Полное имя: <b>{message.from_user.full_name}</b>\n"
             f"2. Username: <b>@{message.from_user.username}</b>\n"
             f"3. TG ID: <b>{message.from_user.id}</b>"
    )
    await message.bot.copy_message(
        chat_id=chat_id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await message.answer("Сообщение отправлено!", reply_markup=main_menu_user_kb)
    await state.set_state()
