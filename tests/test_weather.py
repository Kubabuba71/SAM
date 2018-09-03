from sam.requesthandlers import handle_request


def test_weather_current(load_dotenv, weather_current):
    res = handle_request(weather_current)
    assert 'degrees' in res['fulfillmentText']


def test_weather_current_location(load_dotenv, weather_current_location, now_str):
    weather_current_location['queryResult']['parameters']['date-time'] = now_str
    weather_current_location['queryResult']['outputContexts'][0]['parameters']['date-time'] = now_str
    res = handle_request(weather_current_location)
    assert 'degrees' in res['fulfillmentText']


def test_weather_day(load_dotenv, weather_day):
    res = handle_request(weather_day)
    assert 'degrees' in res['fulfillmentText']


def test_weather_followup_location(load_dotenv, weather_followup_location):
    res = handle_request(weather_followup_location)
    assert 'degrees' in res['fulfillmentText']


def test_weather_period(load_dotenv, weather_period):
    res = handle_request(weather_period)
    assert 'degrees' in res['fulfillmentText']
