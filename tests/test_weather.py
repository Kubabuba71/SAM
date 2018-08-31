
def test_weather_current(load_dotenv, request_handler, weather_current):
    handler = request_handler(weather_current)
    res = handler.handle_request()
    assert 'degrees' in res['fulfillmentText']


def test_weather_current_location(load_dotenv, request_handler, weather_current_location, now_str):
    weather_current_location['queryResult']['parameters']['date-time'] = now_str
    weather_current_location['queryResult']['outputContexts'][0]['parameters']['date-time'] = now_str
    handler = request_handler(weather_current_location)
    res = handler.handle_request()
    assert 'degrees' in res['fulfillmentText']


def test_weather_day(load_dotenv, request_handler, weather_day):
    handler = request_handler(weather_day)
    res = handler.handle_request()
    assert 'degrees' in res['fulfillmentText']


def test_weather_followup_location(load_dotenv, request_handler, weather_followup_location):
    handler = request_handler(weather_followup_location)
    res = handler.handle_request()
    assert 'degrees' in res['fulfillmentText']


def test_weather_period(load_dotenv, request_handler, weather_period):
    handler = request_handler(weather_period)
    res = handler.handle_request()
    assert 'degrees' in res['fulfillmentText']
