MENU_TEXT = 'Привет, {}!\nЧто я могу для тебя сделать?'

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
