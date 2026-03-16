
import requests
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, jsonify

def get_weather(CITY):
    load_dotenv()
    api_key = os.getenv("API_KEY")
    # CITY = "Nashik"
    URL=f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={api_key}"

    response = requests.get(URL)
    data = response.json()

    if response.status_code == 200:
        data = response.json()
        temperature: float = data['main']['temp']-273.15  # Convert from Kelvin to Celsius
        temperature = round(temperature, 2)  # Round to 2 decimal places
        humidity: int = data['main']['humidity']
        description: str = data['weather'][0]['description']
        print(f"The current temperature in {CITY} is {temperature:.2f}°C.")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description}")
        return render_template('weather.html', city=CITY, temperature=temperature, humidity=humidity, description=description)
    else:
        print(f"Failed to retrieve weather data for {CITY}. Error code: {response.status_code}")
        return jsonify({"error": f"Failed to retrieve weather data for {CITY}. Error code: {response.status_code}"}), response.status_code
    
    

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET'])
def home():
        return render_template('index.html')

@flask_app.route('/weather', methods=['GET'])
def weather_route():
    CITY = request.args.get('city')
    return get_weather(CITY)

if __name__ == "__main__":
    flask_app.run(debug=True)

# The following commented code is not needed and can be removed or kept for reference.
# load_dotenv()
#     api_key = os.getenv("API_KEY")
#     CITY = "Nashik"
#     URL=f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={api_key}"

#     response = requests.get(URL)
#     data = response.json()

#     if response.status_code == 200:
#         data = response.json()
#         temperature = data['main']['temp']-273.15  # Convert from Kelvin to Celsius
#         humidity = data['main']['humidity']
#         description = data['weather'][0]['description']
#         print(f"The current temperature in {CITY} is {temperature:.2f}°C.")
#         print(f"Humidity: {humidity}%")
#         print(f"Description: {description}")
#     else:
#         print(f"Failed to retrieve weather data for {CITY}. Error code: {response.status_code}")