from datetime import datetime, timedelta
import locale
import requests

# Set locale Indonesia
locale.setlocale(locale.LC_TIME, "id_ID.UTF-8")

API_KEY = "f215ccee5e991b682666bbef26a5c9a5"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def weather_forecast(city):
    weather_data = None
    params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "id"
        }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_list = data["list"]

        today = datetime.now().date()
        result = []

        for i in range(3):
            target_day = today + timedelta(days=i)

            temp_day = None
            temp_night = None
            icon_day = None

            for item in forecast_list:
                dt = datetime.fromtimestamp(item["dt"])

                if dt.date() == target_day:
                    temp_day = item["main"]["temp"]
                    icon_day = item["weather"][0]["icon"]

            result.append({
                "tanggal": target_day.strftime("%d %B %Y"),
                "hari": target_day.strftime("%A"),
                "suhu": temp_day,
                "icon": icon_day
            })

        weather_data = result
    return weather_data