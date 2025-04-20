from enum import StrEnum


class PaginationAction(StrEnum):
    NEXT = "next"
    PREV = "prev"


class PostChangeItem(StrEnum):
    CATEGORY = "category"
    DELETE = "delete"


class DeletePostAction(StrEnum):
    CONFIRM = "confirm"
    CANCEL = "cancel"


class PaginationMarkup(StrEnum):
    VIEWER = "viewer"
    OWNER = "owner"


class SearchPostType(StrEnum):
    ALL_POSTS = "all-posts"
    BY_CATEGORY = "by-category"
