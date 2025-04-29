from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LinkPreviewOptions

from constants.button_text import ButtonText as BT
from constants.point_counter import Points
from database.models import User, Post, Category
from keyboards.builders import message_user_kb
from keyboards.reply import main_menu_user_kb, cancel_button_kb
from misc.states import AddPostForm, MessageUserForm, RegisterUserForm
from integrations.yagpt import moderate_text
from misc.utils import get_telegraph_page_content

router = Router(name="user_state_processes")

@router.message(RegisterUserForm.agreement, F.text == BT.AGREE_AGREEMENT)
async def user_agree_agreement(message: Message, state: FSMContext):
    user = message.from_user
    tg_id = user.id
    full_name = user.first_name

    if user.last_name:
        full_name += " " + user.last_name

    await User.create(tg_id=tg_id, name=full_name, username=user.username)
    await message.answer('Ты согласился на условия использования бота.', reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(RegisterUserForm.agreement, F.text != BT.AGREE_AGREEMENT and F.text != '/start')
async def invalid_user_agree_agreement(message: Message, state: FSMContext):
    await message.answer('Вы не согласился, с условиями использования!')


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

    text = message.text
    if message.text.startswith("https://telegra.ph/"):
        text = await get_telegraph_page_content(text)

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    try:
        is_flagged = await moderate_text(text)
        if is_flagged:
            await message.answer("Пожалуйста, убери из текста нецензурную брань и попробуй еще раз.",
                                 reply_markup=cancel_button_kb)
            return
    except Exception as e:
        await message.bot.send_message(
            chat_id=511952153,
            text=f"Траблы с подключением к YaGPT: {e}"
        )

    text = message.text
    await Post.create(content=text, user=user, category=category)
    await message.answer("Пост успешно добавлен. Если твой пост не вмещается в одно сообщение,"
                         " то можешь использовать telgra.ph и просто прислать сюда ссылку на статью.", reply_markup=main_menu_user_kb)

    user = await User.get(tg_id=message.from_user.id)
    user.points += Points.HELP
    await user.save()

    await state.set_state()


@router.message(AddPostForm.enter_text, ~F.text)
async def process_add_post_form_text_invalid(message: Message, state: FSMContext):
    await message.answer("Введи текст!")


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
    try:
        is_flagged = await moderate_text(message.text)
        if is_flagged:
            await message.answer("Пожалуйста, убери из текста нецензурную брань и попробуй еще раз.",
                                 reply_markup=cancel_button_kb)
            return
    except Exception as e:
        await message.bot.send_message(
            chat_id=511952153,
            text=f"Траблы с подключением к YaGPT: {e}"
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
