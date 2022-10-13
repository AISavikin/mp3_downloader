from dataclasses import dataclass, field
from utils import get_html, log, strip_char, time_it
from bs4 import BeautifulSoup
import multiprocessing

@dataclass
class FuzzyTrack:
    author: str
    title: str
    url: str = ''


@dataclass
class Track(FuzzyTrack):
    fuzzy_matches: list = field(default_factory=list)

def get_track_list(path):
    """
    Создает список объектов типа Track, из TXT-файла
    :param path:
    :return:
    """
    track_list = []

    with open(path, encoding='UTF-8') as f:
        tracks = f.readlines()
    delimetr = ' - '
    for track in tracks:
        if '_delimetr_' in track:
            delimetr = '_delimetr_'
        author, title = track.split(delimetr)
        author = strip_char(author, find=False)
        title = strip_char(title, find=False)
        track_list.append(Track(author, title))
    return track_list

def find_tracks(window, path, res:list):
    try:
        tracks = get_track_list(path)
    except FileNotFoundError:
        window['log'].update(f'Файл не найден!')
        return
    funcs = (musify, drivemusic, mp3bob, mp3store)
    progress_bar = window['progress']
    progress_bar.Update(visible=True)
    for i, func in enumerate(funcs, 1):
        window['log'].update(f'Поиск на сайте:\n{func}')
        tracks = multy(tracks, func)
        progress_bar.update_bar(i, len(funcs))
    window['save'].Update(disabled=False)
    window['download'].Update(disabled=False)
    progress_bar.Update(visible=False)
    res.extend(tracks)
    return tracks


def musify(track: Track):
    if track.url:
        return track
    author_fs = strip_char(track.author)
    title_fs = strip_char(track.title)
    url = 'https://w1.musify.club/search'
    params = {
        'searchText': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    if not html:
        return track
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
            track.fuzzy_matches = None
            return track
        log.debug(f'{track.author} - {track.title}: Не точное совпадение')  # LOGS
        log.debug(f'{author} - {title}')  # LOGS
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
    return track

def drivemusic(track):
    if track.url:
        return track
    author_fs = strip_char(track.author)
    title_fs = strip_char(track.title)
    url = 'https://ru-drivemusic.net/'
    params = {
        'do': 'search',
        'subaction': 'search',
        'story': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    if not html:
        return track
    soup = BeautifulSoup(html.text, features='html.parser')
    if 'ничего не найдено' in soup.find('h1').text:
        log.error(f'{track.author} - {track.title}: Не найдено')
        return track
    results = soup.find_all('div', class_='genre-music inline_player_playlist_main')
    for result in results:
        hrefs = result.find_all('a')
        author = hrefs[2].text
        title = hrefs[1].text
        url = hrefs[0].get('data-url')
        if author_fs.lower() in strip_char(author).lower() and title_fs.lower() in strip_char(title).lower():
            log.info(f'{track.author} - {track.title}: Точное совпадение')  # LOGS
            log.info(f'{author} - {title}')  # LOGS
            track.title = strip_char(title, find=False)
            track.author = strip_char(author, find=False)
            track.url = url
            track.fuzzy_matches = None
            return track
        log.debug(f'{track.author} - {track.title}: Не точное совпадение')  # LOGS
        log.debug(f'{author} - {title}')  # LOGS
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
    return track

def mp3bob(track):
    if track.url:
        return track
    author_fs = strip_char(track.author)
    title_fs = strip_char(track.title)
    url = 'https://mp3bob.ru/'
    params = {
        'do': 'search',
        'subaction': 'search',
        'story': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    if not html:
        return track
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find('div', class_='wrapp sort_page')
    if 'никаких результатов' in results.text:
        log.error(f'{track.author} - {track.title}: Не найдено')
        return track
    song_items = results.find_all('div', class_='song-item')
    for result in song_items:
        hrefs = result.find_all('a')
        url = 'https://mp3bob.ru' + hrefs[0].get('data-url')
        span = hrefs[1].find_all('span')
        title = span[0].text
        if len(span) == 1:
            author = 'Без автора'
        else:
            author = span[1].text
        if author_fs.lower() in strip_char(author).lower() and title_fs.lower() in strip_char(title).lower():
            log.info(f'{track.author} - {track.title}: Точное совпадение')  # LOGS
            log.info(f'{author} - {title}')  # LOGS
            track.title = strip_char(title, find=False)
            track.author = strip_char(author, find=False)
            track.url = url
            track.fuzzy_matches = None
            return track
        log.debug(f'{track.author} - {track.title}: Не точное совпадение')  # LOGS
        log.debug(f'{author} - {title}')  # LOGS
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
    return track

def mp3store(track: Track):
    if track.url:
        return track
    log.debug(f'Ищу {track.author} - {track.title}')
    author_fs = strip_char(track.author)
    title_fs = strip_char(track.title)
    base_url = 'https://mp3store.net/'
    url = f'{base_url}get-search/{track.author} {track.title}'

    html = get_html(url)
    if not html:
        return track
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find_all('div', class_='music')[:5]
    if not results:
        log.error(f'{track.author} - {track.title}: Не найдено')  # LOGS
        return track
    for result in results:
        author = result.find('b').text
        title = result.find('div', class_='music-info').text[len(author) + 1:]
        if not (author_fs.lower() in strip_char(author).lower()) or not (title_fs.lower() in strip_char(title).lower()):
            continue
        html = get_html(base_url + result.find('a').get('href'))
        soup = BeautifulSoup(html.text, features='html.parser')
        url = base_url + soup.find('div', class_='info-panel').find('a').get('href')
        if author_fs.lower() in strip_char(author).lower() and title_fs.lower() in strip_char(title).lower():
            log.info(f'{track.author} - {track.title}: Точное совпадение')  # LOGS
            log.info(f'{author} - {title}')  # LOGS
            track.title = strip_char(title, find=False)
            track.author = strip_char(author, find=False)
            track.url = url
            track.fuzzy_matches = None
            return track
        log.debug(f'{track.author} - {track.title}: Не точное совпадение')  # LOGS
        log.debug(f'{author} - {title}')  # LOGS
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
    return track

@time_it
def multy(tracklist, func):
    with multiprocessing.Pool(16) as p:
        res = p.map(func, tracklist)
    return res

