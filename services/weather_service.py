import requests

def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=pt&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]
    return result['latitude'], result['longitude']


def get_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) +
        "&longitude=" + str(lon) +
        "&current_weather=true&hourly=temperature_2m"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()
