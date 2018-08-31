import pytest
import os
import platform
import json


if not os.getcwd().endswith('tests'):
    fixtures_dir = os.path.abspath(os.path.join(os.getcwd(), 'tests'))
    fixtures_dir = os.path.abspath(os.path.join(fixtures_dir, 'fixtures'))
else:
    fixtures_dir = os.path.abspath(os.path.join(os.getcwd(), 'fixtures'))


def open_file(param):
    with open(os.path.abspath(os.path.join(fixtures_dir, param))) as file_:
        return json.load(file_)


@pytest.fixture
def music_play_album():
    return open_file('music-play_album.json')


@pytest.fixture
def music_play_artist():
    return open_file('music-play_artist.json')


@pytest.fixture
def music_play_song():
    return open_file('music-play_song.json')


@pytest.fixture
def music_play_control_current_song():
    return open_file('music_play_control_current_song.json')


@pytest.fixture
def music_play_control_skip_forward():
    return open_file('music_play_control_skip_forward.json')


@pytest.fixture
def weather_current():
    return open_file('weather_current.json')


@pytest.fixture
def weather_current_location():
    return open_file('weather_current_location.json')


@pytest.fixture
def weather_day():
    return open_file('weather_day.json')


@pytest.fixture
def weather_followup_location():
    return open_file('weather_followup_location.json')


@pytest.fixture
def weather_period():
    return open_file('weather_period.json')


@pytest.fixture()
def request_handler():
    from sam.requesthandlers import RequestHandler
    return RequestHandler


@pytest.fixture()
def now_str():
    from datetime import datetime
    now = datetime.utcnow()
    now = datetime(now.year,
                   now.month,
                   now.day,
                   now.hour,
                   now.minute,
                   now.second)
    now_str = now.isoformat() + '+02:00'
    return now_str


@pytest.fixture()
def load_dotenv():
    if 'Windows' in platform.system():
        with open('.env') as file_:
            for line in file_:
                key, value = line.split('=')
                os.environ[key] = value.strip()
