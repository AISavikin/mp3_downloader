import os
import PySimpleGUI as sg
from loguru import logger as log
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


@log.catch
def get_html(url, params=None):
    ua = UserAgent()
    try:
        html = requests.get(url, headers={'User-Agent': ua.random}, params=params)
    except SSLError as err:  # Проверка существование url
        log.error('URL Не существует')
        return
    except MissingSchema as err:  # Проверка на схему (http/https)
        log.error('Не указана схема (http/https)')
        return
    if html.status_code != 200:
        log.error(f'Ошибка сервера код: {html}')
    return html


@log.catch
def musify(track: Track):
    if track.url:
        return
    url = 'https://w1.musify.club/search'
    params = {
        'searchText': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    if not html:
        return
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find_all('div', class_='playlist__item')[:2]
    if not results:
        log.error(f'{track.author} - {track.title} : Не найдено')
        return
    for result in results:
        author = result.find_all('a')[0].text
        title = result.find_all('a')[1].text
        url = 'https://musify.club' + result.find_all('a')[2].get('href')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            track.title = title
            track.author = author
            track.url = url
            log.info(f'{track.author} - {track.title} : Точное совпадение')
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
    log.debug(f'{track.author} - {track.title} : Не точное совпадение')

@log.catch()
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
    if not html:
        return
    soup = BeautifulSoup(html.text, features='html.parser')
    if 'ничего не найдено' in soup.find('h1').text:
        log.error(f'{track.author} - {track.title} : Не найдено')
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
            log.info(f'{track.author} - {track.title} : Точное совпадение')
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
    log.debug(f'{track.author} - {track.title} : Не точное совпадение')

@log.catch()
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
    if not html:
        return
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find('div', class_='wrapp sort_page')
    if 'поиск по сайту не дал никаких результатов' in results.text:
        log.error(f'{track.author} - {track.title} : Не найдено')
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
            log.info(f'{track.author} - {track.title} : Точное совпадение')
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
    log.debug(f'{track.author} - {track.title} : Не точное совпадение')


def get_track_list(path):
    """
    Создает список объектов типа Track, из TXT-файла
    :param path:
    :return:
    """
    track_list = []
    with open(path, encoding='UTF-8') as f:
        tracks = f.readlines()
    for track in tracks:
        if track.count('-') > 1:
            track = track.replace('-', ' ', 1)
        track_list.append(Track(track.split('-')[0].strip(), track.split('-')[1].strip()))
    return track_list


def save_not_found(tracks):
    with open('not_found.txt', 'w', encoding='utf-8') as f:
        f.writelines([f'{track.author} - {track.title}\n' for track in tracks])

def check(track):
    file_name = f'MP3/{track.author} - {track.title}.mp3'
    if os.path.exists(file_name):
        log.info(f'{file_name} Уже существует')
        return True

@log.catch()
def find_tracks(window, path, res: list):
    progress_bar = window['progress']
    track_list = get_track_list(path)
    i = 0
    for track in track_list:
        if check(track):
            i += 1
            progress_bar.update_bar(i, len(track_list))
            continue
        window['log'].update(f'Поиск:\n{track.author} - {track.title}')
        musify(track)
        drivemusic(track)
        mp3bob(track)
        res.append(track)
        i += 1
        progress_bar.update_bar(i, len(track_list))
    log.debug(track_list)
    window['save'].Update(disabled=False)
    window['download'].Update(disabled=False)

@log.catch()
def download(track):
    file_name = f'MP3/{track.author} - {track.title}.mp3'
    for char in r'?*<>:"\/|':
        file_name = file_name.replace(char, ' ')
    if os.path.exists(file_name):
        log.info(f'{file_name} Уже существует')
        return
    with open(file_name, 'wb') as f:
        f.write(requests.get(track.url).content)

@log.catch()
def start_download(window, tracks):
    progress_bar = window['progress']
    i = 0
    for track in tracks:
        if check(track):
            i += 1
            progress_bar.update_bar(i, len(tracks))
            continue
        window['log'].update(f'Скачиваю:\n{track.author} - {track.title}')
        download(track)
        i += 1
        progress_bar.update_bar(i, len(tracks))
    window['log'].update(f'Скачивание завершено!\n{i} Треков')