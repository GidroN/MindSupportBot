from enum import StrEnum, unique


@unique
class CallbackConstants(StrEnum):
    DELETE_CATEGORY_MESSAGE = "delete_category_message"
    SEND_HELP_MESSAGE = "help_message"
    SUGGEST_TO_UPDATE_BOT = "suggest_bot_update"
