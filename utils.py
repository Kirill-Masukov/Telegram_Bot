import requests
from config import weather_token


def api_weather(city):
    link = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={weather_token}&units=metric")
    data = link.json()
    return data


def save_history(text):
    with open('history.txt', 'a', encoding='utf-16') as file:
        file.write(text + '\n')
