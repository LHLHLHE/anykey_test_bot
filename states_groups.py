from aiogram.fsm.state import StatesGroup, State


class ShowWeather(StatesGroup):
    city = State()


class Convert(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()


class CreatePoll(StatesGroup):
    question = State()
    options_number = State()
    add_options = State()
    choose_chat = State()
