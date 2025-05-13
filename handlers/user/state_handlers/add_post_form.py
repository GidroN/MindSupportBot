from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.button_text import ButtonText as BT
from constants.point_counter import Points
from database.models import Category, User, Post
from keyboards.reply import main_menu_user_kb, cancel_button_kb
from misc.states import AddPostForm

router = Router(name="user_state_handlers_add_post_form")


@router.message(AddPostForm.enter_text, F.text == BT.CANCEL)
async def process_add_post_form_enter_text_cancel(message: Message, state: FSMContext):
    await message.answer("Отменено.", reply_markup=main_menu_user_kb)
    await state.set_state()


@router.message(AddPostForm.enter_text, F.text.len() < 50 | F.text.startswith("/"))
async def process_add_post_form_enter_text_check_length(message: Message):
    text_length = len(message.text)
    if message.text.startswith("/"):
        await message.answer("Текст не может начинаться с <b>/</b>")
    elif text_length < 50:
        await message.answer(f"Текст не может быть короче чем 50 символов. Сейчас длина у тебя <b>{text_length}</b>")


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

    await message.bot.send_chat_action(
        action=ChatAction.TYPING,
        chat_id=message.chat.id
    )

    text = message.text

    await Post.create(content=text, user=user, category=category)
    await message.answer("Спасибо что поделился своими мыслями!\n")
    await message.answer(
        "Если есть какие-то замечания или предложения по улучшению бота, "
        "то можешь написать разработчику - /info",
        reply_markup=main_menu_user_kb
    )

    user = await User.get(tg_id=message.from_user.id)
    user.points += Points.HELP
    await user.save()

    await state.set_state()


@router.message(AddPostForm.enter_text, ~F.text)
async def process_add_post_form_text_invalid(message: Message):
    await message.answer("Введи текст!")
