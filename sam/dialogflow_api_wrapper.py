import apiai
import json
import os

DIALOGFLOW_CLIENT_ACCESS_TOKEN = os.environ['DIALOGFLOW_CLIENT_ACCESS_TOKEN']
ai = apiai.ApiAI(DIALOGFLOW_CLIENT_ACCESS_TOKEN)


def make_query(query: str) -> dict:
    request = ai.text_request()
    request.query = query
    response = request.getresponse()
    return json.loads(response.read())
