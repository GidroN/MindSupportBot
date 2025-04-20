from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, LinkPreviewOptions

from constants.button_text import ButtonText as BT
from database.models import User, Post, Category
from keyboards.builders import message_user_kb
from keyboards.reply import main_menu_user_kb, cancel_button_kb, remove_kb, profile_button_kb
from misc.states import AddPostForm, MessageUserForm, EditPostForm
from misc.utils import get_name_from_telegraph_article

router = Router(name="user_state_processes")


@router.message(AddPostForm.enter_url, F.text.startswith('https://telegra.ph/'))
async def process_add_post_form_enter_url(message: Message, state: FSMContext):
    tg_id = message.chat.id
    user = await User.get(tg_id=tg_id)
    data = await state.get_data()

    category_id = data['category_id']
    category = await Category.get(id=category_id)

    if await Post.filter(url=message.text).exists():
        await message.answer('Данный пост уже добавлен!', reply_markup=cancel_button_kb)
        return

    url = message.text
    title = get_name_from_telegraph_article(url) or f"Наименование - {user.tg_id}"
    await Post.create(title=title, url=url, user=user, category=category)
    await message.answer('Пост успешно добавлен.', reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(AddPostForm.enter_url, ~F.text.startswith('https://telegra.ph/'))
async def process_add_post_form_url_invalid(message: Message, state: FSMContext):

    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=main_menu_user_kb)
        await state.set_state()
        return

    await message.answer('Ссылка должна быть на статью в https://telegra.ph/ !. Повторите попытку.')


@router.message(MessageUserForm.enter_message, F.text)
async def process_message_user_form_enter_message(message: Message, state: FSMContext):

    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=main_menu_user_kb)
        await state.set_state()
        return

    data = await state.get_data()
    to_user = data["to_user"]
    from_user = data["from_user"]
    reply_to_message_id = data.get("reply_to_message_id", None)
    text = "Вам пришло сообщение!"

    if data.get("post_id"):
        post_id = data.get("post_id")
        post = await Post.get(id=post_id)
        text = f'Вам пришло сообщение к <a href="{post.url}">посту</a>!'


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
async def process_message_user_form_message_enter(message: Message, state: FSMContext):
    await message.answer("Введите текст!")


@router.message(EditPostForm.get_user_input, F.text)
async def process_edit_post_form_get_user_input(message: Message, state: FSMContext):

    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=profile_button_kb)
        await state.set_state()
        return

    data = await state.get_data()
    post_id = data["post_id"]
    text = message.text

    post = await Post.get(id=post_id)

    post.title = text
    await post.save()

    await message.answer("Название поста успешно изменено!", reply_markup=profile_button_kb)
    await state.set_state()


@router.message(EditPostForm.get_user_input, ~F.text)
async def process_edit_post_form_get_user_input_invalid(message: Message, state: FSMContext):
    await message.answer("Введите текст!")
