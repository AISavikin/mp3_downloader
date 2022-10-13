import requests
import urllib3
from pathlib import Path
from business_logic import Track, BeautifulSoup, FuzzyTrack, mp3store, get_track_list
from utils import UserAgent, SSLError, MissingSchema, InvalidSchema, get_html, time_it, strip_char
from loguru import logger as log
import PySimpleGUI as sg
import multiprocessing

def musify(track: Track):
    if track.url:
        return
    author_fs = strip_char(track.author)
    title_fs = strip_char(track.title)
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
        log.error(f'{track.author} - {track.title}: Не найдено')
        return track
    for result in results:
        author = result.find_all('a')[0].text
        title = result.find_all('a')[1].text
        if ' - ' in title:  # TODO убедится, что нет ошибок
            title = title.split(' - ')[1]
        url = 'https://musify.club' + result.find_all('a')[2].get('href')
        if author_fs.lower() in strip_char(author).lower() and title_fs.lower() in strip_char(title).lower():
            log.info(f'{track.author} - {track.title}: Точное совпадение')  # LOGS
            log.info(f'{author} - {title}')  # LOGS
            track.title = strip_char(title, find=False)
            track.author = strip_char(author, find=False)
            track.url = url
            return track
        log.debug(f'{track.author} - {track.title}: Не точное совпадение')  # LOGS
        log.debug(f'{author} - {title}')  # LOGS
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
        log.error(track)
        return track





if __name__ == '__main__':
    tracklist = get_track_list('txt/test_tracks.txt')
    full = [track for track in tracklist if track.url]
    log.debug(len(full))
    print(multiprocessing.cpu_count())
    with multiprocessing.Pool(16) as p:
        res = p.map(musify, tracklist)

    tracklist = res
    full = [track for track in tracklist if track.url]
    log.debug(len(full))

    log.info(res)


