import PySimpleGUI as sg
from bs4 import BeautifulSoup
from loguru import logger as log
import vlc
from utils import Track, FuzzyTrack, get_html


# inst = vlc.Instance()
# list_player = inst.media_list_player_new()
# media_list = inst.media_list_new([])
# list_player.set_media_list(media_list)
# player = list_player.get_media_player()
#

def play():
    my_media = None
    layout = [
        [sg.Input(), sg.Button('▶'), sg.Button('⏸')]
    ]

    window = sg.Window('dfgsdfg', layout)

    while True:
        event, vals = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        if event == '▶':
            my_media = vlc.MediaPlayer(vals[0])
            my_media.play()
        if event == '⏸':
            if my_media:
                my_media.stop()

    # window.close()

@log.catch()
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



test_tracks =  [Track(author='Don McLean', title='Don Mclean - American Pie', url='https://musify.club/track/dl/18437894/don-mclean-don-mclean-american-pie.mp3', fuzzy_matches=[]), Track(author='Паша Руденко', title='Ебш', url='', fuzzy_matches=[FuzzyTrack(author='Паша Руденко', title='Пятница', url='https://musify.club/track/dl/13737391/%d0%bf%d0%b0%d1%88%d0%b0-%d1%80%d1%83%d0%b4%d0%b5%d0%bd%d0%ba%d0%be-%d0%bf%d1%8f%d1%82%d0%bd%d0%b8%d1%86%d0%b0.mp3'), FuzzyTrack(author='Паша Руденко', title='Немой', url='https://musify.club/track/dl/10640390/%d0%bf%d0%b0%d1%88%d0%b0-%d1%80%d1%83%d0%b4%d0%b5%d0%bd%d0%ba%d0%be-%d0%bd%d0%b5%d0%bc%d0%be%d0%b8.mp3')]), Track(author='Metallica', title='Nothing Else Matters (Demo)', url='https://musify.club/track/dl/3071685/metallica-nothing-else-matters-demo.mp3', fuzzy_matches=[FuzzyTrack(author='Silenzium', title='Nothing Else Matters (Metallica)', url='https://musify.club/track/dl/3321400/silenzium-nothing-else-matters-metallica.mp3')]), Track(author='Пневмослон', title='Ебашу как в последний раз', url='', fuzzy_matches=[FuzzyTrack(author='Пневмослон', title='Ебашу, Как В Последний Раз', url='https://musify.club/track/dl/9303415/%d0%bf%d0%bd%d0%b5%d0%b2%d0%bc%d0%be%d1%81%d0%bb%d0%be%d0%bd-%d0%b5%d0%b1%d0%b0%d1%88%d1%83-%d0%ba%d0%b0%d0%ba-%d0%b2-%d0%bf%d0%be%d1%81%d0%bb%d0%b5%d0%b4%d0%bd%d0%b8%d0%b8-%d1%80%d0%b0%d0%b7.mp3'), FuzzyTrack(author='Порнофильмы', title='Как в последний раз', url='https://musify.club/track/dl/6934317/%d0%bf%d0%be%d1%80%d0%bd%d0%be%d1%84%d0%b8%d0%bb%d1%8c%d0%bc%d1%8b-%d0%ba%d0%b0%d0%ba-%d0%b2-%d0%bf%d0%be%d1%81%d0%bb%d0%b5%d0%b4%d0%bd%d0%b8%d0%b8-%d1%80%d0%b0%d0%b7.mp3')]), Track(author='Захар Май', title='Нахуй!', url='https://musify.club/track/dl/1421811/%d0%b7%d0%b0%d1%85%d0%b0%d1%80-%d0%bc%d0%b0%d0%b8-%d0%bd%d0%b0%d1%85%d1%83%d0%b8.mp3', fuzzy_matches=[]), Track(author='Зимовье Зверей', title='Джин И Тоник', url='https://musify.club/track/dl/3245629/%d0%b7%d0%b8%d0%bc%d0%be%d0%b2%d1%8c%d0%b5-%d0%b7%d0%b2%d0%b5%d1%80%d0%b5%d0%b8-%d0%b4%d0%b6%d0%b8%d0%bd-%d0%b8-%d1%82%d0%be%d0%bd%d0%b8%d0%ba.mp3', fuzzy_matches=[]), Track(author='Драгни', title='Не парься!', url='', fuzzy_matches=[FuzzyTrack(author='Башаков', title='Не Парься', url='https://musify.club/track/dl/3415278/%d0%b1%d0%b0%d1%88%d0%b0%d0%ba%d0%be%d0%b2-%d0%bd%d0%b5-%d0%bf%d0%b0%d1%80%d1%8c%d1%81%d1%8f.mp3'), FuzzyTrack(author='Механизм', title='Не Парься!', url='https://musify.club/track/dl/7247954/%d0%bc%d0%b5%d1%85%d0%b0%d0%bd%d0%b8%d0%b7%d0%bc-%d0%bd%d0%b5-%d0%bf%d0%b0%d1%80%d1%8c%d1%81%d1%8f.mp3')]), Track(author='Princesse Angine', title='Фантастический Вальс', url='https://musify.club/track/dl/15045185/princesse-angine-%d1%84%d0%b0%d0%bd%d1%82%d0%b0%d1%81%d1%82%d0%b8%d1%87%d0%b5%d1%81%d0%ba%d0%b8%d0%b8-%d0%b2%d0%b0%d0%bb%d1%8c%d1%81.mp3', fuzzy_matches=[]), Track(author='Nodahsa', title='Я никогда не стану феминисткой', url='', fuzzy_matches=[]), Track(author='GALAGA', title='Супер Марио', url='', fuzzy_matches=[FuzzyTrack(author='Радиоактивный Покемон', title='Супер Марио (rock version)', url='https://musify.club/track/dl/16186313/%d1%80%d0%b0%d0%b4%d0%b8%d0%be%d0%b0%d0%ba%d1%82%d0%b8%d0%b2%d0%bd%d1%8b%d0%b8-%d0%bf%d0%be%d0%ba%d0%b5%d0%bc%d0%be%d0%bd-%d1%81%d1%83%d0%bf%d0%b5%d1%80-%d0%bc%d0%b0%d1%80%d0%b8%d0%be-rock-version.mp3'), FuzzyTrack(author='Марион', title='Супермаркет', url='https://musify.club/track/dl/5128590/%d0%bc%d0%b0%d1%80%d0%b8%d0%be%d0%bd-%d1%81%d1%83%d0%bf%d0%b5%d1%80%d0%bc%d0%b0%d1%80%d0%ba%d0%b5%d1%82.mp3')]), Track(author='БоБРы', title='Бальник', url='', fuzzy_matches=[]), Track(author='ANAZED', title='И я', url='', fuzzy_matches=[FuzzyTrack(author='Лариса Черникова', title='И ты и я, и я и ты', url='https://musify.club/track/dl/1532653/%d0%bb%d0%b0%d1%80%d0%b8%d1%81%d0%b0-%d1%87%d0%b5%d1%80%d0%bd%d0%b8%d0%ba%d0%be%d0%b2%d0%b0-%d0%b8-%d1%82%d1%8b-%d0%b8-%d1%8f-%d0%b8-%d1%8f-%d0%b8-%d1%82%d1%8b.mp3'), FuzzyTrack(author='Умка', title='Я И Я', url='https://musify.club/track/dl/11262259/%d1%83%d0%bc%d0%ba%d0%b0-%d1%8f-%d0%b8-%d1%8f.mp3')]), Track(author='XXX $ Горы', title='Барышни', url='', fuzzy_matches=[]), Track(author='Princesse Angine', title='Не Потянешь', url='https://musify.club/track/dl/9522870/princesse-angine-%d0%bd%d0%b5-%d0%bf%d0%be%d1%82%d1%8f%d0%bd%d0%b5%d1%88%d1%8c.mp3', fuzzy_matches=[]), Track(author='Tardigrade Inferno', title='We Are Number One (Lazy Town cover)', url='https://musify.club/track/dl/10492993/tardigrade-inferno-we-are-number-one-lazy-town-cover.mp3', fuzzy_matches=[]), Track(author='The Kills', title='Doing It To Death', url='https://musify.club/track/dl/6256721/the-kills-doing-it-to-death.mp3', fuzzy_matches=[]), Track(author='Odnono', title='Спасибо', url='', fuzzy_matches=[]), Track(author='Moon Hooch', title='Acid Mountain', url='', fuzzy_matches=[FuzzyTrack(author='Moon Hooch', title='Mountain Lion', url='https://musify.club/track/dl/7318094/moon-hooch-mountain-lion.mp3'), FuzzyTrack(author='Moon Hooch', title='Mountain Song', url='https://musify.club/track/dl/5914894/moon-hooch-mountain-song.mp3')]), Track(author='Антитіла', title='Бери Своє', url='https://musify.club/track/dl/1895231/%d0%b0%d0%bd%d1%82%d0%b8%d1%82i%d0%bb%d0%b0-%d0%b1%d0%b5%d1%80%d0%b8-%d1%81%d0%b2%d0%bee.mp3', fuzzy_matches=[]), Track(author='Coockoo', title="I Can't Remember", url='https://musify.club/track/dl/6849707/coockoo-i-cant-remember.mp3', fuzzy_matches=[]), Track(author='Le Tigre', title='Deceptacon', url='https://musify.club/track/dl/684537/le-tigre-deceptacon.mp3', fuzzy_matches=[]), Track(author='Cut Chemist', title="What's The Altitude", url='https://musify.club/track/dl/2515228/cut-chemist-whats-the-altitude.mp3', fuzzy_matches=[]), Track(author='Заточка', title='В Тюрьму Нельзя Feat. Артур Беркут', url='https://musify.club/track/dl/17197714/%d0%b7%d0%b0%d1%82%d0%be%d1%87%d0%ba%d0%b0-%d0%b2-%d1%82%d1%8e%d1%80%d1%8c%d0%bc%d1%83-%d0%bd%d0%b5%d0%bb%d1%8c%d0%b7%d1%8f-feat-%d0%b0%d1%80%d1%82%d1%83%d1%80-%d0%b1%d0%b5%d1%80%d0%ba%d1%83%d1%82.mp3', fuzzy_matches=[]), Track(author='Карандаш', title='Hellp', url='', fuzzy_matches=[])]


tr = Track(author='Don McLean', title='Don Mclean - American Pie')

# play()
fuzzy_matches(test_tracks)