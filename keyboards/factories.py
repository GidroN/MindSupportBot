from typing import Optional

from aiogram.filters.callback_data import CallbackData

from constants.factory import PaginationAction, PostChangeItem, DeletePostAction, PaginationMarkup, SearchPostType


class ChooseCategoryCallback(CallbackData, prefix="choose_search_category"):
    category_id: int
    search_type: SearchPostType


class PaginationCallback(CallbackData, prefix='pag'):
    page: int
    markup: PaginationMarkup
    action: PaginationAction


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


