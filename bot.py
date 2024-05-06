import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import requests
from integrations import Constants

city = None

TELEGRAM_BOT_TOKEN = "TOKEN"
WEATHER_API_KEY = 'KEY'


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🌆In which city do you live?")


def menu(update: Update, context: CallbackContext) -> None:
    global city
    city = update.message.text
    keyboard = [
        [InlineKeyboardButton("Current Weather", callback_data='current_weather')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('👇Choose an option:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'current_weather':
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}")

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather_data = data['weather'][0]
            celsius_temp = main['temp'] - 273.15
            message = f"<b>🌤Current weather in {city}</b>:\n\n"
            message += f"<b>🌡Temperature: {celsius_temp:.2f}°C</b>\n\n"
            message += f"<b>Description: {weather_data['description'].capitalize()}</b>\n\n"
            message += f"<b>Humidity: {main['humidity']}%</b>\n"
            query.edit_message_text(text=message, parse_mode='HTML')
        else:
            query.edit_message_text(text="Can't find weather information for this city. Try again.")


def main() -> None:
    updater = Updater(token=Constants.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, menu))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
