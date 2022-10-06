from utils import *


def test_get_html():
    assert get_html('https://musify.club/').status_code == 200
    assert get_html('musify.club/') is None
    assert get_html('https://muify.club/') is None


def test_musify():
    track = Track('Сплин', 'Выхода нет')
    musify(track)
    assert track.url == 'https://musify.club/track/track/splin-vihoda-net-1738469'
    track = Track('Кошки Jam', 'Солнце(Купи мне гитару)')
    musify(track)
    assert track.full_match is False
