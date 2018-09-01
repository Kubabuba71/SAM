from . import music
from .exceptions import InvalidDataFormat
from .utils import logged, parse_action
from .weather import weather


class ActionHandler:
    """
    A meta-class that is handles the various action types
    Each action type has its own specific functionality, which is captured in the execute_action function
    """
    def __init__(self, action, parameters, contexts):
        self.action = action
        self.parameters = parameters
        self.contexts = contexts
        self.action_components = self.action.split('.')
        self.super_action, self.sub_action, self.specific_action = parse_action(self.action)

    @logged
    def execute_action(self):
        """
        Execute the expected functionality of the specified action
        Example: action == weather, return weather information, for the date passed in parameters/contexts
        """
        pass


class WeatherActionHandler(ActionHandler):
    """
    WeatherActionHandler handles actions that are of the weather type
    """

    def __init__(self, action, parameters, contexts):
        super().__init__(action, parameters, contexts)

    @logged
    def execute_action(self):
        res = None
        if self.sub_action:
            if self.sub_action.startswith("followup"):
                self._parse_contexts()
                res = self._create_res()
        else:
            self._parse_parameters()
            res = self._create_res()

        return res or 'Weather action not implemented yet'

    def _parse_contexts(self):
        for context in self.contexts:
            if context['name'].endswith('weather'):
                self.date_time = context['parameters'].get('date-time', None)
                self.date_ = context['parameters'].get('date', None)
                self.location = context['parameters'].get('location', None)
                if isinstance(self.location, dict):
                    self.location = self.location['city']
                return

    def _parse_parameters(self):
        self.date_time = self.parameters.get('date-time', None)
        self.date_ = self.parameters.get('date', None)
        self.location = self.parameters.get('location', None)
        if isinstance(self.location, dict):
            self.location = self.location['city']

    def _create_res(self):
        """
        Generate a response for a generic weather request
        """
        res = weather(self.date_time, self.date_, self.location)
        return res


class MusicActionHandler(ActionHandler):

    def __init__(self, action, parameters, contexts):
        super().__init__(action, parameters, contexts)

    @logged
    def execute_action(self):
        self._parse_parameters()
        if self.sub_action:
            if self.sub_action == 'player_control':
                res = self.player_control()
            elif self.sub_action == 'play':
                res = self.play()
            elif self.sub_action == 'device':
                res = self.device()
            else:
                raise InvalidDataFormat('The specified action is invalid: {self.action}')
        else:
            res = 'Not implemented yet'
        return res

    def _parse_contexts(self):
        pass

    def _parse_parameters(self):
        self.artist = self.parameters.get('artist', None)
        self.album = self.parameters.get('album', None)
        self.song = self.parameters.get('song', None)
        self.playlist = self.parameters.get('playlist', None)
        self.sort = self.parameters.get('sort', None)
        self.shuffle = self.parameters.get('shuffle', False)
        self.volume = self.parameters.get('percentage', 10)
        self.device = self.parameters.get('device', None)

    def play(self):
        if self.artist:
            if self.song:
                res = music.play_song_of_artist(self.song, self.artist)
            else:
                res = music.play_artist(self.artist)
        elif self.album:
            res = music.play_album(self.album)
        elif self.song:
            res = music.play_song(self.song)
        elif self.playlist:
            res = music.play_playlist(self.playlist)
        else:
            res = 'Music action not implemented yet'
        return res

    def player_control(self):
        if self.specific_action == 'add_playlist':
            res = music.add_current_song_to_playlist()
        elif self.specific_action == 'current_song':
            res = music.current_song()
        elif self.specific_action == 'pause':
            res = music.pause()
        elif self.specific_action == 'repeat':
            res = music.repeat()
        elif self.specific_action == 'resume':
            res = music.unpause()
        elif self.specific_action == 'shuffle':
            res = music.shuffle(self.shuffle)
        elif self.specific_action == 'skip_backward':
            res = music.unskip()
        elif self.specific_action == 'skip_forward'\
                or self.specific_action == 'skip_forward_followup':
            res = music.skip_forward()
        elif self.specific_action == 'stop':
            res = music.pause()
        elif self.specific_action == 'volume_increase':
            res = music.volume_increase(self.volume)
        elif self.specific_action == 'volume_decrease':
            res = music.volume_lower(self.volume)
        else:
            raise InvalidDataFormat(f'Specified action is not supported by SAM: {self.action}')

        return res

    def device(self):
        if self.specific_action == 'play':
            if self.artist:
                if self.song:
                    res = music.play_song_of_artist_on_device(self.song, self.artist, self.device)
                else:
                    res = music.play_artist_on_device(self.artist, self.device)
            elif self.album:
                res = music.play_album_on_device(self.album, self.device)
            elif self.song:
                res = music.play_song_on_device(self.song, self.device)
            elif self.playlist:
                res = music.play_playlist_on_device(self.playlist, self.device)
            else:
                raise InvalidDataFormat(f'Specified action is not supported by SAM: {self.action}')
        else:
            raise InvalidDataFormat(f'Specified action is not supported by SAM: {self.action}')

        return res
