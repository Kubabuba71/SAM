from . import spotify_api_wrapper
from .utils import logged
from .constants import NOT_IMPLEMENTED
from .utils import normalize_volume_value


@logged
def play_artist(artist, device=None):
    """
    Play artist
    """
    res = spotify_api_wrapper.play(artist, type_='artist')
    if isinstance(artist, list):
        artist = artist[0]

    return f'Playing {artist}'


@logged
def play_album(album, device=None):
    """
    Play album
    """
    spotify_api_wrapper.play(album, type_='album')
    return f'Playing {album}'


@logged
def play_playlist(playlist, device=None):
    """
    Play playlist
    """
    spotify_api_wrapper.play(playlist, type_='playlist')
    return f'Playing {playlist}'


@logged
def play_song_of_artist(song, artist):
    """
    Play song of some artist
    """
    spotify_api_wrapper.play([song, artist], type_='song_artist')
    return f'Playing {format} by {artist}'


@logged
def play_song(song):
    """
    Play song on spotify
    """
    spotify_api_wrapper.play(song, type_='track')
    return f'Playing {song}'


@logged
def play_artist_on_device(artist, device):
    """
    Play specific artist on specific device
    """
    # spotify_api_wrapper.play(artist, type_='artist', device=device)
    # return 'Playing {} on {}'.format(artist, device)
    return NOT_IMPLEMENTED


@logged
def play_album_on_device(album, device):
    """
    Play specified album on specified device
    """
    # spotify_api_wrapper.play(album, type_='album', device=device)
    # return 'Playing {} on {}'.format(album, device)
    return NOT_IMPLEMENTED


@logged
def play_playlist_on_device(playlist, device):
    """
    Play specified playlist on specified device
    """
    # spotify_api_wrapper.play(playlist, type_='playlist', device=device)
    # return 'Playing {} on {}'.format(playlist, device)
    return NOT_IMPLEMENTED


@logged
def add_current_song_to_playlist(playlist):
    """
    Adds currently playing song to specified playlist
    """
    # spotify_api_wrapper.add_to_playlist(playlist)
    # return 'Added current song to the {} playlist'.format(playlist)
    return NOT_IMPLEMENTED


@logged
def get_playlist_tracks(playlist_id):
    """
    Return tracks of specified playlist
    """
    return NOT_IMPLEMENTED


def get_devices():
    """
    Return currently connected devices
    """
    return NOT_IMPLEMENTED


@logged
def playback_state():
    """
    Return current playback state
    """
    return NOT_IMPLEMENTED


@logged
def current_track_and_artist():
    """
    Return info on current track and artist
    """
    return NOT_IMPLEMENTED


@logged
def current_track():
    """
    Return info on current track
    """
    return NOT_IMPLEMENTED


@logged
def current_artist():
    """
    Return info on current artist
    """
    return NOT_IMPLEMENTED


@logged
def current_album():
    """
    Return info on current album
    """
    return NOT_IMPLEMENTED


@logged
def current_song():
    """
    Return artist and name of current song
    """
    json_data = spotify_api_wrapper.currently_playing().json()
    artist = json_data['item']['artists'][0]['name']
    song_name = json_data['item']['name']
    return f'{song_name} by {artist}'


@logged
def pause(device=None):
    """
    Pause on device, if specified
    """
    return NOT_IMPLEMENTED


@logged
def unpause(uri=None):
    """
    Unpause
    """
    # return 'Unpaused music'
    return NOT_IMPLEMENTED


@logged
def unpause_on_device(music_thing, uri=None, input_device='kuba-pc'):
    """
    Unpause on device
    """
    # return f'Unpaused music on {input_device}'
    return NOT_IMPLEMENTED


@logged
def skip_forward():
    """
    Skip currently playing song
    """
    res = spotify_api_wrapper.skip_forward()
    if res.status_code < 200 or res.status_code > 299:
        return res.text
    return 'Skipping current song'


@logged
def unskip():
    """"
    Unskip currently playing song
    """
    # return 'Playing previous track'
    return NOT_IMPLEMENTED


@logged
def repeat(mode='track'):
    """
    Turn on/off repeat
    """
    # return f'Repeat turned on with mode: {mode}'
    return NOT_IMPLEMENTED


@logged
def volume_increase(volume_amount=10):
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


@logged
def volume_lower(volume_amount=10):
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


@logged
def shuffle(shuffle_state=False):
    """
    Turn on/off shuffle
    """
    # return f'Shuffle state set to: {shuffle_state}'
    return NOT_IMPLEMENTED


@logged
def transfer_to_device(input_device):
    """
    Transfer current song to specified device
    """
    # return f'Music playback transfered to {input_device}'
    return NOT_IMPLEMENTED
