import requests

import config
import utils
import geolocator


class OpenWeatherAPI:
    def __init__(self):
        ...

    def start(self):
        if utils.is_holiday() and not utils.compare_time('09:00'):
            return
        try:
            for city in config.CITIES_CHANNEL.keys():
                latitude, longitude = geolocator.check_geolocator(city)
                response = self.get_response(latitude, longitude)
                data_parsed = self.parse_data(response)
                text_to_tg = utils.make_text_to_tg(data_parsed)
                utils.send_msg(text_to_tg, config.CITIES_CHANNEL[city])
        except Exception as e:
            utils.send_error(f"Weather: {e}")

    def get_response(self, latitude: float, longitude: float) -> dict:
        params_onecall = config.PARAMS_ONECALL
        params_onecall['lat'] = latitude
        params_onecall['lon'] = longitude
        response_onecall = requests.get(config.URL_ONECALL, params=params_onecall).json()

        params_air_population = config.PARAMS_AIR_POLLUTION
        params_air_population['lat'] = latitude
        params_air_population['lon'] = longitude
        response_air_population = requests.get(config.URL_AIR_POLLUTION, params=params_air_population).json()

        return utils.merge_responses(response_onecall, response_air_population)

    def parse_data(self, response: dict) -> dict:
        data_parsed = {
            'temp_current': round(response['current']['temp']),
            'temp_feels_like': round(response['current']['feels_like']),
            'temp_max': round(response['daily'][0]['temp']['max']),
            'temp_next_day_max': round(response['daily'][1]['temp']['max']),
            'humidity': response['current']['humidity'],
            'wind_speed': round(response['current']['wind_speed']),
            'wind_speed_next': round(response['daily'][1]['wind_speed']),
            'wind_deg': utils.deg_to_compass(response['current']['wind_deg']),
            'sunrise': response['current']['sunrise'],
            'sunset': response['current']['sunset'],
            'description': response['current']['weather'][0]['description'],
            'description_next': response['daily'][1]['weather'][0]['description'],
            'icon': utils.make_emojies(response['current']['weather'][0]['icon']),
            'icon_next': utils.make_emojies(response['daily'][1]['weather'][0]['icon']),
            'aqi': round(response['list'][0]['main']['aqi']),
            'co': round(response['list'][0]['components']['co']),
            'no': round(response['list'][0]['components']['no']),
            'no2': round(response['list'][0]['components']['no2']),
            'o3': round(response['list'][0]['components']['o3']),
            'so2': round(response['list'][0]['components']['so2']),
            'pm2_5': round(response['list'][0]['components']['pm2_5']),
            'pm10': round(response['list'][0]['components']['pm10']),
            'nh3': round(response['list'][0]['components']['nh3']),
        }
        return data_parsed


if __name__ == '__main__':
    OpenWeatherAPI().start()
