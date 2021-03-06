from ..exceptions import InvalidDataFormatError, InvalidDataValueError
from ..utils import normalize_volume_value
from ..wrappers import spotify


def play(artist=None, song=None, album=None, playlist=None, device: dict=None):
    if artist:
        if song:
            res = play_song_of_artist(song, artist, device=device)
        else:
            res = play_artist(artist, device=device)
    elif album:
        res = play_album(album, device=device)
    elif playlist:
        res = play_playlist(playlist, device=device)
    elif song:
        res = play_song(song, device=device)
    else:
        raise InvalidDataFormatError('No artist/album/song/playlist was specified')
    return res


def play_artist(artist: str, device: str=None):
    """
    Play ```artist```
    :param artist: The name of the ```artist``` to play
    :param device:  The device on which the artist should be played on.
    :type device:   Name of the device to play on
    """
    spotify.play(artist, type_='artist', device=device)
    if isinstance(artist, list):
        artist = artist[0]

    return f'Playing {artist}'


def play_album(album: str, device: "str dict"=None):
    """
    Play ```album```
    :param album:   The name of the ```album``` to play
    :param device:  Name of the device to play on
    """
    spotify.play(album, type_='album', device=device)
    return f'Playing {album}'


def play_playlist(playlist, device: "str dict"=None):
    """
    Play ```playlist```
    :param playlist:    The name of the ```playlist``` to play
    :param device:      Name of the device to play on
    """
    spotify.play(playlist, type_='playlist', device=device)
    return f'Playing {playlist}'


def play_song_of_artist(song: str, artist: str, device: "str dict"=None):
    """
    Play song of some artist
    :param song:    The name of the ```song``` to play
    :param artist:  The name of the ```artist``` of the song
    :param device:  Name of the device to play on
    """
    spotify.play([song, artist], type_='song_artist', device=device)
    return f'Playing {format} by {artist}'


def play_song(song, device: "str dict"=None):
    """
    Play ```song```
    :param song:    The ```song``` to play
    :param device:  Name of the device to play on
    """
    spotify.play(song, type_='track', device=device)
    return f'Playing {song}'


def add_current_song_to_playlist(playlist: str):
    """
    Adds currently playing song to ```playlist```
    :param playlist: The name of the ```playlist``` to which the current song should be added to.
    """
    if playlist is None:
        raise InvalidDataFormatError('playlist parameter not found in request body')
    song_uri = spotify.currently_playing().json()['item']['uri']
    playlist_id = spotify.get_playlist_uri(playlist).split(':')[-1]
    spotify.add_to_playlist(song_uri, playlist_id)
    current_song_summary = current_song()
    return f'Added {current_song_summary} to {playlist} playlist'


def get_active_device() -> dict:
    """
    Return a Device Object of the currently active device
    :return:    Device Object from the Spotify API of the currently active device
    """
    return spotify.current_playback_state().json()['device']


def current_song():
    """
    Get current song_name and artist, as a nice ```str``` representation
    """
    json_data = spotify.currently_playing().json()
    artist = json_data['item']['artists'][0]['name']
    song_name = json_data['item']['name']
    return f'{song_name} by {artist}'


def pause():
    """
    Pause music playback on the currently active device
    """
    spotify.pause()
    return 'Paused music playback'


def unpause():
    """
    Un-pause music playback on the currently active device
    """
    spotify.unpause()
    device_name = get_active_device()['name']
    return f'Unpaused music playback on {device_name}'


def skip_forward():
    """
    Skip the currently playing song
    """
    spotify.skip_forward()
    return 'Skipping current song'


def unskip():
    """"
    Unskip the currently playing song
    """
    spotify.unskip()
    return 'Playing previous track'


def repeat(mode='track'):
    """
    Turn on/off repeat
    :param mode:    Determines what repeat mode is used. By default, it repeats the current track.
                    Valid values: 'track', 'context' or 'off'
    """
    spotify.repeat(mode)
    return f'Repeat changed to {mode} mode'


def volume_increase(volume_amount=10):
    """
    Increase Spotify volume by '''volume_amount'''

    :param volume_amount:   By how much should volume be increased
    """
    volume_amount = normalize_volume_value(volume_amount)
    current_volume_percent = spotify.current_volume()
    if current_volume_percent == 100:
        return 'At max volume'
    new_volume_percent = current_volume_percent + volume_amount
    if new_volume_percent > 100:
        new_volume_percent = 100
    elif new_volume_percent < 0:
        new_volume_percent = 0
    spotify.set_volume(new_volume_percent)
    return f'Increased volume by {volume_amount}'


def volume_decrease(volume_amount=10):
    """
    Decrease Spotify volume by '''volume_amount'''

    :param volume_amount:   By how much should volume be decreased
    """
    volume_amount = normalize_volume_value(volume_amount)
    current_volume_percent = spotify.current_volume()
    if current_volume_percent == 0:
        return 'At min volume'
    new_volume_percent = current_volume_percent - volume_amount
    if new_volume_percent > 100:
        new_volume_percent = 100
    elif new_volume_percent < 0:
        new_volume_percent = 0
    spotify.set_volume(new_volume_percent)
    return f'Lowered the volume by {volume_amount}'


def shuffle(shuffle_state=False):
    """
    Turn on/off shuffle
    :param shuffle_state:   Whether shuffle should be turned on/off
    :type shuffle_state:    bool - True  -> turn on shuffle
                                   False -> turn off shuffle
                            str -  'on',  'true'   map to True
                                   'off', 'false' map to False
    """
    if isinstance(shuffle_state, str):
        if shuffle_state == 'on':
            shuffle_state = True
        elif shuffle_state == 'off':
            shuffle_state = False
        else:
            raise InvalidDataValueError(f"shuffle_state value is invalid: {shuffle_state}. "
                                   f"Valid values are: 'on', 'off', true, false")
    spotify.shuffle(shuffle_state)
    return f'Shuffle state set to {shuffle_state}'


def transfer_to_device(device_in: str):
    """
    Transfer current playback to specified device
    :param device_in:   Name of the device to play on
    """
    spotify.transfer_to_device(device_in)
    return f'Music playback transferred to {device_in}'


def music_action(query_result: dict):
    """
    Perform a music action
    :param query_result:    dict -  All information necessary to perform the music_action.
                                    Depending on the action, different key-value pairs are needed.
                                    The below example shows all possible parameters.
                                    Note that not ALL of these are needed, depending on the action.
    e.g.:
    {
        "action": "music.play",
        "parameters": {
            "artist": "Queen",
            "album": "A Night at the Opera",
            "song": "Bohemian Rhapsody",
            "playlist": "Rock",
            "device": "JOHN-PC",
            "repeat_mode": "track",
            "uri": "spotify:track:4u7EnebtmKWzUH433cf5Qv",
            "shuffle_state": "on",
            "volume_amount": "10%"
        }
    }
    """
    if 'queryResult' in query_result:
        query_result = query_result['queryResult']
    action = query_result.get('action').split('.')[1]

    if not action:
        raise InvalidDataFormatError('No specific music action was provided.')

    parameters = query_result.get('parameters', None)

    # TODO: Some parameters have to be set to default, even if not specified
    if parameters:
        artist = parameters.get('artist', None)
        album = parameters.get('album', None)
        song = parameters.get('song', None)
        playlist = parameters.get('playlist', None)
        device = parameters.get('device', None)
        repeat_mode = parameters.get('repeat_mode', None)
        shuffle_state = parameters.get('shuffle', None)

    # These parameters need to be set to None at the very least
    volume_amount = parameters.get('percentage', 10)

    if action == 'play':
        res = play(artist=artist, song=song, album=album, playlist=playlist, device=device)
    elif action == 'add_playlist':
        res = add_current_song_to_playlist(playlist)
    elif action == 'current_song':
        res = current_song()
    elif action == 'pause':
        res = pause()
    elif action == 'repeat':
        res = repeat(repeat_mode)
    elif action == 'unpause':
        res = unpause()
    elif action == 'shuffle':
        res = shuffle(shuffle_state)
    elif action == 'skip_backward':
        res = unskip()
    elif action == 'skip_forward':
        res = skip_forward()
    elif action == 'transfer':
        res = transfer_to_device(device)
    elif action == 'volume_decrease':
        res = volume_decrease(volume_amount)
    elif action == 'volume_increase':
        res = volume_increase(volume_amount)
    else:
        raise InvalidDataFormatError(f'Specified action is invalid: {action}')
    return res
