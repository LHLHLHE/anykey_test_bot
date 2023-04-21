MENU_TEXT = 'Привет, {}!\nЧто я могу для тебя сделать?'
HELLO_TEXT = 'Привет, чат!\nЯ AnyKey Bot!'
ENTER_CITY_TEXT = 'Введите город'
INCORRECT_CITY_TEXT = 'Неправильно введен город'
WEATHER_TEXT = (
    'Погода в городе {} сейчас:\n'
    '{}\n'
    'Температура: {}\u2103\n'
    'Ощущается как {}\u2103'
)
ENTER_FROM_CURRENCY_CODE_TEXT = 'Введите код валюты, которую нужно конвертировать'
ENTER_TO_CURRENCY_CODE_TEXT = 'Введите код валюты, в которую нужно конвертировать'
ENTER_AMOUNT_TEXT = 'Введите сумму'
INCORRECT_CONVERT_DATA_TEXT = 'Введены некорректные данные'
ENTER_QUESTION_TEXT = 'Введите вопрос'
ENTER_OPTIONS_NUMBER_TEXT = 'Введите количество ответов (не менее 2-х)'
ENTER_OPTIONS_TEXT = 'Введите варинаты ответа по одному'
NEXT_OPTION_TEXT = 'Следующий вариант ответа'
CHOOSE_CHAT_TEXT = 'В какой чат хотите отправить опрос?'
POLL_SENT_TEXT = 'Опрос отправлен!'

MENU_BUTTONS = {
    'get_weather': 'Покажи погоду',
    'convert': 'Конвертирую валюту',
    'get_animal': 'Покажи милашку',
    'create_poll': 'Создай опрос'
}

WEATHER_RETRY_BUTTON_TEXT = 'Ввести город еще раз'
CONVERT_RETRY_BUTTON_TEXT = 'Попробовать снова'

WEATHER_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&units=metric&appid={}'
CONVERT_ENDPOINT = 'https://api.apilayer.com/exchangerates_data/convert?from={}&to={}&amount={}'
ANIMALS_ENDPOINT = 'https://api.thecatapi.com/v1/images/search'
