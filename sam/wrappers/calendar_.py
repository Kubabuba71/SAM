from ..constants import (GOOGLE_CALENDAR_AUTHORIZATION_URI,
                         GOOGLE_CALENDAR_CLIENT_ID,
                         GOOGLE_CALENDAR_CLIENT_SECRET,
                         GOOGLE_CALENDAR_REDIRECT_URI, GOOGLE_CALENDAR_SCOPE,
                         GOOGLE_CALENDAR_TOKEN_URI,
                         GOOGLE_CALENDAR_WRAPPER_STR, GOOGLE_CALENDAR_CUSTOM_CALENDAR_IDS)
from ..sessions.oauth2 import OAuth2Session

oauth2 = OAuth2Session(client_id=GOOGLE_CALENDAR_CLIENT_ID,
                       client_secret=GOOGLE_CALENDAR_CLIENT_SECRET,
                       redirect_uri=GOOGLE_CALENDAR_REDIRECT_URI,
                       token_uri=GOOGLE_CALENDAR_TOKEN_URI,
                       authorization_uri=GOOGLE_CALENDAR_AUTHORIZATION_URI,
                       scope=GOOGLE_CALENDAR_SCOPE,
                       state=GOOGLE_CALENDAR_WRAPPER_STR,
                       component='Google Calendar')


def get_events(calendar_id='primary', time_min: str=None, time_max: str=None,
               order_by: str='startTime', **kwargs)-> list:
    """
    Return a list of events
    :param calendar_id:     ID of the calendar for which events are retrieved
    :param time_min:        Upper bound (exclusive) for an event's start time to filter by
    :param time_max:        Lower bound (inclusive) for an event's end time to filter by.
    :param order_by:        Order by 'startTime' or 'updated'
    """

    params = {
        'timeMin': time_min,
        'timeMax': time_max,
        'singleEvents': True,
        'orderBy': order_by
    }
    
    params.update(kwargs.get('params', dict()))
    calendar_ids = [calendar_id]
    calendar_ids.extend(GOOGLE_CALENDAR_CUSTOM_CALENDAR_IDS)
    res = list()
    for cal_id in calendar_ids:
        res.extend(oauth2.get(f'https://www.googleapis.com/calendar/v3/calendars/{cal_id}/events',
                              params=params).json()['items'])
    return res
