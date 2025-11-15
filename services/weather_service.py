import requests
import pytz
import time
from datetime import datetime
from services.api_client import geocode_city, fetch_weather_data
from services.mapping import map_code_to_icon, map_code_to_description

LATITUDE_PADRAO = -23.55
LONGITUDE_PADRAO = -46.63
CIDADE_PADRAO = "São Paulo"
FUSO_PADRAO = "America/Sao_Paulo"
EXPIRACAO_CACHE_SEGUNDOS = 300

DEFAULT_CITY = CIDADE_PADRAO

cache = {}

def get_error_data(city_name):
    return {
        'city_data': {'city': city_name.title(), 'last_updated': datetime.now().strftime('%H:%M')},
        'current': {'temp': 'N/A', 'icon': 'error', 'condition': 'Não foi possível carregar dados.', 'wind_speed': 0, 'humidity': 0, 'pressure': 0, 'wind_direction': 0},
        'hourly_forecast': [],
        'weekly_forecast': [],
        'bottom_widgets': [{'label': 'Erro', 'icon': 'error', 'value': 'N/A'}] * 6
    }

def process_weather_data(api_data, city_name, timezone):
    current = api_data['current']
    is_day = current['is_day'] == 1
    current_code = current['weather_code']
    current_time = datetime.now(pytz.timezone(timezone)).strftime('%H:%M')

    current_data = {
        'temp': round(current['temperature_2m']),
        'icon': map_code_to_icon(current_code, is_day),
        'condition': map_code_to_description(current_code),
        'wind_speed': round(current['wind_speed_10m']),
        'humidity': round(current['relative_humidity_2m']),
        'pressure': round(current['pressure_msl']),
        'wind_direction': current['wind_direction_10m']
    }

    hourly = api_data['hourly']
    hourly_forecast = []
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)

    for i in range(len(hourly['time'])):
        time_str = hourly['time'][i]
        time_dt_naive = datetime.fromisoformat(time_str)
        time_dt = tz.localize(time_dt_naive)

        if time_dt >= now and len(hourly_forecast) < 7:
            hour_is_day = time_dt.hour >= 6 and time_dt.hour <= 20

            hourly_forecast.append({
                'time': time_dt_naive.strftime('%H:%M'),
                'icon': map_code_to_icon(hourly['weather_code'][i], hour_is_day),
                'temp': round(hourly['temperature_2m'][i]),
                'condition': map_code_to_description(hourly['weather_code'][i])
            })

    daily = api_data['daily']
    weekly_forecast = []

    for i in range(7):
        day_name = datetime.fromisoformat(daily['time'][i]).strftime('%a')
        if i == 0: day_name = "Hoje"

        weekly_forecast.append({
            'day': day_name.capitalize().replace('.', ''),
            'icon': map_code_to_icon(daily['weather_code'][i], True),
            'max_temp': round(daily['temperature_2m_max'][i]),
            'min_temp': round(daily['temperature_2m_min'][i]),
            'uv_index_max': round(daily['uv_index_max'][i]),
            'precipitation_probability': round(daily['precipitation_probability_max'][i]),
            'condition': map_code_to_description(daily['weather_code'][i])
        })

    current_day_data = weekly_forecast[0]

    all_data = {
        'city_data': {
            'city': city_name.title(),
            'last_updated': current_time
        },
        'current': current_data,
        'hourly_forecast': hourly_forecast,
        'weekly_forecast': weekly_forecast,
        'bottom_widgets': [
            {'label': 'Vento', 'icon': 'air', 'value': f"{current_data['wind_speed']} km/h"},
            {'label': 'Umidade', 'icon': 'water_drop', 'value': f"{current_data['humidity']}%"},
            {'label': 'Pressão', 'icon': 'thermostat', 'value': f"{current_data['pressure']} hPa"},
            {'label': 'Máx UV (Dia)', 'icon': 'wb_incandescent', 'value': f"{current_day_data['uv_index_max']}"},
            {'label': 'Prob. Chuva', 'icon': 'rainy', 'value': f"{current_day_data['precipitation_probability']}%"},
            {'label': 'Dir. Vento', 'icon': 'explore', 'value': f"{current_data['wind_direction']}°"},
        ]
    }
    return all_data

def get_weather_data(city_name):
    location_info = geocode_city(city_name)
    is_default = False

    if not location_info:
        location_info = {
            'latitude': LATITUDE_PADRAO,
            'longitude': LONGITUDE_PADRAO,
            'timezone': FUSO_PADRAO,
            'name': CIDADE_PADRAO
        }
        is_default = True

    try:
        api_data = fetch_weather_data(
            location_info['latitude'],
            location_info['longitude'],
            location_info['timezone']
        )
        return process_weather_data(api_data, location_info['name'], location_info['timezone'])
    except requests.exceptions.RequestException:
        if is_default:
            return get_error_data(city_name)
        return get_weather_data(CIDADE_PADRAO)

def get_cached_weather_data(city_name):
    now = time.time()

    if city_name in cache:
        data, cache_time = cache[city_name]
        if now - cache_time < EXPIRACAO_CACHE_SEGUNDOS:
            return data

    data = get_weather_data(city_name)
    cache[city_name] = (data, now)

    return data