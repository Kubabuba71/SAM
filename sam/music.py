from . import spotify_api_wrapper
from .constants import NOT_IMPLEMENTED
from .exceptions import InvalidDataFormat
from .utils import normalize_volume_value


def play_artist(artist, device=None):
    """
    Play artist
    """
    res = spotify_api_wrapper.play(artist, type_='artist')
    if res.status_code != 204:
        return res.text
    else:
        if isinstance(artist, list):
            artist = artist[0]

        return f'Playing {artist}'


def play_album(album, device=None):
    """
    Play album
    """
    spotify_api_wrapper.play(album, type_='album')
    return f'Playing {album}'


def play_playlist(playlist, device=None):
    """
    Play playlist
    """
    spotify_api_wrapper.play(playlist, type_='playlist')
    return f'Playing {playlist}'


def play_song_of_artist(song, artist, device=None):
    """
    Play song of some artist
    """
    spotify_api_wrapper.play([song, artist], type_='song_artist')
    return f'Playing {format} by {artist}'


def play_song(song):
    """
    Play song on spotify
    """
    spotify_api_wrapper.play(song, type_='track')
    return f'Playing {song}'


def play_artist_on_device(artist, device):
    """
    Play specific artist on specific device
    """
    # spotify_api_wrapper.play(artist, type_='artist', device=device)
    # return 'Playing {} on {}'.format(artist, device)
    return NOT_IMPLEMENTED


def add_current_song_to_playlist(playlist):
    """
    Adds currently playing song to specified playlist
    """
    # spotify_api_wrapper.add_to_playlist(playlist)
    # return 'Added current song to the {} playlist'.format(playlist)
    return NOT_IMPLEMENTED


def get_devices():
    """
    Return currently connected devices
    """
    return NOT_IMPLEMENTED


def playback_state():
    """
    Return current playback state
    """
    return NOT_IMPLEMENTED


def current_song():
    """
    Return artist and name of current song
    """
    json_data = spotify_api_wrapper.currently_playing().json()
    artist = json_data['item']['artists'][0]['name']
    song_name = json_data['item']['name']
    return f'{song_name} by {artist}'


def pause(device=None):
    """
    Pause on device, if specified
    """
    return NOT_IMPLEMENTED


def unpause(uri=None, device=None):
    """
    Unpause playback

    :param uri: Optional Spotify URI to play. If not specified, playback is simply resumed
    :param device: Optional device on which the uri should be played/playback should be resumed
    """
    # return 'Unpaused music'
    return NOT_IMPLEMENTED


def skip_forward():
    """
    Skip the currently playing song
    """
    res = spotify_api_wrapper.skip_forward()
    if res.status_code < 200 or res.status_code > 299:
        return res.text
    return 'Skipping current song'


def unskip():
    """"
    Unskip the currently playing song
    """
    # return 'Playing previous track'
    return NOT_IMPLEMENTED


def repeat(mode='track'):
    """
    Turn on/off repeat
    :param mode: Determines what repeat mode is used. By default, it repeats the current track.
    """
    # return f'Repeat turned on with mode: {mode}'
    return NOT_IMPLEMENTED


def volume_increase(volume_amount=10):
    """
    Increase Spotify volume by '''volume_amount'''

    :param volume_amount: By how much should volume be increased
    """
    volume_amount = normalize_volume_value(volume_amount)
    current_volume_percent = spotify_api_wrapper.current_volume()
    if current_volume_percent == 100:
        return 'At max volume'
    new_volume_percent = current_volume_percent + volume_amount
    if new_volume_percent > 100:
        new_volume_percent = 100
    elif new_volume_percent < 0:
        new_volume_percent = 0
    res = spotify_api_wrapper.set_volume(new_volume_percent)
    if res.status_code < 200 or res.status_code > 299:
        return res.text
    return f'Increased volume by {volume_amount}'


def volume_decrease(volume_amount=10):
    """
    Decrease Spotify volume by '''volume_amount'''

    :param volume_amount: By how much should volume be decreased
    """
    volume_amount = normalize_volume_value(volume_amount)
    current_volume_percent = spotify_api_wrapper.current_volume()
    if current_volume_percent == 100:
        return 'At max volume'
    new_volume_percent = current_volume_percent - volume_amount
    if new_volume_percent > 100:
        new_volume_percent = 100
    elif new_volume_percent < 0:
        new_volume_percent = 0
    res = spotify_api_wrapper.set_volume(new_volume_percent)
    if res.status_code < 200 or res.status_code > 299:
        return res.text
    return f'Lowered the volume by {volume_amount}'


def shuffle(shuffle_state=False):
    """
    Turn on/off shuffle
    """
    # return f'Shuffle state set to: {shuffle_state}'
    return NOT_IMPLEMENTED


def transfer_to_device(input_device):
    """
    Transfer current song to specified device
    """
    # return f'Music playback transfered to {input_device}'
    return NOT_IMPLEMENTED


def music_action(query_result: dict):
    """
    Perform a music action

    query_result_example = {
      "action": "music.play",
      "parameters": {
        "album": "Damn",
      }
    }
    """
    if 'queryResult' in query_result:
        query_result = query_result['queryResult']
    action = query_result.get('action').split('.')[1]

    parameters = query_result.get('parameters')
    artist = parameters.get('artist', None)
    album = parameters.get('album', None)
    song = parameters.get('song', None)
    playlist = parameters.get('playlist', None)
    device = parameters.get('device', None)
    repeat_mode = parameters.get('repeat', None)
    uri = parameters.get('uri', None)
    shuffle_state = parameters.get('shuffle', None)
    volume_amount = parameters.get('percentage', None)

    if not action:
        raise InvalidDataFormat('No action was provided')

    if action == 'play':
        if artist:
            if song:
                res = play_song_of_artist(song, artist, device=device)
            else:
                res = play_artist(artist, device)
        elif album:
            res = play_album(album, device)
        elif playlist:
            res = play_playlist(playlist, device)
        else:
            raise InvalidDataFormat('No artist/album/song/playlist was specified')
    elif action == "add_playlist":
        res = add_current_song_to_playlist(playlist)
    elif action == "current_song":
        res = current_song()
    elif action == "pause":
        res = pause(device)
    elif action == "repeat":
        res = repeat(repeat_mode)
    elif action == "resume":
        res = unpause(uri, device)
    elif action == "shuffle":
        res = shuffle(shuffle_state)
    elif action == "skip_backward":
        res = unskip()
    elif action == "skip_forward":
        res = skip_forward()
    elif action == "stop":
        res = pause(device)
    elif action == 'transfer':
        res = transfer_to_device(device)
    elif action == "volume_decrease":
        res = volume_decrease(volume_amount)
    elif action == "volume_increase":
        res = volume_increase(volume_amount)
    else:
        raise InvalidDataFormat(f'Specified action is invalid: {action}')
    return res
