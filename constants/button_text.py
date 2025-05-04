from enum import StrEnum, unique


@unique
class ButtonText(StrEnum):
    MAIN_MENU = "🏠 Главное меню"
    SEARCH_POST = "🔎 Помочь"
    ADD_POST = "💓 Нужен совет"
    ALL_POSTS = "🌐 Все посты"
    PROFILE = "⚙ Профиль"
    PREV = "⬅"
    NEXT = "➡"
    GIVE_ADVICE = "📩"
    REPLY_MESSAGE = "📧"
    CANCEL = "❌ Отмена"
    CONFIRM = "✔ Принять"
    STATISTICS = "📈 Статистика"
    CHANGE_CATEGORY = "✏ Изменить категорию"
    MODERATE_POST = "🛠 Мои посты"
    DELETE_POST = "🗑"
    HOW_TO_EARN_POINTS = "❓ Как получить баллы?"
    READ_AGREEMENT = '📕 Прочесть условия использования'
    AGREE_AGREEMENT = '✅ Я согласен с условиями'
    HELP = "⁉ Помощь"
    INFO = "ℹ Информация"
    DEATH = "💀"
    SUGGEST_UPDATE = "👀 Предложить улучшение"

    @classmethod
    def get_all_buttons(cls):
        return [button.value for button in cls]
