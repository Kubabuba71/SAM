import json


class SamException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        if isinstance(self.payload, str):
            rv = {'payload': self.payload}
        else:
            rv = dict(self.payload or ())
        rv['fulfillmentText'] = self.message
        rv['errorType'] = str(type(self).__name__)
        if self.payload:
            if self.payload.startswith('{'):
                rv['payload'] = json.loads(self.payload)
            else:
                rv['payload'] = self.payload
        return rv


class InvalidDataFormat(SamException):
    """
    The format of the data is invalid
    """
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class InvalidDataType(SamException):
    """
    The type of the data is invalid
    """

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class InvalidDataValue(SamException):
    """
    The value of the data is invalid
    """
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class NoTokenError(SamException):
    """
    No token was provided when accessing some API
    """
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class SpotifyPlaylistNotfoundError(SamException):
    """
    Spotify Playlist was not found anywhere
    """
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message, status_code, payload)
