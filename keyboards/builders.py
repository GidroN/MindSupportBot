from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants.button_text import ButtonText as BT
from constants.callbacks import CallbackConstants
from constants.factory import PaginationAction, PostChangeItem, PaginationMarkup

from database.models import Post, Category
from .factories import ChooseCategoryCallback, FavouriteCallback, PaginationCallback, MessageUserCallback, \
    ChangePostInfoCallback


async def categories(cancel: bool = False):
    all_categories = await Category.filter()
    keyboard = InlineKeyboardBuilder()

    for item in all_categories:
        category_items = await Post.filter(category=item).count()
        keyboard.add(
            InlineKeyboardButton(
                text=f"{item.name} ({category_items})",
                callback_data=ChooseCategoryCallback(category_id=item.id).pack()
            )
        )
    keyboard.adjust(2)
    if cancel:
        keyboard.row(
            InlineKeyboardButton(
                text=BT.CANCEL,
                callback_data=CallbackConstants.DELETE_CATEGORY_MESSAGE
            )
        )
    return keyboard.as_markup()


def post_kb(post_id: int,
            to_user: str,
            from_user: str,
            favourite: bool = False,
            page: int = 0):
    keyboard = InlineKeyboardBuilder()
    is_favourite = BT.ADDED_TO_FAVOURITE if favourite else BT.ADD_TO_FAVOURITE
    keyboard.add(
        InlineKeyboardButton(
            text=is_favourite,
            callback_data=FavouriteCallback(
                page=page,
                post_id=post_id,
            ).pack()
        ),
        InlineKeyboardButton(
            text=BT.PREV,
            callback_data=PaginationCallback(
                page=page,
                action=PaginationAction.PREV
            ).pack()
        ),
        InlineKeyboardButton(
            text=BT.NEXT,
            callback_data=PaginationCallback(
                page=page,
                markup=PaginationMarkup.VIEWER,
                action=PaginationAction.NEXT,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=BT.GIVE_ADVICE,
            callback_data=MessageUserCallback(
                from_user=from_user,
                to_user=to_user,
                post_id=post_id,
            ).pack()
        )
    )

    return keyboard.adjust(1).as_markup()


def message_user_kb(to_user: str,
                    from_user: str,
                    reply_to_message_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=BT.REPLY_MESSAGE,
            callback_data=MessageUserCallback(
                from_user=from_user,
                to_user=to_user,
                reply_to_message_id=reply_to_message_id,
            ).pack()
        )
    )

    return keyboard.adjust(1).as_markup()


def change_post_kb(post_id: int, page: int = 0):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text=BT.PREV,
            callback_data=PaginationCallback(
                page=page,
                markup=PaginationMarkup.OWNER,
                action=PaginationAction.PREV
            ).pack()
        ),
        InlineKeyboardButton(
            text=BT.NEXT,
            callback_data=PaginationCallback(
                page=page,
                markup=PaginationMarkup.OWNER,
                action=PaginationAction.NEXT
            ).pack()
        ),
        InlineKeyboardButton(
            text=BT.CHANGE_POST_NAME,
            callback_data=ChangePostInfoCallback(
                post_id=post_id,
                change_item=PostChangeItem.NAME
            ).pack()
        ),
        InlineKeyboardButton(
            text=BT.CHANGE_CATEGORY,
            callback_data=ChangePostInfoCallback(
                post_id=post_id,
                change_item=PostChangeItem.CATEGORY
            ).pack()
        ),
        InlineKeyboardButton(
            text=BT.DELETE_POST,
            callback_data=ChangePostInfoCallback(
                post_id=post_id,
                change_item=PostChangeItem.DELETE
            ).pack()
        )
    )

    return keyboard.adjust(2, 2, 1).as_markup()
