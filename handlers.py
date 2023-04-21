import requests as requests
from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import OPEN_WEATHER_API_KEY, EXCHANGERATES_API_KEY, group_chats, bot
from constants import (
    MENU_TEXT,
    HELLO_TEXT,
    MENU_BUTTONS,
    WEATHER_RETRY_BUTTON_TEXT,
    WEATHER_ENDPOINT,
    CONVERT_ENDPOINT,
    CONVERT_RETRY_BUTTON_TEXT,
    ENTER_CITY_TEXT,
    INCORRECT_CITY_TEXT,
    WEATHER_TEXT,
    ENTER_FROM_CURRENCY_CODE_TEXT,
    ENTER_TO_CURRENCY_CODE_TEXT,
    ENTER_AMOUNT_TEXT,
    INCORRECT_CONVERT_DATA_TEXT,
    ENTER_QUESTION_TEXT,
    ENTER_OPTIONS_NUMBER_TEXT,
    ENTER_OPTIONS_TEXT,
    NEXT_OPTION_TEXT,
    CHOOSE_CHAT_TEXT,
    POLL_SENT_TEXT,
    ANIMALS_ENDPOINT
)
from filters import ChatTypeFilter
from keyboards import (
    get_menu_keyboard,
    get_retry_weather_keyboard,
    get_retry_convert_keyboard,
    get_choose_chat_keyboard
)
from states_groups import ShowWeather, Convert, CreatePoll

router = Router()


@router.message(Command('start'), ChatTypeFilter('private'))
async def cmd_start_private(message: Message):
    await message.answer(
        MENU_TEXT.format(message.from_user.first_name),
        reply_markup=get_menu_keyboard().as_markup(resize_keyboard=True)
    )


@router.message(Command('start'), ChatTypeFilter(['group', 'supergroup']))
async def cmd_start_group(message: Message):
    await message.answer(HELLO_TEXT)
    group_chats[message.chat.title] = message.chat.id


@router.message(
    Text(MENU_BUTTONS.get('get_weather')),
    ChatTypeFilter('private')
)
@router.message(Text(WEATHER_RETRY_BUTTON_TEXT), ChatTypeFilter('private'))
async def set_city(message: Message, state: FSMContext):
    await message.answer(ENTER_CITY_TEXT)
    await state.set_state(ShowWeather.city)


@router.message(ShowWeather.city)
async def get_weather(message: Message, state: FSMContext):
    city_name = message.text.strip().lower()

    res = requests.get(
        WEATHER_ENDPOINT.format(city_name, OPEN_WEATHER_API_KEY)
    )

    if res.status_code == 404:
        await message.answer(
            INCORRECT_CITY_TEXT,
            reply_markup=get_retry_weather_keyboard().as_markup(
                resize_keyboard=True
            )
        )
    else:
        data = res.json()
        await message.answer(
            WEATHER_TEXT.format(
                city_name.title(),
                data['weather'][0]['description'].capitalize(),
                data['main']['temp'],
                data['main']['feels_like']
            ),
            reply_markup=get_menu_keyboard().as_markup(resize_keyboard=True)
        )

    await state.clear()


@router.message(Text(MENU_BUTTONS.get('convert')), ChatTypeFilter('private'))
@router.message(Text(CONVERT_RETRY_BUTTON_TEXT), ChatTypeFilter('private'))
async def set_currency(message: Message, state: FSMContext):
    await message.answer(ENTER_FROM_CURRENCY_CODE_TEXT)
    await state.set_state(Convert.from_currency)


@router.message(Convert.from_currency)
async def set_currency(message: Message, state: FSMContext):
    await state.update_data({'from_currency': message.text.strip().upper()})
    await message.answer(ENTER_TO_CURRENCY_CODE_TEXT)
    await state.set_state(Convert.to_currency)


@router.message(Convert.to_currency)
async def set_currency(message: Message, state: FSMContext):
    await state.update_data({'to_currency': message.text.strip().upper()})
    await message.answer(ENTER_AMOUNT_TEXT)
    await state.set_state(Convert.amount)


@router.message(Convert.amount)
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
            INCORRECT_CONVERT_DATA_TEXT,
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


@router.message(
    Text(MENU_BUTTONS.get('get_animal')),
    ChatTypeFilter('private')
)
async def get_animal(message: Message):
    await message.answer_photo(
        requests.get(ANIMALS_ENDPOINT).json()[0]['url']
    )


@router.message(
    Text(MENU_BUTTONS.get('create_poll')),
    ChatTypeFilter('private')
)
async def set_question(message: Message, state: FSMContext):
    await message.answer(ENTER_QUESTION_TEXT)
    await state.set_state(CreatePoll.question)


@router.message(CreatePoll.question)
async def set_options_number(message: Message, state: FSMContext):
    await state.update_data({'question': message.text.strip()})
    await message.answer(ENTER_OPTIONS_NUMBER_TEXT)
    await state.set_state(CreatePoll.options_number)


@router.message(CreatePoll.options_number)
async def set_first_option(message: Message, state: FSMContext):
    await state.update_data({'options_number': int(message.text.strip())})
    await message.answer(ENTER_OPTIONS_TEXT)
    await state.update_data({'options': []})
    await state.set_state(CreatePoll.add_options)


@router.message(CreatePoll.add_options)
async def set_options(message: Message, state: FSMContext):
    data = await state.get_data()
    options = data.get('options')
    options.append(message.text.strip())
    await state.update_data({'options': options})

    if len(options) < data.get('options_number'):
        await message.answer(NEXT_OPTION_TEXT)
    else:
        await message.answer(
            CHOOSE_CHAT_TEXT,
            reply_markup=get_choose_chat_keyboard().as_markup(
                resize_keyboard=True
            )
        )
        await state.set_state(CreatePoll.choose_chat)


@router.message(CreatePoll.choose_chat, F.text.in_(group_chats.keys()))
async def choose_chat_for_send(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_poll(
        chat_id=group_chats.get(message.text.strip()),
        question=data.get('question'),
        options=data.get('options')
    )
    await message.answer(
        POLL_SENT_TEXT,
        reply_markup=get_menu_keyboard().as_markup(resize_keyboard=True)
    )
    await state.clear()


