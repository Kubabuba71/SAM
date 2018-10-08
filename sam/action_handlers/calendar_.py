from ..exceptions import InvalidDataFormatError
from ..wrappers import calendar_
from dateutil import parser as date_parser
from datetime import datetime


def get_next_event() -> str:
    """
    Get the summary for the next event
    """
    now = datetime.utcnow().isoformat()
    if not now.endswith('Z') and '+' not in now:
        now += 'Z'
    events = calendar_.get_events(time_min=now)

    if not events:
        res = 'No upcoming events planned'
    else:
        res = generate_event_summary(events[0], specify_day=True)
    return res


def get_events_summary(date_: str) -> str:
    """
    Get a summary of the events for the given date_
    :param date_:   The day for which events are retrieved.
                    Must be the very start of the day, such as 2018-09-20T12:00:00+02:00.
                    Must be an RFC3339 timestamp
    e.g.:           2018-09-20T12:00:00+02:00 or 2018-09-20T12:00:00Z
    """

    # TODO: Ensure that timezone is present in date_start and date_end
    date_start = date_
    # date_end will be 23:59:59 hours ahead of date_start
    date_end = date_parser.parse(date_).replace(hour=23, minute=59, second=59).isoformat()
    events = calendar_.get_events(time_min=date_start,
                                  time_max=date_end)

    if not events:
        res = date_parser.parse(date_).strftime('No events planned for %B %d')
    else:
        res = '. '.join(generate_event_summary(event) for event in events)
    return res


def get_by_type(event_type: str, time_min: str, specify_time: bool=True,
                specify_day: bool=True, specify_location: bool=False) -> str:
    """
        Get event time summary for the next event that has a type of event_type and occurs on date_
        :param event_type:  The type of the event to search form e.g.: 'lecture', 'meeting'
        :param time_min:    The date on which the event occurs.
                            Can be None, in which case,
                            the next event of type event_type is returned
        """

    original_date = time_min
    if time_min is None:
        now = datetime.now()
        time_min = datetime(now.year, now.month, now.day).isoformat() + 'Z'
        if not time_min.endswith('Z') and '+' not in time_min:
            time_min += 'Z'
    else:
        dt = date_parser.parse(time_min)
        time_min = datetime(dt.year, dt.month, dt.day).isoformat()
        time_max = datetime(dt.year, dt.month, dt.day) \
            .replace(hour=23, minute=59, second=59).isoformat()
        if not time_max.endswith('Z') and '+' not in time_max:
            time_max += 'Z'

    if not time_min.endswith('Z') and '+' not in time_min:
        time_min += 'Z'

    event_type = event_type.strip().lower()

    if event_type == 'lecture':
        secondary_event_type = '(le)'
    elif event_type == 'seminar':
        secondary_event_type = '(se)'
    elif event_type == 'exam':
        secondary_event_type = '(ex)'
    else:
        secondary_event_type = None

    if original_date is None:
        # Get the next event, no matter the day
        events = calendar_.get_events(time_min=time_min)
    else:
        events = calendar_.get_events(time_min=time_min, time_max=time_max)

    for event in events:
        event_summary = event['summary'].lower()
        if event_type in event_summary \
                or (secondary_event_type is not None and secondary_event_type in event_summary):
            res = generate_event_summary(event,
                                         specify_time=specify_time,
                                         specify_day=specify_day,
                                         specify_location=specify_location)
            break
    else:
        if original_date is None:
            res = f'No upcoming {event_type} event'
        else:
            res = date_parser.parse(time_min).strftime(f'No {event_type} event on %A')
    return res


def generate_event_summary(event: dict, specify_time: bool=True,
                           specify_day: bool=False, specify_location=True) -> str:
    """
    Generate a summary for a given event. Summary is simply the place, time and name of the event

    :param event:               Event retrieved from the Google Calendar API
    :param specify_time:        Whether the time for the event should be specified
    :param specify_day:         Whether the weekday for the event should be specified
    :param specify_location:    Whether the location for the event should be specified
    """

    # TODO: Handle cases when start.dateTime and end.dateTime aren't present
    start = date_parser.parse(event['start']['dateTime']).strftime('%H:%M')
    end = date_parser.parse(event['end']['dateTime']).strftime('%H:%M')
    location = event.get('location', None)
    summary = event.get('summary')

    res = f'{summary}'

    if specify_time:
        res += f' from {start} until {end}'
    if specify_location and location is not None:
        res += f' at {location}'
    if specify_day:
        res += date_parser.parse(event['start']['dateTime']).strftime(' on %A')

    return res


def calender_action(query_result):
    """
    Perform a calendar action
    :param query_result:    dict -  All information necessary to perform the calendar_action.
                                    Depending on the action, different key-value pairs are needed.
                                    The below example shows all possible parameters.
                                    Note that not ALL of these are needed, depending on the action.
    e.g.:
        "action": "calendar",
        "parameters": {
          "date": "2018-09-20T12:00:00+02:00"
        }
    """
    if 'queryResult' in query_result:
        query_result = query_result['queryResult']

    action = query_result.get('action').split('.')[1]

    if not action:
        raise InvalidDataFormatError('No specific calendar was provided.')

    if 'parameters' in query_result:
        parameters = query_result.get('parameters')
        date = None if parameters.get('date', '') == '' else parameters.get('date')
        event_type = None if parameters.get('event', '') == '' else parameters.get('event')

    if action == 'generic':
        res = get_events_summary(date)
    elif action == 'next':
        res = get_next_event()
    elif action == 'time':
        res = get_by_type(event_type, date, specify_time=True, specify_day=True, specify_location=False)
    elif action == 'location':
        res = get_by_type(event_type, date, specify_time=False, specify_day=False, specify_location=True)
    return res
