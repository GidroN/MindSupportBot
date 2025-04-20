from enum import StrEnum, unique

@unique
class ButtonText(StrEnum):
    MAIN_MENU = '🏠 Главное меню'
    SEARCH_POST = "🔎 Хочу помочь"
    ADD_POST = "💓 Получить помощь"
    FAVOURITE = '♥ Избранное'
    ADD_TO_FAVOURITE = '🤍'
    ADDED_TO_FAVOURITE = '♥'
    PROFILE = '⚙ Профиль'
    PREV = '⬅'
    NEXT = '➡'
    GIVE_ADVICE = "📩"
    REPLY_MESSAGE = "📧"
    CANCEL = "❌ Отмена"
    CONFIRM = '✔ Принять'
    STATISTICS = "📈 Статистика"
    CHANGE_POST_NAME = "✏ Изменить название"
    CHANGE_CATEGORY = "✏ Изменить категорию"
    MODERATE_POST = "🛠 Управлять постами"
    DELETE_POST = "🗑 Удалить"
    HOW_TO_EARN_POINTS = "❓ Как получить баллы?"

