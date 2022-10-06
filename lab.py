import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
import vlc
from utils import Track, FuzzyTrack
from requests.exceptions import SSLError, MissingSchema


@logger.catch()
def fuzzy_matches(track_list):
    my_media = None

    tracks = [track for track in track_list if not track.url and track.fuzzy_matches]

    column = []
    for track in tracks:
        column.append([sg.Frame(f'{track.author} - {track.title}', [], expand_x=True)])
    for indx, frame in enumerate(column):
        frame[0].layout(
            [[sg.Button('▶', k=f'{indx}|{tracks[indx].fuzzy_matches.index(fuzz)}'), sg.Button('⏸'),
              sg.Radio(f'{fuzz.author} - {fuzz.title}', indx, k=f'{indx}:{tracks[indx].fuzzy_matches.index(fuzz)}')]
             for fuzz in tracks[indx].fuzzy_matches])


    layout = [
        [sg.Column(column, vertical_alignment='top', scrollable=True, vertical_scroll_only=True)],
        [sg.Button('Ок')]
    ]
    window = sg.Window('Частичное совпадение', layout, resizable=True, )
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Ок':
            indx_url = [key for key in values if values[key]]
            for i in indx_url:
                indx_tr, indx_fuzz = map(int, i.split(':'))
                track = tracks[indx_tr]
                track.url = track.fuzzy_matches[indx_fuzz].url
            break
        if '⏸' in event:
            if my_media:
                my_media.stop()
                my_media.release()
                my_media = None

        else:
            if my_media:
                pass
            else:
                indx_tr, indx_fuzz = map(int, event.split('|'))
                url_mp3 = tracks[indx_tr].fuzzy_matches[indx_fuzz].url
                my_media = vlc.MediaPlayer(url_mp3)
                my_media.play()
    window.close()

def get_html(url, params=None):
    ua = UserAgent()
    try:
        html = requests.get(url, headers={'User-Agent': ua.random}, params=params)
    except SSLError as err:  # Проверка существование url
        return
    except MissingSchema as err:  # Проверка на схему (http/https)
        return
    return html

@logger.catch()
def drivemusic(track):
    if track.url:
        return
    logger.info(f'musify.club: {track.author} - {track.title}')

    url = 'https://ru-drivemusic.net/'
    params = {
        'do': 'search',
        'subaction': 'search',
        'story': f'{track.author} {track.title}',
    }
    html = get_html(url, params)
    soup = BeautifulSoup(html.text, features='html.parser')
    if 'ничего не найдено' in soup.find('h1').text:
        logger.error('Не найдено')
        return
    results = soup.find_all('div', class_='genre-music inline_player_playlist_main')
    for result in results:
        hrefs = result.find_all('a')
        author = hrefs[2].text
        title = hrefs[1].text
        url = hrefs[0].get('data-url')
        if track.author.lower() in author.lower() and track.title.lower() in title.lower():
            logger.debug('Точное совпадение')
            track.title = title
            track.author = author
            track.url = url
            break
        logger.debug('Не точно')
        track.fuzzy_matches.append(FuzzyTrack(author, title, url=url))


tr = Track(author='Звери', title='Все что тебя касается')
logger.debug(tr)
drivemusic(tr)
logger.debug(tr)

# log.info(UserAgent().random)