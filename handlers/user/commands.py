from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ForceReply

from constants.point_counter import Points
from database.models import User, Post
from constants.button_text import ButtonText as BT
from keyboards.inline import user_how_to_earn_points_kb
from keyboards.reply import main_menu_user_kb, menu_button_kb, profile_user_kb, profile_button_kb
from keyboards.builders import categories
from misc.states import SearchPostForm, AddPostForm
from misc.utils import send_user_change_post_info

router = Router(name="user_commands")


@router.message(F.text == BT.MAIN_MENU)
@router.message(Command("menu"))
async def main_menu(message: Message, state: FSMContext):
    await message.answer("Вы перешли в главное меню", reply_markup=main_menu_user_kb)
    await state.clear()


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    tg_id = user.id
    full_name = user.full_name
    username = user.username

    user = await User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(f"Добро пожаловать, <b>{full_name}</b>!", reply_markup=main_menu_user_kb)
        await User.create(tg_id=tg_id, name=full_name, username=username)
    else:
        await message.answer(f"С возвращением <b>{full_name}</b>!", reply_markup=main_menu_user_kb)


@router.message(Command("search_posts"))
@router.message(F.text == BT.SEARCH_POST)
async def wanna_help(message: Message, state: FSMContext):
    await message.answer("Вы перешли в режим оказания помощи", reply_markup=menu_button_kb)
    await message.answer("Выберите категорию для поиска:", reply_markup=await categories())
    await state.set_state(SearchPostForm.category)


@router.message(Command("add_post"))
@router.message(F.text == BT.ADD_POST)
async def need_help(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id)

    if user.points < abs(Points.ADD_POST):
        await message.answer(f"У вас недостаточно баллов, для добавления поста.\n "
                             f"У вас <b>{user.points}</b>, а необходимо <b>{Points.ADD_POST}</b>.\n "
                             f"Для информации - /stats")
        return

    await state.set_state(AddPostForm.category)
    await message.answer("Вы перешли к выбору категории.", reply_markup=menu_button_kb)
    await message.answer("Чтобы написать сообщение, сначала выберите категорию, в которую хотите добавить:",
                         reply_markup=await categories(show_all=False))


@router.message(Command("profile"))
@router.message(F.text == BT.PROFILE)
async def profile(message: Message):
    await message.answer("Вы перешли в свой профиль", reply_markup=profile_user_kb)


@router.message(Command("stats"))
@router.message(F.text == BT.STATISTICS)
async def user_stats(message: Message):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id)
    published_posts = await Post.filter(user=user).count()
    await message.answer(f"🧑 <b>Ваша статистика</b>\n"
                         f"🎡 Баллы: <b>{user.points}</b>\n"
                         f"📚 Опубликованные посты: <b>{published_posts}</b>\n", reply_markup=user_how_to_earn_points_kb)


@router.message(Command("my_posts"))
@router.message(F.text == BT.MODERATE_POST)
async def moderate_posts(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id)
    posts = await Post.filter(user=user).prefetch_related("user", "category")
    post_list_ids = await Post.filter(user=user).values_list("id", flat=True)

    if not posts:
        await message.answer("Вы пока что не добавили ни одного поста. Чтобы добавить пост напишите /add_post")
        return

    await state.update_data(post_list_ids=post_list_ids)
    await message.answer(f"У вас {len(posts)} созданных постов", reply_markup=profile_button_kb)
    await send_user_change_post_info(posts, message)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Команды для использования бота:\n"
                         "<b>/menu</b> - Переход в главное меню\n"
                         "<b>/profile</b> - Просмотр профиля\n"
                         "<b>/my_posts</b> - Просмотр созданных постов\n"
                         "<b>/search_posts</b> - Поиск постов\n"
                         "<b>/stats</b> - Просмотр статистики\n"
                         "<b>/help - Просмотр данного сообщения.</b>")


@router.message()
async def handle_all_messages(message: Message):
    await message.reply("Извините, мне такая команда неизвестна")
