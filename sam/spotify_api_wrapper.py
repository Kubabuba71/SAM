import json

from . import spotify_oauth2_session
from .constants import (NOT_IMPLEMENTED, SPOTIFY_PLAYLISTS_FILE,
                        SPOTIFY_WRAPPER_STR)
from .exceptions import SpotifyPlaylistNotfoundError, InvalidDataType
from .utils import log, now_str

with open(SPOTIFY_PLAYLISTS_FILE) as file_:
    spotify_playlists: dict = json.load(file_)

valid_types = ['artist', 'album', 'track', 'playlist']


def current_playback_state():
    """
    Get information about the user's current playback state, including track, track progress and active device'
    """
    res = spotify_oauth2_session.get('https://api.spotify.com/v1/me/player')
    return res


def currently_playing():
    """
    Get the currently playing information

    :returns: requests.Response
    """
    res = spotify_oauth2_session.get('https://api.spotify.com/v1/me/player/currently-playing')
    return res


def current_volume():
    """
    Get the user's current volume_percent
    """
    return current_playback_state().json()['device']['volume_percent']


def available_devices():
    """
    Get the user's currently available devices
    """
    res = spotify_oauth2_session.get('https://api.spotify.com/v1/me/player/devices')
    return res


def get_device_by_name(device_name_in: str) -> dict:
    """
    Get the device that has name equivalent to ```device_name_in```.
    :returns    dict - Spotify Device Object that has name equivalent to ```device_name```
                None - device_name was not found in the currently available list
    """
    device_name_in = device_name_in.replace(' ', '').replace('-', '').lower()
    devices = available_devices().json()
    for device in devices['devices']:
        device_name = device['name'].replace(' ', '').replace('-', '').lower()
        if device_name == device_name_in \
                or device['id'] == device_name_in:
            return device
    return None


def get_device_object(device_in: "str dict") -> dict:
    """
    Give the ID or Name of a device, return the Spotify Device Object
    :param device_in:   str -> Name or ID of the device in question
                        dict-> Spotify Device Object (in this case,
                        this function acts as a small validation check)
    """
    if isinstance(device_in, str):
        # Have to determine if it is an ID or the name of the device
        devices_json = available_devices().json()
        for device in devices_json['devices']:
            if device['id'] == device_in:
                # device_in is the id of the device

                break
        else:
            # device_in is the name of the device (assumed)
            device = get_device_by_name(device_in)
    elif isinstance(device_in, dict):
        assert 'id' in device_in and 'name' in device_in
        return device_in
    else:
        raise InvalidDataType(f'The type of `device_in` is invalid: '
                              f'{type(device_in).__name__}')
    return device


@property
def oauth2_session():
    return spotify_oauth2_session


def login():
    """
    Generate an authorization url to authorize your app to connect to the Spotify API,
    and access user resources, and return the authorization url
    """
    authorization_url, state = spotify_oauth2_session.authorization_url()
    return authorization_url


def callback(callback_url):
    """
    Fetch an access token, based on the callback_url

    :param callback_url: The callback url returned by the Spotify API,
                         after the user authorized (or denied) access to their account
    """
    spotify_oauth2_session.fetch_token(callback_url)


def token_info():
    """
    Return current token info for the OAuth2Session
    """
    res = spotify_oauth2_session.oauth2_session.token
    return res


def get_uri(input_, type_='track'):
    payload = {
        'q': input_,
        'type': type_
    }
    res = spotify_oauth2_session.get('https://api.spotify.com/v1/search', params=payload)
    return res


def get_playlist_uri(playlist):
    if playlist in spotify_playlists:
        uri = spotify_playlists[playlist]
    else:
        log(f'{now_str()}-DEBUG{SPOTIFY_WRAPPER_STR}: {playlist} playlist not in spotify_playlists.json. '
            f'Connecting to Spotify API')
        json_data = get_uri(playlist, 'playlist').json()
        try:
            uri = json_data['playlists']['items'][0]['uri']
        except IndexError:
            raise SpotifyPlaylistNotfoundError(f'{playlist} playlist not found anywhere. Yikes.')
    return uri


def skip_forward():
    """
    Skip the currently playing song
    """
    res = spotify_oauth2_session.post('https://api.spotify.com/v1/me/player/next')
    return res


def unskip():
    """
    Play the previous song
    """
    res = spotify_oauth2_session.post('https://api.spotify.com/v1/me/player/previous')
    return res


def repeat(mode):
    """
    Set repeat mode to ```mode```
    """
    params = {
        'state': mode
    }
    res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player/repeat', params=params)
    return res


def shuffle(shuffle_mode: bool):
    """
    Set shuffle mode to ```shuffle_mode```
    """
    params = {
        'state': shuffle_mode
    }
    res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player/shuffle', params=params)
    return res


def transfer_to_device(device: "str dict", play_: bool=True):
    """
    Transfer current music playback to ```device_object```
    :param device:      str -> the name or ID of the device
                        dict -> Device Object retrieved from the Spotify API
    :param play_:       True -> ensure playback happens on new device
                        False-> keep the current playback state.
    """
    device_object = get_device_object(device)
    device_id = device_object['id']
    data = {
        'device_ids': [device_id],
        'play': play_
    }
    res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player', json=data)
    return res


def play(value: str, type_: str='artist', device: "str, dict"=None):
    """
    Attempt to play the specified value, based on type_
    :param value: The value to search for and ultimately play (song name, artist name, album name, playlist name)
    :param type_: (song, artist, album, playlist)
    :param device: (from Spotify API)

    :returns: requests.Response
    """
    if type_ not in valid_types:
        raise ValueError('invalid type_ value passed. Valid types: "song", "album", "track", "playlist"')

    params = dict()

    if device:
        # Play on a specific device
        device_object = get_device_object(device)
        device_id = device_object['id']
        params['device_id'] = device_id

    # Play on the currently active device
    if type_ == 'playlist':
        uri = get_playlist_uri(value)
    else:
        json_data = get_uri(value, type_).json()
        if type_ == 'artist':
            uri = json_data['artists']['items'][0]['uri']
        elif type_ == 'album':
            uri = json_data['albums']['items'][0]['uri']
        elif type_ == 'track':
            uri = json_data['tracks']['items'][0]['uri']

    if type_ == 'track':
        # Play a track
        data = {
            'uris': [uri]
        }
        res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player/play',
                                         json=data,
                                         params=params)
    else:
        # Play an artist/album/playlist
        data = {
            'context_uri': uri
        }
        res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player/play',
                                         json=data,
                                         params=params)
    return res


def pause():
    res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player/pause')
    return res


def unpause():
    """
    Un-pause music playback on the currently active device
    """
    res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player/play')
    return res


def set_volume(volume_percent: int=50, device_id: str=None):
    """
    Set the user's volume_percent
    :param volume_percent: The desired volume level
    :param device_id: The id of the device for which the volume is being changed/set
    :returns: requests.Response
    """
    params = {
        'volume_percent': volume_percent
    }
    if device_id:
        params['device_id'] = device_id
    res = spotify_oauth2_session.put('https://api.spotify.com/v1/me/player/volume', params=params)
    return res


def add_to_playlist(song_uri, playlist_id):
    params = {
        'uris': song_uri
    }
    res = spotify_oauth2_session.post(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', params=params)
    return res
