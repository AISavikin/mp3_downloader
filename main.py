import PySimpleGUI as sg
from utils import *
import threading


def main_window():
    layout = [
        [sg.Input(readonly=True, key='path'), sg.FileBrowse('Файл'), sg.Button('Найти треки')],
        [sg.Text(' ', k='log')],
        [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress', expand_x=True, visible=False)],
        [sg.Button('Точные совпадения', k='full_match', disabled=True),
         sg.Button('Не точные совпадения', k='fuzzy', disabled=True),
         sg.Button('Сохранить не найденные', k='save', disabled=True)]
    ]

    window = sg.Window('Поиск и скачивание MP3', layout)
    tracks = []
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Найти треки':
            my_thread = threading.Thread(target=start, args=(window, values['path'], tracks))
            my_thread.start()
        if event == 'full_match':
            full_match([track for track in tracks if track.full_match])

    window.close()


def full_match(tracks):
    row1 = [[sg.Text(track.author)] for track in tracks if tracks.index(track) % 3 == 0]
    row2 = [[sg.Text(track.author)] for track in tracks if tracks.index(track) % 3 == 1]
    row3 = [[sg.Text(track.author)] for track in tracks if tracks.index(track) % 3 == 2]
    layout = [
        [sg.Column(row1, vertical_alignment='top'), sg.Column(row2, vertical_alignment='top'),
         sg.Column(row3, vertical_alignment='top')]
    ]
    window = sg.Window('Полное совпадение', layout, resizable=True, )
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
    window.close()


def main():
    main_window()


if __name__ == '__main__':
    main()
