from . import spotify_api_wrapper
from .constants import NOT_IMPLEMENTED
from .exceptions import InvalidDataFormat
from .utils import normalize_volume_value


def play_artist(artist: str, device=None):
    """
    Play ```artist```
    :param artist: The name of the ```artist``` to play
    :param device:  The device on which the artist should be played on.
    :type device:   str - Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                    dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    spotify_api_wrapper.play(artist, type_='artist', device=device)
    if isinstance(artist, list):
        artist = artist[0]

    return f'Playing {artist}'


def play_album(album: str, device: "str dict"=None):
    """
    Play ```album```
    :param album:   The name of the ```album``` to play
    :type album: str
    :param device:  The ```device``` on which the album should be played on.
    :type device:   str - Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                    dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    spotify_api_wrapper.play(album, type_='album', device=device)
    return f'Playing {album}'


def play_playlist(playlist, device=None):
    """
    Play ```playlist```
    :param playlist:    The name of the ```playlist``` to play
    :param device:      The name of the ```device``` on which the ```playlist``` should be played on.
    :type device:       str - Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                        dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    spotify_api_wrapper.play(playlist, type_='playlist', device=device)
    return f'Playing {playlist}'


def play_song_of_artist(song: str, artist: str, device: "str dict"=None):
    """
    Play song of some artist
    :param song:    The name of the ```song``` to play
    :param artist:  The name of the ```artist``` of the song
    :param device:  The ```device``` on which the ```song``` of the ```artist``` should be played on.
    :type device:   str - Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                    dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    spotify_api_wrapper.play([song, artist], type_='song_artist', device=device)
    return f'Playing {format} by {artist}'


def play_song(song, device: "str dict"=None):
    """
    Play ```song```
    :param song:    The ```song``` to play
    :param device:  The ```device``` to which music playback should be transferred to.
    :type device:   str - Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                    dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    spotify_api_wrapper.play(song, type_='track', device=device)
    return f'Playing {song}'


def add_current_song_to_playlist(playlist: str):
    """
    Adds currently playing song to ```playlist```
    :param playlist: The name of the ```playlist``` to which the current song should be added to.
    """
    if playlist is None:
        raise InvalidDataFormat('playlist parameter not found in request body')
    song_uri = spotify_api_wrapper.currently_playing().json()['item']['uri']
    playlist_id = spotify_api_wrapper.get_playlist_uri(playlist).split(':')[-1]
    spotify_api_wrapper.add_to_playlist(song_uri, playlist_id)
    current_song_summary = current_song()
    return f'Added {current_song_summary} to {playlist} playlist'


def get_devices():
    """
    Return currently connected devices
    """
    return NOT_IMPLEMENTED


def current_song():
    """
    Get current song_name and artist, as a nice ```str``` representation
    """
    json_data = spotify_api_wrapper.currently_playing().json()
    artist = json_data['item']['artists'][0]['name']
    song_name = json_data['item']['name']
    return f'{song_name} by {artist}'


def pause(device=None):
    """
    Pause on device, if specified
    :param device:  The device to which music playback should be transferred to.
    :type device:   str - Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                    dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    return NOT_IMPLEMENTED


def unpause(uri=None, device=None):
    """
    Unpause playback

    :param uri:     Optional Spotify URI to play. If not specified, playback is simply resumed
    :param device:  The device on which music playback should be unpaused on.
    :type device:   str - Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                    dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    return NOT_IMPLEMENTED


def skip_forward():
    """
    Skip the currently playing song
    """
    spotify_api_wrapper.skip_forward()
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
    :param mode:    Determines what repeat mode is used. By default, it repeats the current track.
    """
    # return f'Repeat turned on with mode: {mode}'
    return NOT_IMPLEMENTED


def volume_increase(volume_amount=10):
    """
    Increase Spotify volume by '''volume_amount'''

    :param volume_amount:   By how much should volume be increased
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
    spotify_api_wrapper.set_volume(new_volume_percent)
    return f'Increased volume by {volume_amount}'


def volume_decrease(volume_amount=10):
    """
    Decrease Spotify volume by '''volume_amount'''

    :param volume_amount:   By how much should volume be decreased
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
    spotify_api_wrapper.set_volume(new_volume_percent)
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
    # return f'Shuffle state set to: {shuffle_state}'
    return NOT_IMPLEMENTED


def transfer_to_device(device: "str dict"):
    """
    Transfer current song to specified device
    :param device:  The device to which music playback should be transferred to.
    :type device:   str -   Natural Language String of the device e.g.: ```JOHN-PC```.
                            In this case, it depends what name Spotify assigns to the device.
                    dict - Device Object retrieved from the Spotify API
                            e.g.:
                            {
                                "id" : "5fbb3ba6aa454b5534c4ba43a8c7e8e45a63ad0e",
                                "is_active" : false,
                                "is_private_session": true,
                                "is_restricted" : false,
                                "name" : "My fridge",
                                "type" : "Computer",
                                "volume_percent" : 100
                            }
    """
    # return f'Music playback transfered to {indeviceput_device}'
    return NOT_IMPLEMENTED


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

    e.g.:
    {
        "queryResult": {
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
                res = play_artist(artist, device=device)
        elif album:
            res = play_album(album, device=device)
        elif playlist:
            res = play_playlist(playlist, device=device)
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
