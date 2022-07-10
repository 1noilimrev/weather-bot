import os

import requests

BASE_URL = os.environ.get('BASE_URL')
API_KEY = os.environ.get('API_KEY')


def get_current(lat: float, ion: float):
    result = requests.get(f'{BASE_URL}/current', params={'lat': lat, 'lon': ion, 'api_key': API_KEY})
    return result.json()


def get_forecast_hourly(lat: float, ion: float, hour_offset: int):
    result = requests.get(f'{BASE_URL}/forecast/hourly',
                          params={'lat': lat, 'lon': ion, 'hour_offset': hour_offset, 'api_key': API_KEY})
    return result.json()


def get_historical_hourly(lat: float, ion: float, hour_offset: int):
    result = requests.get(f'{BASE_URL}/historical/hourly',
                          params={'lat': lat, 'lon': ion, 'hour_offset': hour_offset, 'api_key': API_KEY})
    return result.json()
