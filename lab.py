import requests
import urllib3
from pathlib import Path
from business_logic import Track
from loguru import logger as log
import PySimpleGUI as sg


def download(track, progress):
    file_name = Path('MP3', f'{track.author} - {track.title}.mp3')
    response = requests.request("GET", track.url, stream=True, data=None, headers=None)
    max_val = int(response.headers['Content-Length']) / 10000
    with open(file_name, 'ab') as f:
        for i, chunk in enumerate(response.iter_content(chunk_size=10000)):
            if chunk:
                f.write(chunk)
                progress.Update(i, max_val - 1)


def down_win(track):
    layout = [
        [sg.Text(f'Скачиваю {track.author} - {track.title}')],
        [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
        [sg.Button('OK')]

    ]

    window = sg.Window('!!!!!!!!!', layout)
    while True:
        event, val = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'OK':
            progress = window['progress']
            download(track, progress)
    window.close()


track = Track('Сплин', 'Выхода нет', url='https://mp3bob.ru/download/muz/Splin_-_Vykhoda_net_[mp3pulse.ru]_sample.mp3')
down_win(track)
# response = requests.request("GET", track.url, stream=True, data=None, headers=None)
# log.info(int(response.headers['Content-Length']) / 10000)
# chunks = response.headers
# with open('TEST.mp3', 'ab') as f:
#     for chunk in response.iter_content(chunk_size=10000):
#             if chunk:
#                 f.write(chunk)
#                 log.info(chunk)
