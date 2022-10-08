import os
import requests
from pathlib import Path
from fake_useragent import UserAgent
from loguru import logger as log
from requests.exceptions import SSLError, MissingSchema


def get_html(url, params=None):
    ua = UserAgent()
    try:
        html = requests.get(url, headers={'User-Agent': ua.random}, params=params)
    except SSLError:  # Проверка существование url
        log.error('URL Не существует')
        return
    except MissingSchema:  # Проверка на схему (http/https)
        log.error('Не указана схема (http/https)')
        return
    if html.status_code != 200:
        log.error(f'Ошибка сервера код: {html}')
    return html


def save_not_found(tracks):
    with open('not_found.txt', 'w', encoding='utf-8') as f:
        f.writelines([f'{track.author} - {track.title}\n' for track in tracks])


def check(track):
    file_name = Path('MP3', f'{track.author} - {track.title}.mp3')
    if os.path.exists(file_name):
        log.info(f'{file_name} Уже существует')
        return True

def strip_char(word: str):
    chars = r'?*<>:"\/|'
    for char in chars:
        word = word.replace(char, '')
    return word.strip()

def download(track):
    file_name = Path('MP3', f'{track.author} - {track.title}.mp3')
    with open(file_name, 'wb') as f:
        f.write(requests.get(track.url).content)


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
