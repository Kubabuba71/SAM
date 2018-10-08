from .action_handlers.calendar_ import calender_action
from .action_handlers.music import music_action
from .action_handlers.weather import weather_action
from .exceptions import InvalidDataFormatError
from .utils import log, logged, now_str


@logged
def handle_sam_request(json_data: dict) -> dict:
    """
    Handles the incoming request, by taking the appropriate action
    :returns: The appropriate str response for the specified action

    Minimal example for json_data. This will play Damn Album by Kendrick Lamar on Spotify
    {
        "queryResult": {
          "queryText": "Play Damn album",
          "action": "music.play",
          "parameters": {
            "album": "Damn",
          }
        }
    }
    """
    query_result = json_data.get('queryResult')
    action = query_result.get('action')

    if action.startswith('music'):
        res = music_action(json_data)
    elif action.startswith('calendar'):
        res = calender_action(json_data)
    elif action.startswith('weather'):
        res = weather_action(json_data)
    else:
        raise InvalidDataFormatError(f'action is not supported: {action}')
    log(f'{now_str()}-DEBUG_ACTION: {action}')
    return res
