from . import web_session

from .constants import SAM_HOST


def handle_request(json_data: dict) -> dict:
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
        res = web_session.post(SAM_HOST + '/music', json=query_result).json()
    elif action.startswith('calendar'):
        res = web_session.post(SAM_HOST + '/calendar', json=query_result).json()
    elif action.startswith('weather'):
        res = web_session.post(SAM_HOST + '/weather', json=query_result)
        res = res.json()

    return res
