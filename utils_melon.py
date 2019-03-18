import requests
from bs4 import BeautifulSoup

def get_artist_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    res = requests.get("https://www.melon.com/chart/index.htm", headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    tr_tag_list = soup.select('.d_song_list tbody tr')
    
    artist_list = []

    for tr_tag in tr_tag_list:
        artist_tag = tr_tag.select_one('[href*=goArtistDetail]')
        artist_list.append(artist_tag.text)
    
    return artist_list
