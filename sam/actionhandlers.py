from .weather import weather
from . import music


class ActionHandler:
    """
    A meta-class that is handles the various action types
    Each action type has its own specific functionality, which is captured in the execute_action function
    """

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
        self.action = action
        self.parameters = parameters
        self.contexts = contexts
        try:
            self.super_action, self.sub_action, self.specific_action = self.action.split('.')
        except ValueError:
            try:
                self.super_action, self.sub_action = self.action.split('.'), None
            except ValueError:
                self.super_action = self.action, None

    def execute_action(self):
        res = None
        if self.sub_action is not None:
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


class MusicActionHandler:
    action = ''
    parameters = ''
    contexts = ''
    super_action, sub_action, specific_action = '', '', ''

    def __init__(self, action, parameters, contexts):
        self.action = action
        self.parameters = parameters
        self.contexts = contexts
        my_list = []
        for _ in self.action.split('.'):
            my_list.append(_)
        super_action = my_list[0]
        self.super_action = super_action
        try:
            sub_action = my_list[1]
            self.sub_action = sub_action
        except IndexError:
            sub_action = ''
        try:
            specific_action = my_list[2]
            self.specific_action = specific_action
        except IndexError:
            specific_action = ''

    def execute_action(self):
        # my_list = []
        # for _ in self.action.split('.'):
        #     my_list.append(_)
        # super_action = my_list[0]
        # self.super_action = super_action
        # try:
        #     sub_action = my_list[1]
        #     self.sub_action = sub_action
        # except IndexError:
        #     sub_action = ''
        # try:
        #     specific_action = my_list[2]
        #     self.specific_action = specific_action
        # except IndexError:
        #     specific_action = ''
        self._parse_parameters()
        if self.sub_action is not None:
            if self.sub_action == 'player_control':
                res = self.player_control()
            elif self.sub_action == 'play':
                res = self.play()
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
        pass

    def play(self):
        if self.artist:
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
        if self.specific_action == 'current_song':
            res = music.music()
        elif self.specific_action == 'skip_forward':
            res = music.skip_forward()
        return res
