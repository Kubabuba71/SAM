"""
Return various weather forecast, using ISO-8601 datetime format
"""
import datetime
import time
import iso8601
import requests
from copy import deepcopy


from .constants import (DARK_SKY_URL, GOOGLE_MAPS_TIMEZONE_URL, GOOGLE_MAPS_GEOCODE_URL,
                        DARK_SKY_KEY, GOOGLE_MAPS_TIMEZONE_KEY, GOOGLE_MAPS_GEOCODE_KEY)

WEATHER_PARAMETERS = ['currently', 'minutely', 'hourly', 'daily', 'alerts', 'flags']


def get_offset_from_utc(coordinates):
    # type: (dict) -> int
    """
    Calculate the offset coordinates has from utc

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :return: the offset coordinates has from utc time
    """

    current_epoch_time = time.time()
    url = generate_googlemaps_timezone_url(coordinates, current_epoch_time)
    params = {'key': GOOGLE_MAPS_TIMEZONE_KEY}
    json_data = get_json(url, params=params)
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


def generate_darksky_url(coordinates):
    # type: (dict) -> str
    """
    Generate a dark_sky url with lat and lng

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :return: The generated dark_sky url, with lat and lng properly formatted and positioned
    """
    lat = coordinates['lat']
    lng = coordinates['lng']
    url = '{}{}/{},{}'.format(DARK_SKY_URL, DARK_SKY_KEY, lat, lng)
    return url


def generate_googlemaps_timezone_url(coordinates, epoch_time):
    # type: (dict, double) -> str
    """

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :param epoch_time: the epoch time for which the offset is being calculated for
    :return:
    """
    url = '{}?location={},{}&timestamp={}'.format(GOOGLE_MAPS_TIMEZONE_URL, str(coordinates['lat']),
                                                  str(coordinates['lng']), str(int(epoch_time)))
    return url


def get_weather_data(coordinates, include=None):
    # type: (dict, Optional(list[str])) -> dict
    """
    Returns a dict (json), with weather data for the specified coordinates.
    If include is specified, only that data is retrieved.
    Otherwise, all data is retrieved.

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :param include: Optional list of json data to include
    :returns: a dict (json) with (the specified) data
    """
    url = generate_darksky_url(coordinates)
    params = {'units': 'si'}
    if include is not None:
        weather_parameters = deepcopy(WEATHER_PARAMETERS)
        for param in include:
            weather_parameters.remove(param)
        params['exclude'] = ','.join(weather_parameters)
    return get_json(url, params=params)


def generate_summary(json_data, index=None):
    if index is not None:
        summary = json_data[index]['summary']
        temperature = json_data[index]['apparentTemperature']
    else:
        summary = json_data['summary']
        temperature = (json_data['apparentTemperatureMax'] + json_data['apparentTemperatureMin']) / 2
    result = '{} with a temperature of {} degrees celsius'.format(summary, temperature)
    return result


def get_coordinates(location):
    # type: (str) -> dict
    """
    Returns a dict (json), with the coordinates for specified location

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


def get_weather_summary_current(coordinates):
    # type: (dict) -> str
    """
    Returns current weather summary

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :returns: a str summary  of the current weather located at coordinates
    """
    json_data = get_weather_data(coordinates, include=['currently'])
    result = generate_summary(json_data, 'currently')
    return result


def get_weather_summary_no_date_time(coordinates):
    # type: (dict) -> str
    """
    Returns weather summary for the next few hours

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :returns: a str summary  of the upcoming weather (next few hours) located at coordinates
    """
    json_data = get_weather_data(coordinates, include=['currently'])
    result = generate_summary(json_data, 'currently')
    return result


def get_weather_summary_for_hour(date_time, coordinates):
    # type: (dict) -> str
    """
    Returns weather summary for the specific hour

    :param date_time: The specific hour to get weather summary for
    :param coordinates: The coordinates to get weather summary for
    :returns: a str summary  of the upcoming weather at the specified hour located at coordinates
    """
    date_time = iso8601.parse_date(date_time)
    date_time = time.mktime(date_time.timetuple())

    json_data = get_weather_data(coordinates, include=['hourly'])
    for entry in json_data['hourly']['data']:
        if entry['time'] == date_time:
            response = '{} with a temperature of {} degrees Celsius.'\
                .format(entry['summary'], str(int(round(entry['apparentTemperature']))))
            return response


def get_weather_summary_for_day(date_time, coordinates):
    # type: (dict, str) -> str
    """
    Returns weather summary for the entire day

    :param date_time: The specific day to get weather summary for
    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :returns: a str summary of the weather on the specified day located at coordinates
    """
    hour_offset = get_offset_from_utc(coordinates)
    date_time = iso8601.parse_date(date_time)
    date_time = time.mktime(date_time.timetuple()) - hour_offset + 3600
    json_data = get_weather_data(coordinates, include=['daily'])
    for i in range(15):
        try:
            if json_data['daily']['data'][i]['time'] == date_time:
                summary = generate_summary(json_data['daily']['data'][i])
                return summary
        except IndexError:
            return 'weather.get_weather_for_day()_1'


def get_weather_summary_for_time_period(date_time, coordinates):
    # type: (dict, str) -> str
    """
    Return weather summary for a a time period (around 4 hours)

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :param date_time: The time period to get weather summary for
    :returns: a str summary of the weather for the specified date_time located at coordinates
    """
    date_time = iso8601.parse_date(date_time)
    date_time = time.mktime(date_time.timetuple())

    json_data = get_weather_data(coordinates, include=['hourly'])
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
    # type: (Union[str, dict], str) -> str
    """
    Return weather summary for date_time

    :param date_time: The time to get the weather for
    :param location: The location to get the weather for
    :returns: the generated response, based on date_time and location
    """
    coordinates = get_coordinates(location)
    date_time_len = len(date_time)

    if isinstance(date_time, dict):
        start_date_time = date_time['startDateTime']
        end_date_time = date_time['endDateTime']
        average_hour = (int(start_date_time[11:13]) + int(end_date_time[11:13])) / 2
        if average_hour <= 9:
            average_hour = '0{}'.format(average_hour)
        date_time = end_date_time[:11] + str(average_hour) + ':00:00Z'
        print('date_time:{}'.format(date_time))
        response = get_weather_summary_for_time_period(date_time, coordinates)

    elif date_time_len == 10:
        # Get the weather forecast for the whole day
        # 2014-08-09
        # works
        response = get_weather_summary_for_day(date_time, coordinates)

    elif date_time_len == 8:
        # Get the weather forecast for a specific hour today
        # 16:00:00
        # works
        current_time = datetime.datetime.now().isoformat()
        date_time = current_time[:11] + date_time
        response = get_weather_summary_for_hour(date_time, coordinates)

    elif date_time_len == 20:
        # Get the weather forecast for a specific hour for some day
        # 2014-08-09T16:00:00Z
        # kind of works
        response = get_weather_summary_for_hour(date_time, coordinates)

    elif date_time_len == 17:
        # 13:00:00/14:00:00
        # works
        average_hour = (int(date_time[:2]) + int(date_time[9:11])) / 2
        if average_hour <= 9:
            average_hour = '0' + str(average_hour)
        current_time = datetime.datetime.now().isoformat()
        date_time = current_time[:11] + str(average_hour) + ':00:00'
        response = get_weather_summary_for_hour(date_time, coordinates)

    else:
        return get_weather_summary_no_date_time(coordinates)

    if not response:
        return 'weather.weather()_2'

    return str(response)
