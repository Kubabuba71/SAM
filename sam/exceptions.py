from .sam import app
from flask import jsonify


class SamException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['fulfillmentText'] = self.message
        return rv


class InvalidDataFormat(SamException):
    """
    The format of the data is invalid
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


@app.errorhandler(InvalidDataFormat)
def handle_invalid_data_format(error: InvalidDataFormat):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(NoTokenError)
def handle_invalid_data_format(error: NoTokenError):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(SpotifyPlaylistNotfoundError)
def handle_invalid_data_format(error: SpotifyPlaylistNotfoundError):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
