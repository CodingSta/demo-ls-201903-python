import requests
from bs4 import BeautifulSoup
import telegram


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

chat_id = '42478249'
TOKEN = '880339082:AAEa3xDy1tX5mWGja91s1BqO2Ydr6RQlX9Q'  # FIXME: 토큰 지정

text = '\n'.join(네이버_실검())

bot = telegram.Bot(token=TOKEN)
bot.send_message(chat_id=chat_id, text=text)
