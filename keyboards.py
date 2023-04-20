from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from constants import (
    MENU_BUTTONS,
    WEATHER_RETRY_BUTTON_TEXT,
    CONVERT_RETRY_BUTTON_TEXT
)


def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    for text in MENU_BUTTONS.values():
        builder.add(KeyboardButton(text=text))
    return builder


def get_retry_weather_keyboard():
    return ReplyKeyboardBuilder().add(
        KeyboardButton(text=WEATHER_RETRY_BUTTON_TEXT)
    )


def get_retry_convert_keyboard():
    return ReplyKeyboardBuilder().add(
        KeyboardButton(text=CONVERT_RETRY_BUTTON_TEXT)
    )
