from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_btn = [
    [
        InlineKeyboardButton(text="audio", callback_data="audio"),
    ]
]

keyboard_inline = InlineKeyboardMarkup(inline_keyboard=inline_btn)