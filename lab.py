import requests
import urllib3
from pathlib import Path
from business_logic import Track, BeautifulSoup, FuzzyTrack
from utils import get_html, UserAgent, strip_char
from loguru import logger as log
import PySimpleGUI as sg

@log.catch
def mp3store(track: Track):
    if track.url:
        return
    base_url = 'https://mp3store.net/'
    url = f'{base_url}get-search/{track.author} {track.title}'

    html = get_html(url)
    if not html:
        return
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find_all('div', class_='music')[:3]
    if not results:
        return
    for result in results:
        author = result.find('b').text
        title = result.find('div', class_='music-info').text[len(author) + 1:]
        author, title = map(strip_char, (author, title))
        html = get_html(base_url + result.find('a').get('href'))
        soup = BeautifulSoup(html.text, features='html.parser')
        url = base_url + soup.find('div', class_='info-panel').find('a').get('href')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            track.title = title
            track.author = author
            track.url = url
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))


def mp3_download():
    url = 'https://mp3store.net/get-music/splin-vyhoda-net-djgraff-hype-ext-mix/'
    html = get_html(url)
    soup = BeautifulSoup(html.text, features='html.parser')
    mp3_url = 'https://mp3store.net/' + soup.find('div', class_='info-panel').find('a').get('href')
    response = requests.request("GET", mp3_url, stream=True, data=None, headers={'User-Agent': UserAgent().random})
    log.debug(response.headers)


if __name__ == '__main__':
    tr = Track('алое вера', 'ты что такой')
    # tr = Track('sasf','me')
    mp3store(tr)
    log.debug(tr)
    # mp3_download()
