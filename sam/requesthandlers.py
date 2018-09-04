from .calendar_ import calender_action
from .exceptions import InvalidDataFormat
from .music import music_action
from .weather import weather_action


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
        res = calender_action()
    elif action.startswith('weather'):
        res = weather_action(json_data)
    else:
        raise InvalidDataFormat(f'action is not supported: {action}')

    return res
