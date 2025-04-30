from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LinkPreviewOptions

from constants.button_text import ButtonText as BT
from constants.point_counter import Points
from database.models import Post, User
from keyboards.builders import message_user_kb
from keyboards.reply import main_menu_user_kb
from misc.states import MessageUserForm


router = Router(name="user_state_handlers_message_user_form")


@router.message(MessageUserForm.enter_message, F.text == BT.CANCEL)
async def process_message_user_form_enter_message_cancel(message: Message, state: FSMContext):
    await message.answer("Отменено.", reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(MessageUserForm.enter_message, F.text)
async def process_message_user_form_enter_message(message: Message, state: FSMContext):
    data = await state.get_data()
    to_user = data["to_user"]
    from_user = data["from_user"]
    reply_to_message_id = data.get("reply_to_message_id", None)
    text = "Тебе пришло сообщение!"

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )

    if data.get("post_id"):
        post_id = data.get("post_id")
        post = await Post.get(id=post_id)

        text = f"Тебе пришло сообщение к посту:\n<i>{post.content}</i>"

        if len(post.content) > 300:
            text = f"Тебе пришло сообщение к посту:\n<i>{post.content[:301]}...</i>"

        user = await User.get(tg_id=message.from_user.id)
        user.points += Points.HELP
        await user.save()
        await message.answer(f"Спасибо! Тебе начислено <b>{abs(Points.HELP)}</b> балла за поддержку.",
                             reply_markup=main_menu_user_kb)


    await message.bot.send_message(chat_id=to_user,
                                   text=text,
                                   link_preview_options=LinkPreviewOptions(is_disabled=True))
    await message.bot.copy_message(chat_id=to_user,
                                   from_chat_id=message.chat.id,
                                   message_id=message.message_id,
                                   reply_to_message_id=reply_to_message_id,
                                   reply_markup=message_user_kb(
                                       to_user=from_user,
                                       from_user=to_user,
                                       reply_to_message_id=message.message_id
                                   ))
    await message.answer("Сообщение отправлено!", reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(MessageUserForm.enter_message, ~F.text)
async def process_message_user_form_message_enter(message: Message):
    await message.answer("Введи текст!")

