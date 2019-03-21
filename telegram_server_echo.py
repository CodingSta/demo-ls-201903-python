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


def 네이버_블로그_검색(keyword):
    url = 'https://search.naver.com/search.naver'
    params = {
        'where': 'post',
        'sm': 'tab_jum',
        'query': keyword,
    }
    res = requests.get(url, params=params)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    post_list = []
    for tag in soup.select('.sh_blog_title'):
        title = tag.text
        url = tag['href']
        # TODO: 요약문, 대표이미지, 글쓴날짜
        post_list.append({
            'url': url,
            'title': title,
        })
    return post_list


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text  # 수신한 텍스트 메세지

    if text.lower() in ['네이버 실검', 'naver']:
        response = "\n".join(네이버_실검())
    elif text.startswith('블로그 검색:'):
        검색어 = text[7:]
        line_list = []
        for post in 네이버_블로그_검색(검색어):
            line = '{}\n{}'.format(post['title'], post['url'])
            line_list.append(line)
        response = '\n\n'.join(line_list)
    # TODO: 네이버 블로그에서 LS산전 검색해줘 => 정규표현식
    else:
        response = "니가 무슨 말 하는 지 모르겠어. :("

    bot.send_message(chat_id=chat_id, text=response)

    print('chat_id :', chat_id)
    print(update)


def main(token):
    bot = Updater(token=TOKEN)

    # /start
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
