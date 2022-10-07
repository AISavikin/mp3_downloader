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
def get_html(url, params=None):
    ua = UserAgent()
    try:
        html = requests.get(url, headers={'User-Agent': ua.random}, params=params)
    except SSLError as err:  # Проверка существование url
        logger.error('URL Не существует')
        return
    except MissingSchema as err:  # Проверка на схему (http/https)
        logger.error('Не указана схема (http/https)')
        return
    if html.status_code != 200:
        logger.error(f'Ошибка сервера код: {html}')
    return html


@logger.catch
def musify(track: Track):
    if track.url:
        return
    url = 'https://w1.musify.club/search'
    params = {
        'searchText': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find_all('div', class_='playlist__item')[:2]
    if not results:
        return
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

@logger.catch()
def drivemusic(track):
    if track.url:
        return

    url = 'https://ru-drivemusic.net/'
    params = {
        'do': 'search',
        'subaction': 'search',
        'story': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    soup = BeautifulSoup(html.text, features='html.parser')
    if 'ничего не найдено' in soup.find('h1').text:
        return
    results = soup.find_all('div', class_='genre-music inline_player_playlist_main')
    for result in results:
        hrefs = result.find_all('a')
        author = hrefs[2].text
        title = hrefs[1].text
        url = hrefs[0].get('data-url')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            track.title = title
            track.author = author
            track.url = url
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))

@logger.catch()
def mp3bob(track):
    if track.url:
        return

    url = 'https://mp3bob.ru/'
    params = {
        'do': 'search',
        'subaction': 'search',
        'story': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find('div', class_='wrapp sort_page')
    if 'поиск по сайту не дал никаких результатов' in results.text:
        return
    song_items = results.find_all('div', class_='song-item')
    for result in song_items:
        hrefs = result.find_all('a')
        url = hrefs[0].get('data-url')
        title = hrefs[1].find_all('span')[0].text
        author = hrefs[1].find_all('span')[1].text
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

@logger.catch()
def start(window, path, res: list):
    progress_bar = window['progress']
    track_list = get_track_list(path)
    i = 0
    for track in track_list:
        window['log'].update(f'Поиск:\n{track.author} - {track.title}')
        musify(track)
        drivemusic(track)
        mp3bob(track)
        if track.url:
            logger.debug(f'{track.author} - {track.title}: Точное совпадение')
        elif track.fuzzy_matches:
            logger.debug(f'{track.author} - {track.title}: Неточное совпадение')
        else:
            logger.error(f'{track.author} - {track.title}: Не найдено')
        res.append(track)
        i += 1
        progress_bar.update_bar(i, len(track_list))
    window['save'].Update(disabled=False)
