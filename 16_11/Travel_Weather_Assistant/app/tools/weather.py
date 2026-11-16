
import requests
from datetime import date, timedelta


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(destination: str, start_date: date, end_date: date):

    # Step 1: Resolve destination using Geocoding API
    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={
                "name": destination,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=15
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

    except requests.RequestException as e:
        return {"error": f"Geocoding service unavailable: {e}"}

    results = geo_data.get("results", [])

    if not results:
        return {"error": f"Destination '{destination}' not found."}

    location = results[0]

    latitude = location["latitude"]
    longitude = location["longitude"]
    city = location["name"]
    country = location.get("country", "")

    # Step 2: Check forecast horizon
    today = date.today()
    last_forecast_date = today + timedelta(days=16)

    if start_date < today:
        return {"error": "Weather forecast is not available for past dates."}

    if end_date > last_forecast_date:
        return {
            "error": "Requested travel dates exceed the supported forecast horizon."
        }

    # Step 3: Fetch actual weather forecast
    try:
        weather_response = requests.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_sum"
                ),
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "timezone": "auto",
                "temperature_unit": "celsius"
            },
            timeout=20
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

    except requests.RequestException as e:
        return {"error": f"Weather service unavailable: {e}"}

    daily = weather_data.get("daily")

    if not daily or not daily.get("time"):
        return {"error": "Forecast data is unavailable for these dates."}

    # Step 4: Format forecast
    forecasts = []

    for i, forecast_date in enumerate(daily["time"]):
        forecasts.append({
            "date": forecast_date,
            "weather_code": daily["weather_code"][i],
            "temperature_max": daily["temperature_2m_max"][i],
            "temperature_min": daily["temperature_2m_min"][i],
            "precipitation_mm": daily["precipitation_sum"][i]
        })

    return {
        "destination": city,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
        "forecasts": forecasts
    }
