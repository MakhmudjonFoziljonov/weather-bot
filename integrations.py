import requests


class Constants:
    TELEGRAM_BOT_TOKEN = "5677756493:AAFxIsGxpmF4h8nabX_cdX6xx4hNDkwLpz0"
    WEATHER_API_KEY = '9154bdf34f1724dade7661f0ae461190'
    ABOUT_MESSAGE = 'Created by chivalrous'
    COMMAND_START = 'start'


def get_weather_data(city):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Constants.WEATHER_API_KEY}")
    if response.status_code == 200:
        data = response.json()
        city = data['name']
        main = data['weather'][0]['main']
        temp = round(data['main']['temp'] - 273, 2)
        speed = data['wind']['speed']
        text = (f"<b>🏙City name</b>: {city}\n\n"
                f"<b>🌤Information about weather</b>: {main}\n\n"
                f"<b>🌡️Current temperature</b>: {temp}°C\n\n"
                f"<b>💨Wind speed</b>: {speed} km/h")
        return text
    return "Please enter the correct city name"
