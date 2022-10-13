import requests
import urllib3
from pathlib import Path
from business_logic import Track, BeautifulSoup, FuzzyTrack, mp3store
from utils import UserAgent, strip_char, SSLError, MissingSchema, InvalidSchema, get_html
from loguru import logger as log
import PySimpleGUI as sg
import time


def time_it(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        res = func(*args, **kargs)
        res_time = time.time() - start_time
        print(f'Время выолнения {round(float(res_time), 3)}')
        return res

    return wrapper

@time_it
@log.catch
def pars_YM(path):
    with open(path, encoding='utf-8') as f:
        tarcks = f.readlines()
    for track in tarcks:
        log.debug(track)
        url = 'https://music.yandex.ru/search'
        ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.9.1 Yowser/2.5 Safari/537.36'
        html = requests.get(url, headers={'User-Agent': ua}, params={'text': track}).text
        soup = BeautifulSoup(html, features='html.parser')
        author = soup.find('span', class_='d-track__artists').find('a').get('title')
        title = soup.find('div', class_='d-track__name').get('title')
        log.info(f'{author} - {title}')

if __name__ == '__main__':
    pars_YM('ira_playlist.txt')
