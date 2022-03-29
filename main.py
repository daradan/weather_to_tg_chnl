import requests
import json
import time


class OpenWeatherMap:

    def __init__(self):
        ### OpenWeatherMap config
        # 0=Астана, 1=Алматы, 2=Тараз,
        self.cities = [
            {
                'latitude': '51.09744581291194',
                'longitude': '71.45051590881198'
            },
            {
                'latitude': '43.2140510019299',
                'longitude': '76.85050814809058'
            },
            {
                'latitude': '42.883465',
                'longitude': '71.303688'
            },
        ]
        self.appid = 'XXXXXXXXXXXXXXXXXXXX' ### указать API от OpenWeatherMap
        self.exclude = 'minutely,hourly'
        self.units = 'metric'
        self.lang = 'ru'
        self.url_onecall = 'https://api.openweathermap.org/data/2.5/onecall'
        self.url_air_population = 'http://api.openweathermap.org/data/2.5/air_pollution'
        self.params_onecall = {
            'appid': self.appid,
            'units': self.units,
            'lang': self.lang,
            'exclude': self.exclude,
        }

        ### Telegram config
        self.token = 'XXXXXXXXXXXXXXXXXXXX' ### указать API от Telegram бота, у которого есть доступ администратора к каналу
        self.tg_url = 'https://api.telegram.org/bot'
        self.channels = ['@pogodaNQZ', '@pogodaALA', '@pogodaDMB']

    def make_url_for_api(self, city):
        dict_json_data = {}
        self.params_onecall['lat'] = city['latitude']
        self.params_onecall['lon'] = city['longitude']

        # не смог победить %2C вместо запятой в self.exclude, поэтому как временное решение пришлось сделать так
        url_temp_onecall = requests.get(self.url_onecall, params=self.params_onecall).url
        url_onecall = url_temp_onecall.replace('%2C', ',')

        params_air_population = {
            'lat': city['latitude'],
            'lon': city['longitude'],
            'appid': self.appid,
        }

        dict_json_data['onecall'] = json.loads(requests.get(url_onecall).text)
        dict_json_data['air_population'] = json.loads(requests.get(self.url_air_population, params=params_air_population).text)

        return dict_json_data

    def parse_data(self, json_data_onecall, json_data_air_population):
        data_parsed = {
            'temp_current': round(json_data_onecall['current']['temp']),
            'temp_feels_like': round(json_data_onecall['current']['feels_like']),
            'temp_max': round(json_data_onecall['daily'][0]['temp']['max']),
            'temp_next_day_max': round(json_data_onecall['daily'][1]['temp']['max']),
            'humidity': json_data_onecall['current']['humidity'],
            'wind_speed': round(json_data_onecall['current']['wind_speed']),
            'wind_deg': json_data_onecall['current']['wind_deg'],
            'sunrise': json_data_onecall['current']['sunrise'],
            'sunset': json_data_onecall['current']['sunset'],
            'description': json_data_onecall['current']['weather'][0]['description'],
            'wind_speed_next': round(json_data_onecall['daily'][1]['wind_speed']),
            'icon': json_data_onecall['current']['weather'][0]['icon'],
            'co': round(json_data_air_population['list'][0]['components']['co']),
            'no': round(json_data_air_population['list'][0]['components']['no']),
            'no2': round(json_data_air_population['list'][0]['components']['no2']),
            'o3': round(json_data_air_population['list'][0]['components']['o3']),
            'so2': round(json_data_air_population['list'][0]['components']['so2']),
            'pm2_5': round(json_data_air_population['list'][0]['components']['pm2_5']),
            'pm10': round(json_data_air_population['list'][0]['components']['pm10']),
            'nh3': round(json_data_air_population['list'][0]['components']['nh3']),
        }

        return data_parsed

    def deg_to_compass(self, wind_deg):
        val = int((wind_deg / 22.5) + 0.5)
        text_compass = ['С', 'ССВ', 'СВ', 'ВСВ', 'В', 'ВЮВ', 'ЮВ', 'ЮЮВ', 'Ю', 'ЮЮЗ', 'ЮЗ', 'ЗЮЗ', 'З', 'ЗСЗ', 'СЗ', 'ССЗ']

        return text_compass[(val % 16)]

    def get_emojies(self, icon):
        if '01' in icon:
            return '☀️'
        if '02' in icon:
            return '🌤️'
        if '03' in icon or '04' in icon:
            return '☁️'
        if '09' in icon:
            return '🌧️'
        if '10' in icon:
            return '🌦️'
        if '11' in icon:
            return '🌩️'
        if '13' in icon:
            return '🌨️'
        if '50' in icon:
            return '🌫️'
        else:
            return ''

    def compare_time(self):
        current_time = time.strftime('%H:%M')
        if current_time > '20:00':
            return True

    def make_text_to_tg(self, data_parsed):
        if self.compare_time() != True:
            text_to_tg = f'''🌡️ {data_parsed['temp_current']}° ({data_parsed['temp_feels_like']}°), \
{self.get_emojies(data_parsed['icon'])} {data_parsed['description']}, \
🌬️ {data_parsed['wind_speed']}м/с - {self.deg_to_compass(data_parsed['wind_deg'])}, \
💧 {data_parsed['humidity']}%
<b>SO2:</b> {data_parsed['so2']}, \
<b>O3:</b> {data_parsed['o3']}, \
<b>PM2.5:</b> {data_parsed['pm2_5']}, \
<b>PM10:</b> {data_parsed['pm10']}
'''
            ### <b>CO:</b> {data_parsed['co']}, \
            ### <b>NO:</b> {data_parsed['no']}, \
            ### <b>NO2:</b> {data_parsed['no2']}, \
            ### <b>NH3:</b> {data_parsed['nh3']}
        else:
            temp_max = data_parsed['temp_current']
            temp_max_next = data_parsed['temp_next_day_max']
            compare_day = temp_max - temp_max_next
            compare_day_str = str(compare_day * (1 if compare_day > 0 else -1))
            if compare_day < 0:
                compare_text = 'теплее'
            elif compare_day > 0:
                compare_text = 'холоднее'
            if compare_day != 0:
                text_to_tg = f'Завтра 🌡️ {temp_max_next}° 🌬️ {data_parsed["wind_speed_next"]}м/с, \
на {compare_day_str}° {compare_text}, чем сегодня'
            else:
                text_to_tg = f'Завтра 🌡️ {temp_max_next}° 🌬️ {data_parsed["wind_speed_next"]}м/с, как сегодня'

        return text_to_tg

    def send_telegram(self, text_to_tg, channel):
        url = f'{self.tg_url}{self.token}/sendMessage'
        data = {
            'chat_id': channel,
            'text': text_to_tg,
            'parse_mode': 'HTML',
        }

        r = requests.post(url, data=data)

    def main_func(self):
        n = 0
        for city in self.cities:
            data_json = self.make_url_for_api(city)
            data_parsed = self.parse_data(data_json['onecall'], data_json['air_population'])
            text_to_tg = self.make_text_to_tg(data_parsed)
            self.send_telegram(text_to_tg, self.channels[n])
            n += 1


if __name__ == '__main__':
    OpenWeatherMap().main_func()
