from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "df0e9ab964044bb70ee84b6c860177c0"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data['cod'] != 200:
            return None, data.get('message', 'City not found')

        weather = {
            'city':        data['name'],
            'country':     data['sys']['country'],
            'temp':        round(data['main']['temp']),
            'feels_like':  round(data['main']['feels_like']),
            'humidity':    data['main']['humidity'],
            'pressure':    data['main']['pressure'],
            'wind_speed':  data['wind']['speed'],
            'description': data['weather'][0]['description'].title(),
            'icon':        data['weather'][0]['icon'],
            'main':        data['weather'][0]['main'],
            'visibility':  round(data.get('visibility', 0) / 1000, 1),
            'sunrise':     datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p'),
            'sunset':      datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p'),
            'date':        datetime.now().strftime('%A, %B %d %Y'),
            'time':        datetime.now().strftime('%I:%M %p'),
        }
        return weather, None

    except Exception as e:
        return None, str(e)


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error   = None
    city    = ''

    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if city:
            weather, error = get_weather(city)
        else:
            error = 'Please enter a city name'

    return render_template('index.html', weather=weather, error=error, city=city)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)