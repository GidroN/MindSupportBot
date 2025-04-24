from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LinkPreviewOptions

from constants.button_text import ButtonText as BT
from constants.point_counter import Points
from database.models import User, Post, Category
from integrations.chatgpt_openai import moderate_text_openai
from keyboards.builders import message_user_kb
from keyboards.reply import main_menu_user_kb, cancel_button_kb, remove_kb, profile_button_kb
from misc.states import AddPostForm, MessageUserForm, EditPostForm

router = Router(name="user_state_processes")

@router.message(AddPostForm.enter_text, F.text == BT.CANCEL)
async def process_add_post_form_enter_text_cancel(message: Message, state: FSMContext):
    await message.answer("Отменено.", reply_markup=main_menu_user_kb)
    await state.set_state()

@router.message(AddPostForm.enter_text, F.text)
async def process_add_post_form_enter_text(message: Message, state: FSMContext):
    tg_id = message.chat.id
    user = await User.get(tg_id=tg_id)
    data = await state.get_data()

    category_id = data["category_id"]
    category = await Category.get(id=category_id)

    if await Post.filter(content=message.text).exists():
        await message.answer("Данный пост уже добавлен!", reply_markup=cancel_button_kb)
        return

    # is_flagged = moderate_text_openai(message.text)
    # if is_flagged:
    #     await message.answer("Пожалуйста уберите из текста нецензурную брань и попробуйте еще раз.")
    #     return

    text = message.text
    await Post.create(content=text, user=user, category=category)
    await message.answer("Пост успешно добавлен. Если ваш пост не вмещается в одно сообщение,"
                         " то можете использовать telgra.ph и просто прислать сюда ссылку на статью.", reply_markup=main_menu_user_kb)

    user = await User.get(tg_id=message.from_user.id)
    user.points += Points.HELP
    await user.save()

    await state.set_state()


@router.message(AddPostForm.enter_text, ~F.text)
async def process_add_post_form_text_invalid(message: Message, state: FSMContext):
    await message.answer("Введите текст!")


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
    text = "Вам пришло сообщение!"

    if data.get("post_id"):
        post_id = data.get("post_id")
        post = await Post.get(id=post_id)

        text = f"Вам пришло сообщение к посту:\n<i>{post.content}</i>"

        if len(post.content) > 300:
            text = f"Вам пришло сообщение к посту:\n<i>{post.content[:301]}...</i>"

        user = await User.get(tg_id=message.from_user.id)
        user.points += Points.HELP
        await user.save()
        await message.answer(f"Спасибо! Вам начислено <b>{abs(Points.HELP)}</b> балла за поддержку.",
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
    await message.answer("Введите текст!")
