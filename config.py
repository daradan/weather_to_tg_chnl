import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


CITIES_CHANNEL = {'Астана': os.getenv('TG_CHANNEL_ASTANA'),
                  'Алматы': os.getenv('TG_CHANNEL_ALMATY')}
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')

URL_ONECALL = 'https://api.openweathermap.org/data/2.5/onecall'
URL_AIR_POLLUTION = 'http://api.openweathermap.org/data/2.5/air_pollution'
PARAMS_ONECALL = {'appid': os.getenv('API_ID'),
                  'units': 'metric',
                  'lang': 'ru',
                  'exclude': 'minutely,hourly'
                  }
PARAMS_AIR_POLLUTION = {'appid': os.getenv('API_ID')}
URL_HOLIDAYS = 'https://raw.githubusercontent.com/daradan/production_calendar_kz/main/kz_holidays_2.json'
