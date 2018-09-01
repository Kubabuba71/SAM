class InvalidDataFormat(Exception):
    """
    The format of the data is invalid
    """
    pass


class NoTokenError(Exception):
    """
    No token was provided when accessing some API
    """
    pass


class SpotifyPlaylistNotfoundError(Exception):
    """
    Spotify Playlist was not found anywhere
    """
    pass
