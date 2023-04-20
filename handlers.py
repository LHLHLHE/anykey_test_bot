import os

import requests as requests
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv

from constants import MENU_TEXT, MENU_BUTTONS, WEATHER_RETRY_BUTTON_TEXT
from keyboards import get_menu_keyboard, get_retry_weather_keyboard

router = Router()

load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')


class ChooseCity(StatesGroup):
    city = State()


async def get_menu(message):
    await message.answer(
        MENU_TEXT.format(message.from_user.first_name),
        reply_markup=get_menu_keyboard().as_markup(resize_keyboard=True)
    )


@router.message(Command('start'))
async def cmd_start(message: Message):
    await get_menu(message)


@router.message(Text(MENU_BUTTONS.get('get_weather')))
@router.message(Text(WEATHER_RETRY_BUTTON_TEXT))
async def set_city(message: Message, state: FSMContext):
    await message.answer('Введите город')
    await state.set_state(ChooseCity.city)


@router.message(ChooseCity.city)
async def get_weather(message: Message, state: FSMContext):
    city_name = message.text.strip().lower()
    res = requests.get(
        'https://api.openweathermap.org/data/2.5/'
        'weather?q={}&lang=ru&units=metric&appid={}'.format(
            city_name, OPEN_WEATHER_API_KEY
        )
    )
    if res.status_code == 404:
        await message.answer(
            'Неправильно введен город',
            reply_markup=get_retry_weather_keyboard().as_markup(
                resize_keyboard=True
            )
        )
    else:
        data = res.json()
        await message.answer(
            f'Погода в городе {city_name.title()} сейчас:\n'
            f'{data["weather"][0]["description"].capitalize()}\n'
            f'Температура: {data["main"]["temp"]}\u2103\n'
            f'Ощущается как {data["main"]["feels_like"]}\u2103',
            reply_markup=get_menu_keyboard().as_markup(resize_keyboard=True)
        )
    await state.clear()
