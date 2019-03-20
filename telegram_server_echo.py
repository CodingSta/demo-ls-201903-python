from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler


import requests
from bs4 import BeautifulSoup

def 네이버_실검():
    res = requests.get("http://naver.com")
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    tag_list = soup.select('.PM_CL_realtimeKeyword_rolling .ah_k')

    keyword_list = []
    for rank, tag in enumerate(tag_list, 1): # 항상 하위 block 전에 콤마(:)를 씁니다.
        keyword = tag.text
        keyword_list.append(keyword)

    return keyword_list


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text  # 수신한 텍스트 메세지

    if text == '네이버 실검':
        response = "\n".join(네이버_실검())
    else:
        response = "니가 무슨 말 하는 지 모르겠어. :("

    bot.send_message(chat_id=chat_id, text=response)

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
