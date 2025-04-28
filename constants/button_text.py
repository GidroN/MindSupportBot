from enum import StrEnum, unique

@unique
class ButtonText(StrEnum):
    MAIN_MENU = "🏠 Главное меню"
    SEARCH_POST = "🔎 Хочу помочь"
    ADD_POST = "💓 Получить помощь"
    ALL_POSTS = "🌐 Все посты"
    FAVOURITE = "♥ Избранное"
    ADD_TO_FAVOURITE = "🤍"
    ADDED_TO_FAVOURITE = "♥"
    PROFILE = "⚙ Профиль"
    PREV = "⬅"
    NEXT = "➡"
    GIVE_ADVICE = "📩"
    REPLY_MESSAGE = "📧"
    CANCEL = "❌ Отмена"
    CONFIRM = "✔ Принять"
    STATISTICS = "📈 Статистика"
    CHANGE_POST_NAME = "✏ Изменить название"
    CHANGE_CATEGORY = "✏ Изменить категорию"
    MODERATE_POST = "🛠 Управлять постами"
    DELETE_POST = "🗑"
    HOW_TO_EARN_POINTS = "❓ Как получить баллы?"
    READ_AGREEMENT = '📕 Прочесть условия использования'
    AGREE_AGREEMENT = '✅ Я согласен с условиями'
    HELP = "⁉ Помощь"
    INFO = "ℹ Информация"
