import os

import requests as requests
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv

from constants import MENU_TEXT, MENU_BUTTONS, WEATHER_RETRY_BUTTON_TEXT, \
    WEATHER_ENDPOINT, CONVERT_ENDPOINT, CONVERT_RETRY_BUTTON_TEXT
from keyboards import get_menu_keyboard, get_retry_weather_keyboard, \
    get_retry_convert_keyboard

router = Router()

load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
EXCHANGERATES_API_KEY = os.getenv('EXCHANGERATES_API_KEY')


class ShowWeather(StatesGroup):
    city = State()


class Exchange(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()


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
    await state.set_state(ShowWeather.city)


@router.message(ShowWeather.city)
async def get_weather(message: Message, state: FSMContext):
    city_name = message.text.strip().lower()
    res = requests.get(
        WEATHER_ENDPOINT.format(city_name, OPEN_WEATHER_API_KEY)
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


@router.message(Text(MENU_BUTTONS.get('convert')))
@router.message(Text(CONVERT_RETRY_BUTTON_TEXT))
async def set_currency(message: Message, state: FSMContext):
    await message.answer('Введите код валюты, которую нужно конвертировать')
    await state.set_state(Exchange.from_currency)


@router.message(Exchange.from_currency)
async def set_currency(message: Message, state: FSMContext):
    await message.answer('Введите код валюты, в которую нужно конвертировать')
    await state.update_data({'from_currency': message.text.strip().upper()})
    await state.set_state(Exchange.to_currency)


@router.message(Exchange.to_currency)
async def set_currency(message: Message, state: FSMContext):
    await message.answer('Введите сумму')
    await state.update_data({'to_currency': message.text.strip().upper()})
    await state.set_state(Exchange.amount)


@router.message(Exchange.amount)
async def convert_currency(message: Message, state: FSMContext):
    amount = message.text.strip()
    currencies = await state.get_data()
    from_currency = currencies.get('from_currency')
    to_currency = currencies.get('to_currency')
    res = requests.get(
        CONVERT_ENDPOINT.format(
            from_currency,
            to_currency,
            amount
        ),
        headers={'apikey': EXCHANGERATES_API_KEY}
    )
    if res.status_code == 400:
        await message.answer(
            'Введены некорректные данные',
            reply_markup=get_retry_convert_keyboard().as_markup(
                resize_keyboard=True
            )
        )
    else:
        data = res.json()
        await message.answer(
            f'{amount} {from_currency} = {data["result"]} {to_currency}',
            reply_markup=get_menu_keyboard().as_markup(resize_keyboard=True)
        )
    await state.clear()
