import re
from io import BytesIO
from naver import 네이버_실검, 네이버_블로그_검색
from utils import get_file
import cognitive_face as CF


KEY = 'dc92e69d27e8463e8becd3035dce9940'  # 강사 Key
CF.Key.set(KEY)

BASE_URL = 'https://koreacentral.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)


class FaceTask:
    def __init__(self, update, token):
        self.photos = update.message.photo
        self.token = token

    def is_valid(self):
        return len(self.photos) > 0

    def proc(self):
        # for photo in self.photos:
        #     print(photo.file_id, photo.width, photo.height)
        photo = self.photos[0]  # 제일 작은 사진
        img_data = get_file(photo.file_id, self.token)
        f = BytesIO(img_data)

        attributes = 'age,gender,smile,facialHair,headPose,glasses'
        faces = CF.face.detect(f, attributes=attributes)
        return str(faces)


class WhyTask:
    def __init__(self, update, token):
        self.text = update.message.text or ''  # 수신한 텍스트 메세지

    def is_valid(self):
        return self.text == '왜?'

    def proc(self):
        return '니가 궁금해 ~~~'


class YaTask:
    def __init__(self, update, token):
        self.text = update.message.text or ''  # 수신한 텍스트 메세지

    def is_valid(self):
        return self.text == '야'

    def proc(self):
        return '왜?'


class NaverRealtimeKeywordsTask:
    def __init__(self, update, token):
        self.text = update.message.text or ''  # 수신한 텍스트 메세지

    def is_valid(self):
        return self.text.lower() in ['네이버 실검', 'naver']

    def proc(self):
        response = "\n".join(네이버_실검())
        return response


class NaverBlogSearchTask:
    def __init__(self, update, token):
        self.text = update.message.text or ''  # 수신한 텍스트 메세지
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
