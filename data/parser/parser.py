import requests
from bs4 import BeautifulSoup
from os import path
import re

file_name = path.abspath('Parser')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/87.0.4280.88 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


class ParsError(Exception):
    pass


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_page(link):
    lk = get_html(link)
    soup = BeautifulSoup(lk.text, 'html.parser')
    template = r'/[0-9]+'
    link = soup.find('a', class_="next").get('href')
    return int(re.search(template, link).group()[1:]) + 1


def get_content(html, pos):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="postContainer")
    posts = []
    post_url = []
    for item in items:
        url = item.find('div', class_="image").find('img').get('src')
        purl = item.find('div', class_="ufoot_first").find('a', class_="link").get('href')
        posts.append(url)
        post_url.append(purl)
    return posts[pos-1], URL + post_url[pos-1]


def gif_parse(html, pos):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="postContainer")
    gifs = []
    post_url = []
    for item in items:
        try:
            url = item.find('div', class_="image").find('a', class_="video_gif_source").get('href')
        except AttributeError:
            url = item.find('div', class_="image").find('a', class_="prettyPhotoLink")
        purl = item.find('div', class_="ufoot_first").find('a', class_="link").get('href')
        gifs.append(url)
        post_url.append(purl)
    return gifs[pos-1], URL + post_url[pos-1]


def parse(name, pos, page):
    global URL
    if name == "/tag/ecchi":
        URL = "http://joyreactor.com/"
    else:
        URL = "http://anime.reactor.cc"
    if page > 1:
        page = '/' + str(get_page(URL+name) - (page - 1))
        html = get_html(URL + name + page)
    else:
        html = get_html(URL + name)
    if html.status_code == 200:
        if name == "/tag/Anime+%D0%93%D0%B8%D1%84%D0%BA%D0%B8":
            return gif_parse(html.text, pos)
        else:
            return get_content(html.text, pos)
    else:
        raise ParsError