from ..exceptions import InvalidDataFormat
from ..wrappers import calendar_
from dateutil import parser as date_parser


def get_events_summary(date_: str) -> str:
    """
    Get a summary of the events for the given date_
    :param date_:   The day for which events are retrieved.
                    Must be the very start of the day, such as 2018-09-20T12:00:00+02:00.
                    Must be an RFC3339 timestamp
    e.g.:           2018-09-20T12:00:00+02:00 or 2018-09-20T12:00:00Z
    """
    date_start = date_
    # date_end will be 23:59:59 hours ahead of date_start
    date_end = date_parser.parse(date_).replace(hour=23, minute=59, second=59).isoformat()
    events = calendar_.get_events(calendar_id='primary',
                                  date_start=date_start,
                                  date_end=date_end)

    if len(events) == 0:
        res = date_parser.parse(date_).strftime('No events planned for %B %d')
    else:
        res = '. '.join(generate_event_summary(event) for event in events)
    return res


def generate_event_summary(event: dict) -> str:
    """
    Generate a summary for a given event. Summary is simply the place, time and name of the event

    :param event: Event retrieved from the Google Calendar API
    """

    start = date_parser.parse(event['start']['dateTime']).strftime('%H:%M')
    end = date_parser.parse(event['end']['dateTime']).strftime('%H:%M')
    location = event.get('location', None)
    summary = event.get('summary')

    res = f'{summary} from {start} until {end}'

    if location:
        res += f' at {location}'

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
        raise InvalidDataFormat('No specific calendar was provided.')

    parameters = query_result.get('parameters', None)

    if parameters:
        date = parameters.get('date', None)

    if action == 'generic':
        res = get_events_summary(date)

    return res
