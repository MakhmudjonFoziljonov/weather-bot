from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram import Update
from integrations import Constants


def start(update: Update, context: CallbackContext):
    update.message.reply_text('🌆Name the city you want to know')


def main():
    updater = Updater(Constants.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(Constants.COMMAND_START, start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
