import re
from naver import 네이버_실검, 네이버_블로그_검색


class WhyTask:
    def __init__(self, text):
        self.text = text

    def is_valid(self):
        return self.text == '왜?'

    def proc(self):
        return '니가 궁금해 ~~~'


class YaTask:
    def __init__(self, text):
        self.text = text

    def is_valid(self):
        return self.text == '야'

    def proc(self):
        return '왜?'


class NaverRealtimeKeywordsTask:
    def __init__(self, text):
        self.text = text

    def is_valid(self):
        return self.text.lower() in ['네이버 실검', 'naver']

    def proc(self):
        response = "\n".join(네이버_실검())
        return response


class NaverBlogSearchTask:
    def __init__(self, text):
        self.text = text
        self.matched = None

    def is_valid(self):
        네이버_블로그_검색_키워드_패턴 = r"블로그에?서?(.+)검색"
        self.matched = re.search(네이버_블로그_검색_키워드_패턴, self.text)
        return bool(self.matched)

    def proc(self):
        검색어 = self.matched.group(1)
        line_list = []
        for post in 네이버_블로그_검색(검색어):
            line = '{}\n{}'.format(post['title'], post['url'])
            line_list.append(line)
        response = '\n\n'.join(line_list)
        return response
