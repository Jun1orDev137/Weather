from flask import Flask, request, jsonify
import requests
from datetime import datetime


app = Flask(__name__)

API_KEY = "55ba9c2274c1473f97f122508242106"


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    api_url = f"http://api.weatherapi.com/v1/history.json"
    params = {
        'key': API_KEY,
        'q': city,
        'dt': date_from if date_from else datetime.now().date(),
        'end_dt': date_to if date_to else datetime.now().date()
    }

    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from weather service"}), 500

    data = response.json()
    # Парсинг данных
    forecast_days = data['forecast']['forecastday']
    if not forecast_days:
        return jsonify({"error": "No data available for the given dates"}), 404

    temperature_c = {
        "average": sum(day['day']['avgtemp_c'] for day in forecast_days) / len(forecast_days),
        "median": forecast_days[len(forecast_days) // 2]['day']['avgtemp_c'],
        "min": min(day['day']['mintemp_c'] for day in forecast_days),
        "max": max(day['day']['maxtemp_c'] for day in forecast_days)
    }

    weather_data = {
        "service": "weather",
        "data": {
            "temperature_c": temperature_c
        }
    }

    return jsonify(weather_data)


if __name__ == '__main__':
    app.run(debug=True)