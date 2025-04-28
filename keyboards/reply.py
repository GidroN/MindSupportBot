from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from constants.button_text import ButtonText as BT


remove_kb = ReplyKeyboardRemove()

main_menu_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.SEARCH_POST),
            KeyboardButton(text=BT.ADD_POST)
        ],
        [
            KeyboardButton(text=BT.PROFILE)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Главное меню"
)

menu_button_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.MAIN_MENU)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Вернуться в главное меню",
)

cancel_button_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.CANCEL)
        ]
    ],
    resize_keyboard=True,
)

profile_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.STATISTICS),
            KeyboardButton(text=BT.MODERATE_POST),
        ],
        [
            KeyboardButton(text=BT.INFO),
        ],
        [
            KeyboardButton(text=BT.MAIN_MENU),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Профиль",
)

profile_button_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.PROFILE)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Вернуться в профиль"
)

user_agree_agreement_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.AGREE_AGREEMENT)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Соглашение.'
)
