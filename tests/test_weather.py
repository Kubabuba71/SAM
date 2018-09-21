from sam.requesthandlers import handle_sam_request

from datetime import date, datetime


def test_weather_current():
    query = {
        "queryResult": {
            "action": "weather",
            "parameters": {
                "location": {
                    "city": "Amsterdam"
                }
            }
        }
    }
    res = handle_sam_request(query)
    assert 'degrees' in res


def test_weather_current_location(now_str):
    query = {
        "queryResult": {
            "action": "weather",
            "date-time": now_str,
            "parameters": {
                "location": {
                    "city": "Tbilisi"
                }
            }
        }
    }
    res = handle_sam_request(query)
    assert 'degrees' in res


def test_weather_day(tomorrow_str):
    query = {
        "queryResult": {
            "action": "weather",
            "date": tomorrow_str,
            "parameters": {
                "location": {
                    "city": "Tbilisi"
                }
            }
        }
    }
    res = handle_sam_request(query)
    assert 'degrees' in res


def test_weather_period():
    today = date.today()
    start = datetime(today.year, today.month, today.day, 12, 0, 0).isoformat() + 'Z'
    end = datetime(today.year, today.month, today.day, 16, 0, 0).isoformat() + 'Z'
    query = {
        "queryResult": {
            "action": "weather",
            "date-time": {
                "startDateTime": start,
                "endDateTime": end
            },
            "parameters": {
                "location": {
                    "city": "Tbilisi"
                }
            }
        }
    }
    res = handle_sam_request(query)
    assert 'degrees' in res
