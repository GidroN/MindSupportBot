from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.point_counter import Points
from database.models import User, Post
from constants.button_text import ButtonText as BT
from keyboards.inline import user_agreement_kb, info_kb
from keyboards.reply import main_menu_user_kb, menu_button_kb, profile_user_kb, profile_button_kb, \
    user_agree_agreement_kb
from keyboards.builders import categories
from misc.states import SearchPostForm, AddPostForm, RegisterUserForm
from misc.utils import send_user_change_post_info

router = Router(name="user_commands")


@router.message(F.text == BT.MAIN_MENU)
@router.message(Command("menu"))
async def main_menu(message: Message, state: FSMContext):
    await message.answer("Ты перешел в главное меню", reply_markup=main_menu_user_kb)
    await state.clear()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user = message.from_user

    tg_id = user.id
    full_name = user.full_name

    user = await User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(f'<b>{full_name}, добро пожаловать в нашего бота!</b>\n'
                             f'Перед тем как начать им пользоваться тебе необходимо '
                             f'ознакомиться с условиями использования бота.',
                             reply_markup=user_agreement_kb)
        await message.answer('НАЖИМАЯ НА КНОПКУ НИЖЕ, ТЫ СОГЛАШАЕШЬСЯ С УСЛОВИЯМИ ИСПОЛЬЗОВАНИЯ БОТА.',
                             reply_markup=user_agree_agreement_kb)
        await state.set_state(RegisterUserForm.agreement)
    else:
        await message.answer(f"С возвращением <b>{full_name}</b>!", reply_markup=main_menu_user_kb)


@router.message(Command("search_posts"))
@router.message(F.text == BT.SEARCH_POST)
async def wanna_help(message: Message, state: FSMContext):
    await message.answer("Ты перешел в режим оказания помощи", reply_markup=menu_button_kb)
    await message.answer("Выбери категорию для поиска:", reply_markup=await categories())
    await state.set_state(SearchPostForm.category)


@router.message(Command("add_post"))
@router.message(F.text == BT.ADD_POST)
async def need_help(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id)

    if user.points < abs(Points.ADD_POST):
        await message.answer(f"У тебя недостаточно баллов, для добавления поста.\n "
                             f"У тебя <b>{user.points}</b>, а необходимо <b>{Points.ADD_POST}</b>.\n "
                             f"Для информации - /info")
        return

    await state.set_state(AddPostForm.category)
    await message.answer("Ты перешел к выбору категории.", reply_markup=menu_button_kb)
    await message.answer("Чтобы написать сообщение, сначала выбери категорию, в которую хочешь добавить:",
                         reply_markup=await categories(show_all=False, show_number_items=False))


@router.message(Command("profile"))
@router.message(F.text == BT.PROFILE)
async def profile(message: Message):
    await message.answer("Ты перешел в свой профиль", reply_markup=profile_user_kb)


@router.message(Command("stats"))
@router.message(F.text == BT.STATISTICS)
async def user_stats(message: Message):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id)
    published_posts = await Post.filter(user=user).count()
    await message.answer(f"🧑 <b>Твоя статистика</b>\n"
                         f"🎡 Баллы: <b>{user.points}</b>\n"
                         f"📚 Опубликованные посты: <b>{published_posts}</b>\n")


@router.message(Command("my_posts"))
@router.message(F.text == BT.MODERATE_POST)
async def moderate_posts(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id)
    posts = await Post.filter(user=user).prefetch_related("user", "category")
    post_list_ids = await Post.filter(user=user).values_list("id", flat=True)

    if not posts:
        await message.answer("Ты пока что не добавил ни одного поста. Чтобы добавить пост напиши /add_post")
        return

    await state.update_data(post_list_ids=post_list_ids)
    await message.answer(f"У тебя {len(posts)} созданных постов", reply_markup=profile_button_kb)
    await send_user_change_post_info(posts, message)


@router.message(Command("info"))
@router.message(F.text == BT.INFO)
async def info_command(message: Message):
    await message.answer(
        "Полезные ссылки:",
        reply_markup=info_kb
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды для использования бота:\n"
        "<b>/menu</b> - Переход в главное меню\n"
        "<b>/profile</b> - Просмотр профиля\n"
        "<b>/my_posts</b> - Просмотр созданных постов\n"
        "<b>/search_posts</b> - Поиск постов\n"
        "<b>/add_post</b> - Добавить пост\n"
        "<b>/stats</b> - Просмотр статистики\n"
        "<b>/info</b> - Информация о боте\n"
        "<b>/help</b> - Просмотр данного сообщения"
    )


@router.message()
async def handle_all_messages(message: Message):
    await message.reply("Извини, мне такая команда неизвестна")
