from utils import *
import PySimpleGUI as sg

tracks = [Track(author='Don McLean', title='Don Mclean - American Pie', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/don-mclean-don-mclean-american-pie-18437894'),
          Track(author='Паша Руденко', title='Ебш', fuzzy_matches=[
              Track(author='Паша Руденко', title='Пятница', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/pasha-rudenko-pyatnitsa-13737391'),
              Track(author='Паша Руденко', title='Немой', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/pasha-rudenko-nemoi-10640390')], full_match=False, url=''),
          Track(author='Metallica', title='Nothing Else Matters (Demo)', fuzzy_matches=[
              Track(author='Silenzium', title='Nothing Else Matters (Metallica)', fuzzy_matches=[],
                    full_match=False,
                    url='https://musify.club/track/track/silenzium-nothing-else-matters-metallica-3321400')],
                full_match=True, url='https://musify.club/track/track/metallica-nothing-else-matters-demo-3071685'),
          Track(author='Пневмослон', title='Ебашу как в последний раз', fuzzy_matches=[
              Track(author='Пневмослон', title='Ебашу, Как В Последний Раз', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/pnevmoslon-ebashu-kak-v-poslednii-raz-9303415'),
              Track(author='Порнофильмы', title='Как в последний раз', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/pornofilmi-kak-v-poslednii-raz-6934317')],
                full_match=False, url=''),
          Track(author='Захар Май', title='Нахуй!', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/zahar-mai-nahui-1421811'),
          Track(author='Зимовье Зверей', title='Джин И Тоник', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/zimove-zverei-dzhin-i-tonik-3245629'),
          Track(author='Драгни', title='Не парься!', fuzzy_matches=[
              Track(author='Башаков', title='Не Парься', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/bashakov-ne-parsya-3415278'),
              Track(author='Механизм', title='Не Парься!', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/mehanizm-ne-parsya-7247954')], full_match=False, url=''),
          Track(author='Princesse Angine', title='Фантастический Вальс', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/princesse-angine-fantasticheskii-vals-15045185'),
          Track(author='Nodahsa', title='Я никогда не стану феминисткой', fuzzy_matches=[], full_match=False,
                url=''), Track(author='GALAGA', title='Супер Марио', fuzzy_matches=[
        Track(author='Радиоактивный Покемон', title='Супер Марио (rock version)', fuzzy_matches=[],
              full_match=False,
              url='https://musify.club/track/track/radioaktivnii-pokemon-super-mario-rock-version-16186313'),
        Track(author='Марион', title='Супермаркет', fuzzy_matches=[], full_match=False,
              url='https://musify.club/track/track/marion-supermarket-5128590')], full_match=False, url=''),
          Track(author='БоБРы', title='Бальник', fuzzy_matches=[], full_match=False, url=''),
          Track(author='ANAZED', title='И я', fuzzy_matches=[
              Track(author='Лариса Черникова', title='И ты и я, и я и ты', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/larisa-chernikova-i-ti-i-ya-i-ya-i-ti-1532653'),
              Track(author='Умка', title='Я И Я', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/umka-ya-i-ya-11262259')], full_match=False, url=''),
          Track(author='XXX $ Горы', title='Барышни', fuzzy_matches=[], full_match=False, url=''),
          Track(author='Don McLean', title='Don Mclean - American Pie', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/don-mclean-don-mclean-american-pie-18437894'),
          Track(author='Princesse Angine', title='Не Потянешь', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/princesse-angine-ne-potyanesh-9522870'),
          Track(author='Tardigrade Inferno', title='We Are Number One (Lazy Town cover)', fuzzy_matches=[],
                full_match=True,
                url='https://musify.club/track/track/tardigrade-inferno-we-are-number-one-lazy-town-cover-10492993'),
          Track(author='The Kills', title='Doing It To Death', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/the-kills-doing-it-to-death-6256721'),
          Track(author='Odnono', title='Спасибо', fuzzy_matches=[], full_match=False, url=''),
          Track(author='Moon Hooch', title='Acid Mountain', fuzzy_matches=[
              Track(author='Moon Hooch', title='Mountain Lion', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/moon-hooch-mountain-lion-7318094'),
              Track(author='Moon Hooch', title='Mountain Song', fuzzy_matches=[], full_match=False,
                    url='https://musify.club/track/track/moon-hooch-mountain-song-5914894')], full_match=False,
                url=''), Track(author='Антитіла', title='Бери Своє', fuzzy_matches=[], full_match=True,
                               url='https://musify.club/track/track/antitila-beri-svoe-1895231'),
          Track(author='Coockoo', title="I Can't Remember", fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/coockoo-i-cant-remember-6849707'),
          Track(author='Le Tigre', title='Deceptacon', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/le-tigre-deceptacon-684537'),
          Track(author='Cut Chemist', title="What's The Altitude", fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/cut-chemist-whats-the-altitude-2515228'),
          Track(author='Заточка', title='В Тюрьму Нельзя Feat. Артур Беркут', fuzzy_matches=[], full_match=True,
                url='https://musify.club/track/track/zatochka-v-turmu-nelzya-feat-artur-berkut-17197714'),
          Track(author='Карандаш', title='Hellp', fuzzy_matches=[], full_match=False, url='')]


def full_match(tracks):
    row1 = [[sg.Text(track.author)] for track in tracks if tracks.index(track) % 3 == 0]
    row2 = [[sg.Text(track.author)] for track in tracks if tracks.index(track) % 3 == 1]
    row3 = [[sg.Text(track.author)] for track in tracks if tracks.index(track) % 3 == 2]
    layout = [
        [sg.Column(row1, vertical_alignment='top'), sg.Column(row2, vertical_alignment='top'), sg.Column(row3, vertical_alignment='top')]
    ]
    window = sg.Window('Полное совпадение', layout, resizable=True, )
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
    window.close()

full_match([track for track in tracks if track.full_match])
# row1 = [sg.Text(track.author) for track in tracks if tracks.index(track) % 3 == 0]
# print(row1)