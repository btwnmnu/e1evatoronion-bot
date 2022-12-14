from telegram import InlineKeyboardButton
from settings import TG_URL
from answers import CHECK_CHANNEL_KEYBOARD, SEND_MORE_KEYBOARD, SEND_FEEDBACK_KEYBOARD

isTodayKeyboard = [
        [
            InlineKeyboardButton("Да", callback_data="today"),
            InlineKeyboardButton("Нет", callback_data="notToday"),
        ]
    ]

isCityCorrectKeyboard = [
            [
                InlineKeyboardButton("Да", callback_data='cityCorrect'),
                InlineKeyboardButton("Нет", callback_data="cityWrong")
            ]
        ]

finalKeyboard = [
            [InlineKeyboardButton(CHECK_CHANNEL_KEYBOARD, url=TG_URL)],
            [InlineKeyboardButton(SEND_MORE_KEYBOARD, callback_data="one more photo")],
            [InlineKeyboardButton(SEND_FEEDBACK_KEYBOARD, callback_data="feedback")],
        ]

finalKeyboardAfterFeedback = [
            [InlineKeyboardButton(SEND_MORE_KEYBOARD, callback_data="one more photo")],
        ]