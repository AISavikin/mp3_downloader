from dataclasses import dataclass, field
from utils import check, get_html, log, strip_char
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
        if '_delimetr_' in track:
            delimetr = '_delimetr_'
        else:
            delimetr = ' - '
        author, title = map(strip_char, track.split(delimetr))
        track_list.append(Track(author, title))
    return track_list


def find_tracks(window, path, res: list):
    try:
        tracks = get_track_list(path)
    except FileNotFoundError:
        window['log'].update(f'Файл не найден!')
        return
    progress_bar = window['progress']
    progress_bar.Update(visible=True)
    for i, track in enumerate(tracks, 1):
        if check(track):
            progress_bar.update_bar(i, len(tracks))
            continue
        window['log'].update(f'Поиск:\n{track.author[:37]} - {track.title[:37]}')
        musify(track)
        drivemusic(track)
        mp3bob(track)
        mp3store(track)
        res.append(track)
        progress_bar.update_bar(i, len(tracks))
    window['save'].Update(disabled=False)
    window['download'].Update(disabled=False)
    progress_bar.Update(visible=False)


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
        return
    for result in results:
        author = result.find_all('a')[0].text
        title = result.find_all('a')[1].text
        author, title = map(strip_char, (author, title))
        url = 'https://musify.club' + result.find_all('a')[2].get('href')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            track.title = title
            track.author = author
            track.url = url
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))


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
        return
    results = soup.find_all('div', class_='genre-music inline_player_playlist_main')
    for result in results:
        hrefs = result.find_all('a')
        author = hrefs[2].text
        title = hrefs[1].text
        author, title = map(strip_char, (author, title))
        url = hrefs[0].get('data-url')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            track.title = title
            track.author = author
            track.url = url
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))


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
    if 'никаких результатов' in results.text:
        return
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
        author, title = map(strip_char, (author, title))
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            track.title = title
            track.author = author
            track.url = url
            break
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))

@log.catch()
def mp3store(track: Track):
    if track.url:
        return
    base_url = 'https://mp3store.net/'
    url = f'{base_url}get-search/{track.author} {track.title}'

    html = get_html(url)
    if not html:
        return
    soup = BeautifulSoup(html.text, features='html.parser')
    results = soup.find_all('div', class_='music')[:2]
    if not results:
        log.error(f'{track.author} - {track.title}: Не найдено')
        return
    for result in results:
        author = result.find('b').text
        title = result.find('div', class_='music-info').text[len(author) + 1:]
        author, title = map(strip_char, (author, title))
        html = get_html(base_url + result.find('a').get('href'))
        soup = BeautifulSoup(html.text, features='html.parser')
        url = base_url + soup.find('div', class_='info-panel').find('a').get('href')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            log.info(f'{track.author} - {track.title}: Точное совпадение\n{title} - {author}')
            track.title = title
            track.author = author
            track.url = url
            break
        log.debug(f'{track.author} - {track.title}: Не точное совпадение\n{title} - {author}')
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))
