import PySimpleGUI as sg
from utils import *
import threading
import vlc


def main_window():
    layout = [
        [sg.Input(readonly=True, key='path'), sg.FileBrowse('Файл', file_types=(('TXT', '*.txt'),)),
         sg.Button('Найти треки')],
        [sg.Text('Поиск:\n', k='log')],
        [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress', expand_x=True)],
        [sg.Button('Список для скачивания', k='full_match'),
         sg.Button('Не точные совпадения', k='fuzzy'),
         sg.Button('Сохранить не найденные', k='save', disabled=True)]
    ]

    window = sg.Window('Поиск и скачивание MP3', layout, size=(500, 150))
    track_list = []
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Найти треки':
            my_thread = threading.Thread(target=start, args=(window, values['path'], track_list))
            my_thread.start()
        if event == 'full_match':
            full_match([track for track in track_list if track.url])
        if event == 'fuzzy':
            fuzzy_matches(track_list)

        if event == 'save':
            save_not_found([track for track in track_list if not track.url])

    window.close()


def full_match(tracks):
    row1 = [[sg.Text(f'{track.author} - {track.title[:23]}')] for track in tracks if tracks.index(track) % 3 == 0]
    row2 = [[sg.Text(f'{track.author} - {track.title[:23]}')] for track in tracks if tracks.index(track) % 3 == 1]
    row3 = [[sg.Text(f'{track.author} - {track.title[:23]}')] for track in tracks if tracks.index(track) % 3 == 2]
    main_column = [sg.Column(row1, vertical_alignment='top'),
                   sg.Column(row2, vertical_alignment='top'),
                   sg.Column(row3, vertical_alignment='top')]

    layout = [
        [sg.Column([main_column], vertical_scroll_only=True, scrollable=True, size_subsample_height=2)]
    ]
    window = sg.Window('Список для скачивания', layout, resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
    window.close()


def fuzzy_matches(track_list):
    my_media = None

    tracks = [track for track in track_list if not track.url and track.fuzzy_matches]
    logger.info(tracks)
    column = []
    for track in tracks:
        column.append([sg.Frame(f'{track.author} - {track.title}', [], expand_x=True)])
    for indx, frame in enumerate(column):
        frame[0].layout(
            [[sg.Button('▶', k=f'{indx}|{tracks[indx].fuzzy_matches.index(fuzz)}'), sg.Button('⏸'),
              sg.Radio(f'{fuzz.author} - {fuzz.title[:23]}', indx, k=f'{indx}:{tracks[indx].fuzzy_matches.index(fuzz)}')]
             for fuzz in tracks[indx].fuzzy_matches])

    layout = [
        [sg.Column(column, vertical_alignment='top', scrollable=True, vertical_scroll_only=True, size=(500, 600))],
        [sg.Button('Добавить в список скачивания')]
    ]
    window = sg.Window('Частичное совпадение', layout, resizable=True)
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


def main():
    main_window()


if __name__ == '__main__':
    main()
