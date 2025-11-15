import requests

URL_API_CLIMA = "https://api.open-meteo.com/v1/forecast"
URL_API_GEO = "https://geocoding-api.open-meteo.com/v1/search"

def geocode_city(city_name):
    params = {'name': city_name, 'count': 1, 'language': 'pt', 'format': 'json'}

    try:
        response = requests.get(URL_API_GEO, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('results'):
            return data['results'][0]
    except requests.exceptions.RequestException:
        pass
    return None

def fetch_weather_data(latitude, longitude, timezone):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'timezone': timezone,
        'current': ['temperature_2m', 'relative_humidity_2m', 'is_day', 'weather_code', 'wind_speed_10m', 'wind_direction_10m', 'pressure_msl'],
        'hourly': ['temperature_2m', 'weather_code'],
        'daily': ['weather_code', 'temperature_2m_max', 'temperature_2m_min', 'uv_index_max', 'precipitation_probability_max'],
        'forecast_days': 7,
        'models': 'best_match'
    }

    response = requests.get(URL_API_CLIMA, params=params)
    response.raise_for_status()
    return response.json()