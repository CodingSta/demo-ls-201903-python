from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
import tasks


TASK_CLS_LIST = [
    tasks.WhyTask,
    # tasks.YaTask,
    tasks.NaverRealtimeKeywordsTask,
    tasks.NaverBlogSearchTask,
    tasks.FaceTask,
]


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id

    print('chat_id :', chat_id)
    print(update)

    try:
        for task_cls in TASK_CLS_LIST:
            task = task_cls(update, TOKEN)
            if task.is_valid():
                response = task.proc()
                break
        else:
            # break없이 마지막까지 루프를 돌고, 루프가 종료되었을 경우
            response = '니가 무슨 말을 하는 지 모르겠어. :('
    except Exception as e:
        response = '예기치못한 오류가 발생했습니다. -' + str(e)

    bot.send_message(chat_id=chat_id, text=response)



def main(token):
    bot = Updater(token=TOKEN)

    # /start
    handler = CommandHandler('start', start)
    bot.dispatcher.add_handler(handler)

    handler = MessageHandler(Filters.all, echo)
    bot.dispatcher.add_handler(handler)

    bot.start_polling()

    print('running telegram bot ...')
    bot.idle()


if __name__ == '__main__':
    TOKEN = '880339082:AAEa3xDy1tX5mWGja91s1BqO2Ydr6RQlX9Q'  # FIXME: 토큰 지정
    main(TOKEN)
