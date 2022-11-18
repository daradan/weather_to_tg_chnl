import json
import os
from geopy.geocoders import Nominatim
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_lat_long(city: str) -> dict:
    geolocator = Nominatim(user_agent=os.getenv('USER_AGENT'))
    location = geolocator.geocode(city)
    data = {city.lower(): [location.latitude, location.longitude]}
    return data


def add_city(data_prev: dict, city: str) -> list:
    city_with_geo = get_lat_long(city)
    data_prev.update(city_with_geo)
    with open('geolocator.json', 'w', encoding='utf-8') as file:
        json.dump(data_prev, file, ensure_ascii=False)
    return city_with_geo[city.lower()]


def check_geolocator(city: str) -> list:
    if not os.path.exists('geolocator.json'):
        return add_city({}, city)
    with open('geolocator.json', encoding='utf-8') as file:
        data = json.load(file)
        if city.lower() in data.keys():
            return data[city.lower()]
        return add_city(data, city)


if __name__ == '__main__':
    print(check_geolocator('Жанатас'))
