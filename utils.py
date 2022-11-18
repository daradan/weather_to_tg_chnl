import time
import json
import requests

import config


def merge_responses(onecall: dict, air_population: dict) -> dict:
    merged_responses = onecall.copy()
    merged_responses.update(air_population)
    return merged_responses


def deg_to_compass(wind_deg):
    val = int((wind_deg / 22.5) + 0.5)
    text_compass = ['С', 'ССВ', 'СВ', 'ВСВ', 'В', 'ВЮВ', 'ЮВ', 'ЮЮВ', 'Ю', 'ЮЮЗ', 'ЮЗ', 'ЗЮЗ', 'З', 'ЗСЗ', 'СЗ', 'ССЗ']
    return text_compass[(val % 16)]


def make_emojies(icon: str):
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


def compare_time() -> bool:
    current_time = time.strftime('%H:%M')
    if current_time > '20:00':
        return True


def compare_temp(data: dict) -> str:
    compare_day = data['temp_max'] - data['temp_next_day_max']
    compare_day_str = str(compare_day * (1 if compare_day > 0 else -1))
    if compare_day < 0:
        compare_text = 'теплее'
    elif compare_day > 0:
        compare_text = 'холоднее'
    else:
        return f"Завтра 🌡️ {data['temp_next_day_max']}° 🌬️ {data['wind_speed_next']}м/с, как сегодня"
    return f"Завтра 🌡️ {data['temp_next_day_max']}° 🌬️ {data['wind_speed_next']}м/с, " \
           f"на {compare_day_str}° {compare_text}, чем сегодня"
    # if compare_day != 0:
    #     return f"Завтра 🌡️ {data['temp_next_day_max']}° 🌬️ {data['wind_speed_next']}м/с, " \
    #            f"на {compare_day_str}° {compare_text}, чем сегодня"
    # else:
    #     return f"Завтра 🌡️ {data['temp_next_day_max']}° 🌬️ {data['wind_speed_next']}м/с, как сегодня"


def make_text_to_tg(data: dict) -> str:
    text_to_tg = f"🌡 {data['temp_current']}° ({data['temp_feels_like']}°), " \
                 f"{data['icon']} {data['description']}, " \
                 f"🌬️ {data['wind_speed']}м/с - {data['wind_deg']}, " \
                 f"💧{data['humidity']}%\n" \
                 f"<b>AQI:</b> {data['aqi']}, " \
                 f"<b>SO2:</b> {data['so2']}, " \
                 f"<b>O3:</b> {data['o3']}, " \
                 f"<b>PM2.5:</b> {data['pm2_5']}, " \
                 f"<b>PM10:</b> {data['pm10']}"
    if not compare_time():
        return text_to_tg
    else:
        return compare_temp(data)


def send_msg(message, channel):
    url = f'https://api.telegram.org/bot{config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': channel,
        'text': message,
        'parse_mode': 'HTML',
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_msg(message, channel)


def send_error(message):
    url = f'https://api.telegram.org/bot{config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': config.TG_CHANNEL_ERROR,
        'text': message
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_error(message)
