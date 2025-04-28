from constants.button_text import ButtonText as BT
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from constants.callbacks import CallbackConstants
from constants.factory import DeletePostAction
from keyboards.factories import DeletePostCallback


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

user_agreement_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BT.READ_AGREEMENT,
                url="https://telegra.ph/Agreement-04-28-5"
            )
        ]
    ]
)

info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BT.READ_AGREEMENT,
                url="https://telegra.ph/Agreement-04-28-5"
            )
        ],
        [
            InlineKeyboardButton(
                text=BT.HOW_TO_EARN_POINTS,
                url="https://telegra.ph/How-to-earn-points-04-12",
            )
        ],
        [
            InlineKeyboardButton(
                text=BT.HELP,
                callback_data=CallbackConstants.SEND_HELP_MESSAGE
            )
        ]
    ]
)