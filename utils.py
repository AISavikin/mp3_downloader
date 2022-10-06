from loguru import logger
from dataclasses import dataclass, field
import requests
from fake_useragent import UserAgent
from requests.exceptions import SSLError, MissingSchema
from bs4 import BeautifulSoup


@dataclass
class FuzzyTrack:
    author: str
    title: str
    url: str = ''


@dataclass
class Track(FuzzyTrack):
    fuzzy_matches: list = field(default_factory=list)


@logger.catch
def get_html(url):
    ua = UserAgent()
    try:
        html = requests.get(url, headers={'User-Agent': ua.random})
    except SSLError as err:  # Проверка существование url
        return
    except MissingSchema as err:  # Проверка на схему (http/https)
        return
    return html


@logger.catch
def musify(track: Track):
    logger.info(f'{track.author} - {track.title}')
    if track.url:
        return
    html = get_html(f'https://w1.musify.club/search?searchText={track.author} {track.title}')
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find_all('div', class_='playlist__item')[:2]
    for result in results:
        author = result.find_all('a')[0].text
        title = result.find_all('a')[1].text
        url = 'https://musify.club' + result.find_all('a')[2].get('href')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            track.title = title
            track.author = author
            track.url = url
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))


def get_track_list(path):
    """
    Создает список объектов типа Track, из TXT-файла
    :param path:
    :return:
    """
    with open(path, encoding='UTF-8') as f:
        tracks = f.readlines()
    return [Track(tr.split('-')[0].strip(), tr.split('-')[1].strip()) for tr in tracks]


def save_not_found(tracks):
    with open('not_found.txt', 'w', encoding='utf-8') as f:
        f.writelines([f'{track.author} - {track.title}\n' for track in tracks])


def start(window, path, res: list):
    progress_bar = window['progress']
    track_list = get_track_list(path)
    i = 0
    progress_bar.Update(visible=True)
    for track in track_list:
        window['log'].update(f'Поиск:\n{track.author} - {track.title}')
        musify(track)
        res.append(track)
        i += 1
        progress_bar.update_bar(i, len(track_list))
    window['full_match'].Update(disabled=False)
    window['fuzzy'].Update(disabled=False)
    window['save'].Update(disabled=False)
    logger.info(track_list)
