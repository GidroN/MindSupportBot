from aiogram.types import CallbackQuery, Message
from telegraph.aio import Telegraph

from database.models import User, Post
from keyboards.builders import post_kb, change_post_kb


async def send_user_post_info(posts_list: list[Post],
                              callback: CallbackQuery,
                              page: int = 0):
    message = callback.message
    post = posts_list[page]

    text = f"""Пост {page + 1}/{len(posts_list)}
<i>{post.created_at.strftime("%d.%m.%Y")}</i>
{post.category.name}

{post.content}"""

    # Пользователь не может давать советы сам себе (скрывается кнопка дать совет)
    creator = post.user
    message_sender = await User.get(tg_id=message.chat.id)
    give_advice = creator != message_sender

    await message.answer(text, reply_markup=post_kb(post_id=post.id,
                                                    to_user=post.user.tg_id,
                                                    from_user=str(callback.from_user.id),
                                                    show_give_advice=give_advice,
                                                    page=page))


async def send_user_change_post_info(posts_list: list[Post],
                                     message: Message,
                                     edit_msg: bool = False,
                                     page: int = 0):
    post = posts_list[page]

    text = f"""Пост {page + 1}/{len(posts_list)}
<i>{post.created_at.strftime("%d.%m.%Y")}</i>
{post.category.name}

{post.content}"""

    reply_markup = change_post_kb(post_id=post.id, page=page)

    if not edit_msg:
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)


async def get_telegraph_page_content(url: str) -> str:
    telegraph = Telegraph()
    response = await telegraph.get_page(url[19:])
    return response["content"]
