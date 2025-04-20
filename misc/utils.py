import requests
from aiogram.types import CallbackQuery, Message
from bs4 import BeautifulSoup

from database.models import User, Post
from keyboards.builders import post_kb, change_post_kb


def get_name_from_telegraph_article(url: str) -> str:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.find("title").text
    formatted_text = title.split('–')[0]

    return formatted_text


async def send_user_post_info(posts_list: list[Post],
                              callback: CallbackQuery,
                              page: int = 0):
    message = callback.message
    post = posts_list[page]

    text = f"""Пост {page + 1}/{len(posts_list)}
<b>{post.title}</b>
Категория: {post.category.name}
{post.url}"""

    await message.answer(text, reply_markup=post_kb(post_id=post.id,
                                                    to_user=post.user.tg_id,
                                                    from_user=str(callback.from_user.id),
                                                    page=page))


async def send_user_change_post_info(posts_list: list[Post],
                                     message: Message,
                                     edit_msg: bool = False,
                                     page: int = 0):
    post = posts_list[page]

    text = f"""Пост {page + 1}/{len(posts_list)}
<b>{post.title}</b>
Категория: {post.category.name}
{post.url}"""

    reply_markup = change_post_kb(post_id=post.id, page=page)

    if not edit_msg:
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)
