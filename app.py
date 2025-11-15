from flask import Flask, render_template, request
from services.weather_service import get_cached_weather_data, CIDADE_PADRAO
import locale

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
    except locale.Error:
        pass

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    city_to_search = CIDADE_PADRAO

    if request.method == 'POST':
        city_from_form = request.form.get('city_name')
        if city_from_form:
            city_to_search = city_from_form

    weather_data = get_cached_weather_data(city_to_search)

    hourly_forecast = weather_data.get('hourly_forecast', [])
    
    chart_temps = [item['temp'] for item in hourly_forecast]
    chart_times = [item['time'] for item in hourly_forecast]

    return render_template(
        'index.html',
        **weather_data,
        chart_temps=chart_temps,
        chart_times=chart_times
    )

if __name__ == '__main__':
    app.run(debug=True)