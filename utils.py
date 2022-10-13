import os
import requests
from pathlib import Path
from fake_useragent import UserAgent
from loguru import logger as log
from requests.exceptions import SSLError, MissingSchema, InvalidSchema


def get_html(url, params=None):
    try:
        html = requests.get(url, headers={'User-Agent': UserAgent().random}, params=params)
    except SSLError:  # Проверка существование url
        log.error('URL Не существует')
        return
    except MissingSchema:  # Проверка на схему (http/https)
        log.error('Не указана схема (http/https)')
        return
    except InvalidSchema:
        log.error('Неверная схема (http/https)')
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


def download(track, progress=None):
    file_name = Path('MP3', f'{track.author} - {track.title}.mp3')
    response = get_html(track.url)
    if not response:
        return
    if not progress:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return
    try:
        max_val = int(response.headers['Content-Length']) / 10000
        with open(file_name, 'ab') as f:
            for i, chunk in enumerate(response.iter_content(chunk_size=10000)):
                if chunk:
                    f.write(chunk)
                    progress.Update(i, max_val - 1)
    except KeyError:
        track.url = ''

def start_download(window, tracks):
    progress_bar = window['progress']
    progress_file = window['progress_file']
    progress_bar.Update(0, visible=True)
    progress_file.Update(visible=True)
    i = 0
    for i, track in enumerate(tracks, 1):
        if check(track):
            progress_bar.update_bar(i, len(tracks))
            continue
        window['log'].update(f'Скачиваю:\n{track.author} - {track.title}')
        download(track, progress_file)
        progress_bar.update_bar(i, len(tracks))
    window['log'].update(f'Скачивание завершено!\n{i} Треков')
    progress_bar.Update(visible=False)
    progress_file.Update(visible=False)
