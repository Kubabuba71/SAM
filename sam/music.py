from . import spotify_api_wrapper

NOT_IMPLEMENTED = 'Not implemented yet!'


def play_artist(artist, device=None):
    """
    Play artist
    """
    spotify_api_wrapper.play(artist, type_='artist')
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


def play_song_of_artist(song, artist):
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


def play_album_on_device(album, device):
    """
    Play specified album on specified device
    """
    # spotify_api_wrapper.play(album, type_='album', device=device)
    # return 'Playing {} on {}'.format(album, device)
    return NOT_IMPLEMENTED


def play_playlist_on_device(playlist, device):
    """
    Play specified playlist on specified device
    """
    # spotify_api_wrapper.play(playlist, type_='playlist', device=device)
    # return 'Playing {} on {}'.format(playlist, device)
    return NOT_IMPLEMENTED


def add_current_song_to_playlist(playlist):
    """
    Adds currently playing song to specified playlist
    """
    # spotify_api_wrapper.add_to_playlist(playlist)
    # return 'Added current song to the {} playlist'.format(playlist)
    return NOT_IMPLEMENTED


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


def playback_state():
    """
    Return current playback state
    """
    return NOT_IMPLEMENTED


def current_track_and_artist():
    """
    Return info on current track and artist
    """
    return NOT_IMPLEMENTED


def current_track():
    """
    Return info on current track
    """
    return NOT_IMPLEMENTED


def current_artist():
    """
    Return info on current artist
    """
    return NOT_IMPLEMENTED


def current_album():
    """
    Return info on current album
    """
    return NOT_IMPLEMENTED


def pause(device_id=''):
    """
    Pause on device, if specified
    """
    return NOT_IMPLEMENTED


def unpause(uri=None):
    """
    Unpause
    """
    return 'Unpaused music'


def unpause_on_device(music_thing, uri=None, input_device='kuba-pc'):
    """
    Unpause on device
    """
    return f'Unpaused music on {input_device}'


def skip_forward():
    """
    Skip currently playing song
    """
    spotify_api_wrapper.skip_forward()
    res = 'Skipping current song'
    return res


def unskip():
    """"
    Unskip currently playing song
    """
    return 'Playing previous track'


def repeat(mode='track'):
    """
    Turn on/off repeat
    """
    return f'Repeat turned on with mode: {mode}'


def volume(volume_level=50):
    """
    Change the volume
    """
    return f'Volume set to: {volume_level}'


def shuffle(shuffle_state='false'):
    """
    Turn on/off shuffle
    """
    return f'Shuffle state set to: {shuffle_state}'


def transfer_to_device(input_device):
    """
    Transfer current song to specified device
    """
    return f'Music playback transfered to {input_device}'


def music():
    """

    :return: str
    """
    json_data = spotify_api_wrapper.currently_playing().json()
    artist = json_data['item']['artists'][0]['name']
    song_name = json_data['item']['name']
    return f'{song_name} by {artist}'
