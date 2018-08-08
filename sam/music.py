from . import spotify_api_wrapper

NOT_IMPLEMENTED = 'Not implemented yet!'


def play_artist(artist, device=None):
    """
    Play artist
    """
    spotify_api_wrapper.play(artist, type_='artist')
    return 'Playing {}'.format(artist)


def play_album(album, device=None):
    """
    Play album
    """
    spotify_api_wrapper.play(album, type_='album')
    return 'Playing {}'.format(album)


def play_playlist(playlist, device=None):
    """
    Play playlist
    """
    spotify_api_wrapper.play(playlist, type_='playlist')
    return 'Playing {}'.format(playlist)


def play_song_of_artist(song, artist):
    """
    Play song of some artist
    """
    spotify_api_wrapper.play([song, artist], type_='song_artist')
    return 'Playing {} by {}'.format(song, artist)


def play_song(song):
    """
    Play song(parameter) on spotify
    """
    spotify_api_wrapper.play(song, type_='track')
    return 'Playing {}'.format(song)


def play_artist_on_device(artist, device):
    """
    Play specific artist on specific device
    """
    # spotify_api_wrapper.play(artist, type_='artist', device=device)
    # return 'Playing {} on {}'.format(artist, device)
    return NotImplemented


def play_album_on_device(album, device):
    """
    Play specified album on specified device
    """
    # spotify_api_wrapper.play(album, type_='album', device=device)
    # return 'Playing {} on {}'.format(album, device)
    return NotImplemented


def play_playlist_on_device(playlist, device):
    """
    Play specified playlist on specified device
    """
    # spotify_api_wrapper.play(playlist, type_='playlist', device=device)
    # return 'Playing {} on {}'.format(playlist, device)
    return NotImplemented


def add_current_song_to_playlist(playlist):
    """
    Adds currently playing song to specified playlist
    """
    # spotify_api_wrapper.add_to_playlist(playlist)
    # return 'Added current song to the {} playlist'.format(playlist)
    return NotImplemented


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
    return 'Unpaused music on {}'.format(input_device)


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
    return 'Repeat turned on with mode: {}'.format(mode)


def volume(volume_level=50):
    """
    Change the volume
    """
    return 'Volume set to: {}'.format(volume_level)


def shuffle(shuffle_state='false'):
    """
    Turn on/off shuffle
    """
    return 'Shuffle state set to: {}'.format(shuffle_state)


def transfer_to_device(input_device):
    """
    Transfer current song to specified device
    """
    return 'Music playback transfered to {}'.format(input_device)


def music():
    """

    :return: str
    """
    json_data = spotify_api_wrapper.currently_playing().json()
    artist = json_data['item']['artists'][0]['name']
    song_name = json_data['item']['name']
    return '{} by {}'.format(song_name, artist)
