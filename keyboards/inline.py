from constants.button_text import ButtonText as BT
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from constants.factory import DeletePostAction
from keyboards.factories import DeletePostCallback

user_how_to_earn_points_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BT.HOW_TO_EARN_POINTS,
                url='https://telegra.ph/How-to-earn-points-04-12'
            ),
        ]
    ]
)

confirm_post_delete_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BT.CONFIRM,
                callback_data=DeletePostCallback(
                    action=DeletePostAction.CONFIRM
                ).pack()
            ),
            InlineKeyboardButton(
                text=BT.CANCEL,
                callback_data=DeletePostCallback(
                    action=DeletePostAction.CANCEL
                ).pack()
            )
        ],
    ],
)
