import requests
from flask import Flask, render_template, request
from datetime import datetime
import pytz 
import locale 

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

app = Flask(__name__)

DEFAULT_LAT = -23.55
DEFAULT_LON = -46.63
DEFAULT_CITY = "São Paulo"
DEFAULT_TIMEZONE = "America/Sao_Paulo"

def map_weather_code_to_icon(code, is_day):
    if code in [0]: return 'sunny' if is_day else 'clear_night'
    if code in [1, 2, 3]: return 'partly_cloudy_day' if is_day else 'partly_cloudy_night'
    if code in [45, 48]: return 'foggy'
    if code in [51, 53, 55, 56, 57]: return 'rainy_light'
    if code in [61, 63, 65, 66, 67]: return 'rainy'
    if code in [71, 73, 75, 77]: return 'snowing'
    if code in [80, 81, 82]: return 'thunderstorm_showers'
    if code in [85, 86]: return 'heavy_snow'
    if code in [95, 96, 99]: return 'thunderstorm'
    return 'cloud'

def map_weather_code_to_description(code):
    if code == 0: return 'Céu Limpo'
    if code == 1: return 'Principalmente Limpo'
    if code == 2: return 'Parcialmente Nublado'
    if code == 3: return 'Nublado'
    if code in [45, 48]: return 'Névoa'
    if code in [51, 53, 55]: return 'Chuvisco Fraco'
    if code in [61, 63, 65]: return 'Chuva'
    if code in [80, 81, 82]: return 'Aguaceiros'
    if code in [71, 73, 75]: return 'Neve'
    if code in [95, 96, 99]: return 'Trovoada'
    return 'Condição Desconhecida'

def geocode_city_name(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {'name': city_name, 'count': 1, 'language': 'pt', 'format': 'json'}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('results'):
            result = data['results'][0]
            return {
                'latitude': result['latitude'],
                'longitude': result['longitude'],
                'timezone': result.get('timezone', DEFAULT_TIMEZONE),
                'name': result.get('name', city_name)
            }
    except requests.exceptions.RequestException:
        pass
    
    return None

def get_weather_data_api(latitude, longitude, timezone, city_name):
    url = "https://api.open-meteo.com/v1/forecast"
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

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    current = data['current']
    is_day = current['is_day'] == 1
    current_code = current['weather_code']
    current_time = datetime.now(pytz.timezone(timezone)).strftime('%H:%M')

    current_data = {
        'temp': round(current['temperature_2m']),
        'icon': map_weather_code_to_icon(current_code, is_day),
        'condition': map_weather_code_to_description(current_code),
        'wind_speed': round(current['wind_speed_10m']),
        'humidity': round(current['relative_humidity_2m']),
        'pressure': round(current['pressure_msl']),
        'wind_direction': current['wind_direction_10m']
    }

    hourly = data['hourly']
    hourly_forecast = []
    
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    
    for i in range(len(hourly['time'])):
        hour_time_str = hourly['time'][i]
        hour_dt_naive = datetime.fromisoformat(hour_time_str)
        hour_dt = tz.localize(hour_dt_naive)
        
        if hour_dt >= now and len(hourly_forecast) < 8:
            hour_is_day = hour_dt.hour >= 6 and hour_dt.hour <= 20
            
            hourly_forecast.append({
                'time': hour_dt_naive.strftime('%H:%M'), 
                'icon': map_weather_code_to_icon(hourly['weather_code'][i], hour_is_day),
                'temp': round(hourly['temperature_2m'][i])
            })
    
    daily = data['daily']
    weekly_forecast = []
    
    for i in range(7):
        day_dt = datetime.fromisoformat(daily['time'][i])
        day_name = day_dt.strftime('%a')
        if i == 0: day_name = "Hoje"
        
        weekly_forecast.append({
            'day': day_name.capitalize().replace('.', ''),
            'icon': map_weather_code_to_icon(daily['weather_code'][i], True),
            'max_temp': round(daily['temperature_2m_max'][i]),
            'min_temp': round(daily['temperature_2m_min'][i]),
            'uv_index_max': round(daily['uv_index_max'][i]),
            'precipitation_prob': round(daily['precipitation_probability_max'][i])
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
            {'label': 'Prob. Chuva', 'icon': 'rainy', 'value': f"{current_day_data['precipitation_prob']}%"},
            {'label': 'Dir. Vento', 'icon': 'explore', 'value': f"{current_data['wind_direction']}°"},
        ]
    }
    
    return all_data

def get_weather_data(city_name):
    
    location_info = geocode_city_name(city_name)
    
    if location_info:
        try:
            return get_weather_data_api(
                location_info['latitude'], 
                location_info['longitude'], 
                location_info['timezone'], 
                location_info['name']
            )
        except requests.exceptions.RequestException:
            pass 
    
    try:
        return get_weather_data_api(DEFAULT_LAT, DEFAULT_LON, DEFAULT_TIMEZONE, DEFAULT_CITY)
    except Exception:
        error_data = {
            'city_data': {'city': 'Erro de Conexão', 'last_updated': datetime.now().strftime('%H:%M')},
            'current': {'temp': 'N/A', 'icon': 'error', 'condition': 'Não foi possível carregar dados.', 'wind_speed': 0, 'humidity': 0},
            'hourly_forecast': [],
            'weekly_forecast': [],
            'bottom_widgets': [{'label': 'Erro', 'icon': 'error', 'value': 'N/A'}] * 6
        }
        return error_data

@app.route('/', methods=['GET', 'POST'])
def index():
    city_to_search = DEFAULT_CITY

    if request.method == 'POST':
        city_from_form = request.form.get('city_name')
        if city_from_form:
            city_to_search = city_from_form
        
    data = get_weather_data(city_to_search)
    
    temperatures = [item['temp'] for item in data.get('hourly_forecast', [])]
    times = [item['time'] for item in data.get('hourly_forecast', [])]
    
    return render_template(
        'index.html', 
        **data, 
        chart_temps=temperatures, 
        chart_times=times
    )

if __name__ == '__main__':
    app.run(debug=True)