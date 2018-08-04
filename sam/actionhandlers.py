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

    def execute_action(self):
        pass


class WeatherActionHandler(ActionHandler):
    """
    WeatherActionHandler handles actions that are of the weather type
    """

    def __init__(self, action, parameters, contexts):
        self.action = action
        self.parameters = parameters
        self.contexts = contexts

    def execute_action(self):
        action = self.action[8:]
        if action.startswith("followup"):
            action = self.action[9:]
            date_time, date_, location = self._parse_contexts()
            response = self._create_res(date_time, date_, location, action=action)
        else:
            date_time, date_, location = self._parse_parameters()
            response = self._create_res(date_time, date_, location)
        return response

    def _parse_contexts(self):
        for context in self.contexts:
            if context['name'].endswith('weather'):
                date_time = context['parameters'].get('date-time', None)
                date_ = context['parameters'].get('date', None)
                location = context['parameters'].get('location', None)
                if isinstance(location, dict):
                    location = location['city']
                break
        return date_time, date_, location

    def _parse_parameters(self):
        date_time = self.parameters.get('date-time', None)
        date_ = self.parameters.get('date', None)
        location = self.parameters.get('location', None)
        if isinstance(location, dict):
            location = location['city']
        return date_time, date_, location

    @staticmethod
    def _create_res(date_time, date_,  location, action=None):
        """
        Generate a response for a generic weather request
        :param date_time: The time for the weather
        :param location: The location for the weather
        :param action: The dialogflow defined action (possible that it was modified)
        """
        res = weather(date_time, date_, location)
        return res
