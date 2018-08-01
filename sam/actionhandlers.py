from .weather import weather


class ActionHandler:
    """
    A meta-class that is handles the various action types
    Each action type has its own specific functionality, which is encapture in execute_action
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
            date_time, location = self._parse_contexts()
            response = self._create_res(date_time, location, action=action)
        else:
            date_time, location = self._parse_parameters()
            # response = self._create_res(date_time, location)
            response = self._create_res(date_time, location)
        return response

    def _parse_contexts(self):
        for i in range(15):
            if self.contexts[i]['name'] == 'weather':
                date_time = self.contexts[i]['parameters']['date-time']
                location = self.contexts[i]['parameters']['location']
                if isinstance(location, dict):
                    location = location['city']
                break
        return date_time, location

    def _parse_parameters(self):
        date_time = self.parameters.get('date-time')
        location = self.parameters['location']
        if isinstance(location, dict):
            location = location['city']
        return date_time, location

    @staticmethod
    def _create_res(date_time, location, action=None):
        """
        Generate a response for a generic weather request
        :param date_time: The time for the weather
        :param location: The location for the weather
        :param action: The dialogflow defined action (possible that it was modified)
        """
        res = weather(date_time, location)
        return res
