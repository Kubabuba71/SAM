"""
Return various weather forecast, using ISO-8601 datetime format
"""
import datetime
import time
import iso8601
import requests


from .constants import (DARKSKY_URL, GOOGLE_MAPS_TIMEZONE_URL, GOOGLE_MAPS_GEOCODE_URL,
                        GOOGLE_MAPS_TIMEZONE_KEY, GOOGLE_MAPS_GEOCODE_KEY)


def get_offset_from_utc(coordinates):
    """
    Return the offset for daylight-savings time in seconds
    """
    current_epoch_time = time.time()
    url = ''.join([GOOGLE_MAPS_TIMEZONE_URL, '?location=', str(coordinates['lat']), ',',
                   str(coordinates['lng']), '&timestamp=', str(int(current_epoch_time)),
                   '&key=', GOOGLE_MAPS_TIMEZONE_KEY])
    json_data = requests.get(url).json()
    return json_data['dstOffset'] + json_data['rawOffset']


def get_json(url, params=None):
    # type: (str, Optional[dict[str]]) -> dict
    """
    Returns the json (represented as a dict) for specified url
    :param url: the url that json should be retrieve from
    :param params: optional parameters that can be used as URL parameters
    :returns: dict that contains the json from the url location
    """
    if params is None:
        return requests.get(url).json()
    else:
        return requests.get(url, params=params).json()


def get_coordinates(location):
    # type: (str) -> dict
    """
    Returns a dict, with the coordinates for specified location
    :param location: the location for which coordinates are to be parsed
    :returns: dict that contains lat and lng
    """
    location = location.replace(' ', '+')
    params = {
        'address': location,
        'key': GOOGLE_MAPS_GEOCODE_KEY
    }
    json_data = get_json(GOOGLE_MAPS_GEOCODE_URL, params=params)
    coordinates = json_data['results'][0]['geometry']['location']
    coordinates['lng'] = round(coordinates['lng'], 7)
    coordinates['lat'] = round(coordinates['lat'], 7)
    return coordinates


def get_weather_data_all(coordinates):
    """
    :param coordinates: The coordinates to get all weather data for
    :returns: a dict (json) with all weather data
    Return all weather forecast data
    """
    url = (
        DARKSKY_URL
        + str(coordinates['lat'])
        + ','
        + str(coordinates['lng'])
        + '/?units=si'
    )
    return get_json(url)


def get_weather_data_minutely(coordinates):
    """
    Return minutely weather data
    :param coordinates: The coordinates to get all weather data for
    :returns: a dict (json) with minutely weather data
    """
    url = (
        DARKSKY_URL
        + str(coordinates['lat'])
        + ','
        + str(coordinates['lng'])
        + '/?units=si&exclude=currently,hourly,daily,alerts,flags'
    )
    return get_json(url)


def get_weather_data_hourly(coordinates):
    """
    Return hourly weather data
    :param coordinates: The coordinates to get all weather data for
    :returns: a dict (json) with hourly weather data
    """
    url = (
        DARKSKY_URL
        + str(coordinates['lat'])
        + ','
        + str(coordinates['lng'])
        + '/?units=si&exclude=currently,minutely,daily,alerts,flags'
    )
    return get_json(url)


def get_weather_data_daily(coordinates):
    """
    Return daily weather data
    :param coordinates: The coordinates to get all weather data for
    :returns: a dict (json) with daily weather data
    """
    url = (
        DARKSKY_URL
        + str(coordinates['lat'])
        + ','
        + str(coordinates['lng'])
        + '/?units=si&exclude=currently,minutely,hourly,alerts,flags'
    )
    return get_json(url)


def get_weather_data_current(coordinates):
    """
    Return current weather data
    :param coordinates: The coordinates to get all weather data for
    :returns: a dict (json) with current weather data
    """
    url = (
        DARKSKY_URL
        + str(coordinates['lat'])
        + ','
        + str(coordinates['lng'])
        + '/?units=si&exclude=minutely,hourly,daily,alerts,flags'
    )
    return get_json(url)


def get_weather_current(coordinates):
    """
    Return current weather summary
    :param coordinates: The coordinates to get current weather summary for
    :returns: a str summary  of the current weather located at coordinates
    """
    json_data = get_weather_data_current(coordinates)
    return (
        json_data['currently']['summary']
        + ' with a temperature of '
        + json_data['currently']['apparentTemperature']
        + ' celsius.'
    )


def get_weather_no_date_time(coordinates):
    """
    Return weather summary for next few hours
    :param coordinates: The coordinates to get weather summary for
    :returns: a str summary  of the upcoming weather (next few hours) located at coordinates
    """
    json_data = get_weather_data_hourly(coordinates)
    return json_data['hourly']['summary']


def get_weather_for_hour(coordinates, time_input):
    """
    Return weather summary for a specific hour
    :param coordinates: The coordinates to get weather summary for
    :param time_input: The specific hour to get weather summary for
    :returns: a str summary  of the upcoming weather at the specified hour located at coordinates
    """
    time_input = iso8601.parse_date(time_input)
    time_input = time.mktime(time_input.timetuple())

    json_data = get_weather_data_hourly(coordinates)
    response = ''
    for i in json_data['hourly']['data']:
        if i['time'] == time_input:
            response = (
                i['summary']
                + ' with a temperature of '
                + str(int(round(i['apparentTemperature'])))
                + ' degrees Celsius.'
            )
            break
    return response


def get_weather_for_day(coordinates, time_input):
    """
    Return weather summary for an entire day
    :param coordinates: The coordinates to get weather summary for
    :param time_input: The specific day to get weather summary for
    :returns: a str summary of the weather on the specified day located at coordinates
    """
    hour_offset = get_offset_from_utc(coordinates)
    time_input = iso8601.parse_date(time_input)
    time_input = (
        time.mktime(time_input.timetuple()) - hour_offset + 3600
    )  # Convert ISO time to epoch time
    json_data = get_weather_data_daily(coordinates)
    response = ''
    for i in range(15):
        try:
            if json_data['daily']['data'][i]['time'] == time_input:

                average_temp = (
                    json_data['daily']['data'][i]['apparentTemperatureMax']
                    + json_data['daily']['data'][i]['apparentTemperatureMin']
                ) / 2

                weather_summary = json_data['daily']['data'][i]['summary']
                weather_summary = weather_summary.replace('.', '')

                response = ' '
                response = response.join(
                    [
                        weather_summary,
                        'with a temperature of',
                        str(int(round(average_temp))),
                        'degrees Celsius',
                    ]
                )
                return response
        except IndexError:
            return 'weather.get_weather_for_day()_1'


def get_weather_for_time_period(coordinates, date_time):
    """
    Return weather summary for a a time period (around 4 hours)
    :param coordinates: The coordinates to get weather summary for
    :param date_time: The time period to get weather summary for
    :returns: a str summary of the weather for the specified date_time located at coordinates
    """
    date_time = iso8601.parse_date(date_time)
    date_time = time.mktime(date_time.timetuple())

    json_data = get_weather_data_hourly(coordinates)
    response = ''
    for i in json_data['hourly']['data']:
        if i['time'] == int(date_time):
            response = (
                i['summary']
                + ' with a temperature of '
                + str(int(round(i['apparentTemperature'])))
                + ' degrees Celsius.'
            )
            break
    return response


def weather(date_time, location):
    """
    Return weather summary for date_time
    :param date_time: The time to get the weather for
    :param location: The location to get the weather for
    """
    response = ''
    coordinates = get_coordinates(location)

    if date_time != '':
        date_time_len = len(date_time)

        if date_time_len == 10:
            # Get the weather forecast for the whole day
            # 2014-08-09
            # works
            response = get_weather_for_day(coordinates, date_time)

        elif date_time_len == 41:
            # Get weather forecast for date-time period
            # 2017-02-08T08:00:00Z/2017-02-08T12:00:00Z
            # works
            average_hour = (int(date_time[11:13]) + int(date_time[32:34])) / 2

            if average_hour <= 9:
                average_hour = '0' + str(average_hour)

            date_time = date_time[:11] + str(average_hour) + ':00:00Z'

            response = get_weather_for_time_period(coordinates, date_time)

        elif date_time_len == 8:
            # Get the weather forecast for a specific hour today
            # 16:00:00
            # works
            current_time = datetime.datetime.now().isoformat()
            date_time = current_time[:11] + date_time
            response = get_weather_for_hour(coordinates, date_time)

        elif date_time_len == 20:
            # Get the weather forecast for a specific hour for some day
            # 2014-08-09T16:00:00Z
            # kind of works
            response = get_weather_for_hour(coordinates, date_time)

        elif date_time_len == 17:
            # 13:00:00/14:00:00
            # works
            average_hour = (int(date_time[:2]) + int(date_time[9:11])) / 2
            if average_hour <= 9:
                average_hour = '0' + str(average_hour)
            current_time = datetime.datetime.now().isoformat()
            date_time = current_time[:11] + str(average_hour) + ':00:00'
            response = get_weather_for_hour(coordinates, date_time)
        else:
            return 'Could not resolve date-time type'

    else:
        return get_weather_no_date_time(coordinates)

    if response == '':
        return 'weather.weather()_2'

    return str(response)
