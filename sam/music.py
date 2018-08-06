from . import spotify_api_wrapper

NOT_IMPLEMENTED = 'Not implemented yet!'


def get_artist_uri(artist):
    """
    Return artist URI for artist
    """
    return NOT_IMPLEMENTED


def get_album_uri(album):
    """
    Return album URI for album
    """
    return


def get_song_uri(track):
    """
    Return song URI for some song(parameter)
    """
    return NOT_IMPLEMENTED


def get_playlist_uri(playlist):
    """
    Return playlist uri for playlist
    """
    return NOT_IMPLEMENTED


def play_artist(artist, device=''):
    """
    Play artist
    """
    return NOT_IMPLEMENTED


def play_album(album, device=''):
    """
    Play album
    """
    return NOT_IMPLEMENTED


def play_playlist(playlist, device=''):
    """
    Play playlist
    """
    return NOT_IMPLEMENTED


def play_song_of_artist(song, artist):
    """
    Play song of some artist
    """
    return NOT_IMPLEMENTED


def play_song(song):
    """
    Play song(parameter) on spotify
    """
    return NOT_IMPLEMENTED


def search_song_data(song):
    """
    Retrieve spotify data for some song
    """
    return NOT_IMPLEMENTED


def play_artist_on_device(artist, device):
    """
    Play specific artist on specific device
    """
    return NOT_IMPLEMENTED


def play_album_on_device(album, device):
    """
    Play specified album on specified device
    """
    return NOT_IMPLEMENTED


def play_playlist_on_device(playlist, device):
    """
    Play specified playlist on specified device
    """
    return NOT_IMPLEMENTED


def add_current_song_to_playlist(playlist):
    """
    Adds currently playing song to specified playlist
    """
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


def unpause(uri=''):
    """
    Unpause
    """
    return 'Unpaused music'


def unpause_on_device(music_thing, uri='', input_device='kuba-pc'):
    """
    Unpause on device
    """
    return 'Unpaused music on {}'.format(input_device)


def skip():
    """
    Skip currently playing song
    """
    return 'Skipping'


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