"""
Return various weather forecast, using ISO-8601 datetime format
"""
from datetime import datetime
from dateutil import parser as date_parser
import time
import requests
from copy import deepcopy


from .constants import (DARK_SKY_URL, GOOGLE_MAPS_TIMEZONE_URL, GOOGLE_MAPS_GEOCODE_URL,
                        DARK_SKY_KEY, GOOGLE_MAPS_TIMEZONE_KEY, GOOGLE_MAPS_GEOCODE_KEY)

WEATHER_PARAMETERS = ['currently', 'minutely', 'hourly', 'daily', 'alerts', 'flags']


def get_datetime_from_string(datetime_str):
    # type: (str) -> datetime
    """
    Given a str, generate equivalent datetime object

    :param datetime_str: string representation of time
    :return: the corresponding datetime object
    """
    datetime_object = date_parser.parse(datetime_str)
    return datetime_object


def get_offset_from_utc(coordinates):
    # type: (dict) -> int
    """
    Calculate the offset coordinates has from utc

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :return: the offset, in seconds, that coordinates has from utc time
    """

    current_epoch_time = time.time()
    lat = coordinates['lat']
    lng = coordinates['lng']
    location_param = '{},{}'.format(lat, lng)

    params = {'key': GOOGLE_MAPS_TIMEZONE_KEY,
              'location': location_param,
              'timestamp': current_epoch_time}

    json_data = get_json(GOOGLE_MAPS_TIMEZONE_URL, params=params)
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
        r = requests.get(url)
    else:
        r = requests.get(url, params=params)
    return r.json()


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
    result = '{} with a temperature of {} degrees celsius'.format(summary, str(round(temperature, 2)))
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


def get_weather_summary_no_datetime(coordinates):
    # type: (dict) -> str
    """
    Returns weather summary for the next few hours

    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :returns: a str summary  of the upcoming weather (next few hours) located at coordinates
    """
    json_data = get_weather_data(coordinates, include=['currently'])
    result = generate_summary(json_data, 'currently')
    return result


def get_weather_summary_for_hour(datetime_, coordinates):
    # type: (dict) -> str
    """
    Returns weather summary for the specific hour

    :param datetime_: The specific hour to get weather summary for
    :type datetime_: datetime_
    :param coordinates: The coordinates to get weather summary for
    :returns: a str summary  of the upcoming weather at the specified hour located at coordinates
    """
    timestamp = datetime_.timestamp()

    json_data = get_weather_data(coordinates, include=['hourly'])
    for entry in json_data['hourly']['data']:
        if entry['time'] == timestamp:
            response = '{} with a temperature of {} degrees Celsius.'\
                .format(entry['summary'], str(int(round(entry['apparentTemperature']))))
            return response


def get_weather_summary_for_day(datetime_, coordinates):
    # type: (dict, str) -> str
    """
    Returns weather summary for the entire day

    :param datetime_: The specific day to get weather summary for
    :type datetime_: datetime
    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :returns: a str summary of the weather on the specified day located at coordinates
    """
    new_datetime = datetime(
        datetime_.year,
        datetime_.month,
        datetime_.day)
    timestamp = new_datetime.timestamp()
    json_data = get_weather_data(coordinates, include=['daily'])
    for entry in json_data['daily']['data']:
        try:
            if entry['time'] == timestamp:
                summary = generate_summary(entry)
                return summary
        except IndexError:
            return 'weather.get_weather_for_day()_1'


def get_weather_summary_for_time_period(datetime_, coordinates):
    # type: (dict, str) -> str
    """
    Return weather summary for a a time period (around 4 hours)

    :param datetime_: The time to get weather summary for
    :type datetime_: datetime
    :param coordinates: dict containing the lat and lng keys (and their respective values)
    :type coordinates: datetime
    :returns: a str summary of the weather for the specified datetime_ located at coordinates
    """
    # new_datetime_ = datetime(
    #     datetime_.year,
    #     datetime_.month,
    #     datetime_.day
    # )
    timestamp = datetime_.timestamp()
    json_data = get_weather_data(coordinates, include=['hourly'])
    for i in json_data['hourly']['data']:
        if i['time'] == timestamp:
            response = '{} with a temperature of {} degreese Celsius.'\
                .format(i['summary'], str(int(round(i['apparentTemperature']))))
            return response


def weather(datetime_, location):
    # type: (Union[str, dict], str) -> str
    """
    Return weather summary for datetime_

    :param datetime_: The time to get the weather for
    :param location: The location to get the weather for
    :returns: the generated response, based on datetime_ and location
    """
    coordinates = get_coordinates(location)
    datetime_len = len(datetime_)

    if isinstance(datetime_, dict):
        start_hour = date_parser.parse(datetime_['startDateTime']).hour
        end_hour = date_parser.parse(datetime_['endDateTime']).hour

        average_hour = int((start_hour + end_hour) / 2)

        if average_hour < 0 or average_hour > 24:
            return "Error, average_hour has been calculated as invalid"
        if average_hour <= 9:
            average_hour = '0{}'.format(average_hour)

        new_str = ''.join([
            datetime_['startDateTime'][:11],
            str(average_hour),
            datetime_['startDateTime'][13:]
        ])

        new_datetime_ = date_parser.parse(new_str)

        print('new_datetime_:{}'.format(new_datetime_))
        response = get_weather_summary_for_time_period(new_datetime_, coordinates)

    else:
        datetime_object = date_parser.parse(datetime_)
        if datetime_len == 10:
            # Get the weather forecast for the whole day
            # 2014-08-09
            # works
            response = get_weather_summary_for_day(datetime_object, coordinates)

        elif datetime_len == 8:
            # Get the weather forecast for a specific hour today
            # 16:00:00
            # works
            current_time = datetime.now().isoformat()
            datetime_ = current_time[:11] + datetime_
            response = get_weather_summary_for_hour(datetime_, coordinates)

        elif datetime_ == 20:
            # Get the weather forecast for a specific hour for some day
            # 2014-08-09T16:00:00Z
            # kind of works
            response = get_weather_summary_for_hour(datetime_object, coordinates)

        elif datetime_len == 17:
            # 13:00:00/14:00:00
            # works
            average_hour = (int(datetime_[:2]) + int(datetime_[9:11])) / 2
            if average_hour <= 9:
                average_hour = '0' + str(average_hour)
            current_time = datetime.now().isoformat()
            datetime_object = current_time[:11] + str(average_hour) + ':00:00'
            response = get_weather_summary_for_hour(datetime_object, coordinates)

        elif datetime_len == 25:
            # 2018-08-04T12:00:00+02:00
            response = get_weather_summary_for_day(datetime_object, coordinates)
            pass

        else:
            return get_weather_summary_no_datetime(coordinates)

    if not response:
        return 'weather.weather()_2'

    return str(response)
