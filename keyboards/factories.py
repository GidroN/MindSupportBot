from typing import Optional

from aiogram.filters.callback_data import CallbackData

from constants.factory import PaginationAction, PostChangeItem, DeletePostAction, PaginationMarkup


class ChooseCategoryCallback(CallbackData, prefix="choose_search_category"):
    category_id: int


class PaginationCallback(CallbackData, prefix='pag'):
    page: int
    markup: PaginationMarkup
    action: PaginationAction


class FavouriteCallback(CallbackData, prefix="fav"):
    page: int
    post_id: int


class MessageUserCallback(CallbackData, prefix="advice"):
    to_user: str
    from_user: str
    post_id: Optional[int | None] = None
    reply_to_message_id: Optional[int | None] = None


class ChangePostInfoCallback(CallbackData, prefix="change_post"):
    post_id: int
    change_item: PostChangeItem


class DeletePostCallback(CallbackData, prefix="delete_post"):
    action: DeletePostAction


