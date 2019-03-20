from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text=text)

    print('chat_id :', chat_id)
    print(update)


def main(token):
    bot = Updater(token=TOKEN)
    handler = CommandHandler('start', start)

    bot.dispatcher.add_handler(handler)
    handler = MessageHandler(Filters.text, echo)

    bot.dispatcher.add_handler(handler)

    bot.start_polling()

    print('running telegram bot ...')
    bot.idle()


if __name__ == '__main__':
    TOKEN = '...'  # FIXME: 토큰 지정
    main(TOKEN)

