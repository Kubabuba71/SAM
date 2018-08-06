from . import spotify_oauth2_session


def login():
    spotify_oauth2_session.authorization_url()


def currently_playing():
    """
    Get the currently playing information

    :returns: requests.Response
    """
    res = spotify_oauth2_session.get('https://api.spotify.com/v1/me/player/currently-playing')
    return res


def token_info():
    """
    Return current token info for the OAuth2Session
    """
    res = spotify_oauth2_session.oauth2_session.token
    return res


def callback(callback_url):
    """
    Fetch an access token, based on the callback_url

    :param callback_url: The callback urlreturned by the Spotify API,
                         after the user authorized (or denied) access to their account
    """
    spotify_oauth2_session.fetch_token(callback_url)
