from .actionhandlers import WeatherActionHandler, MusicActionHandler


class RequestHandler:
    def __init__(self, req):
        self.req = req
        self.action_handler = None
        # self.action = self.req.get("result").get("action")
        self.action = self.req.get('queryResult').get('action')
        # self.parameters = self.req.get("result").get("parameters")
        self.parameters = self.req.get('queryResult').get('parameters')
        # self.contexts = self.req.get("result").get("contexts")
        self.contexts = self.req.get('queryResult').get('outputContexts')
        self.res = None

    def handle_request(self):
        """
        Handles the incoming request, by taking the appropriate action
        :returns: The appropriate json response for the specified action, formatted as a str
        """
        if self.action.startswith("music."):
            # self.action_handler = MusicHandler()
            self.action_handler = MusicActionHandler(self.action, self.parameters, self.contexts)
            pass

        elif self.action.startswith("calendar"):
            # self.action_handler = CalendarHandler()
            pass

        elif self.action.startswith("weather"):
            self.action_handler = WeatherActionHandler(self.action, self.parameters, self.contexts)

        result = 'Not yet implemented' if self.action_handler is None else self.action_handler.execute_action()
        self. res = {'fulfillmentText': result}
        return self.res
