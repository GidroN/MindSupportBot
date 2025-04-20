from enum import StrEnum


class PaginationAction(StrEnum):
    NEXT = "next"
    PREV = "prev"


class PostChangeItem(StrEnum):
    NAME = "name"
    CATEGORY = "category"
    DELETE = "delete"


class DeletePostAction(StrEnum):
    CONFIRM = "confirm"
    CANCEL = "cancel"


class PaginationMarkup(StrEnum):
    VIEWER = "viewer"
    OWNER = "owner"
