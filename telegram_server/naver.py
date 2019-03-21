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
