import requests
import datetime

# All 25 districts of Sri Lanka with coordinates
SRI_LANKA_LOCATIONS = {
    "Ampara": (7.2985, 81.6747),
    "Anuradhapura": (8.3114, 80.4037),
    "Badulla": (6.9934, 81.0550),
    "Batticaloa": (7.7170, 81.7000),
    "Colombo": (6.9271, 79.8612),
    "Galle": (6.0535, 80.2210),
    "Gampaha": (7.0917, 80.0000),
    "Hambantota": (6.1241, 81.1185),
    "Jaffna": (9.6615, 80.0255),
    "Kalutara": (6.5854, 79.9607),
    "Kandy": (7.2906, 80.6337),
    "Kegalle": (7.2513, 80.3464),
    "Kilinochchi": (9.3803, 80.3770),
    "Kurunegala": (7.4863, 80.3647),
    "Mannar": (8.9810, 79.9044),
    "Matale": (7.4675, 80.6234),
    "Matara": (5.9549, 80.5550),
    "Monaragala": (6.8728, 81.3507),
    "Mullaitivu": (9.2671, 80.8120),
    "Nuwara Eliya": (6.9497, 80.7891),
    "Polonnaruwa": (7.9403, 81.0188),
    "Puttalam": (8.0362, 79.8283),
    "Ratnapura": (6.6828, 80.3992),
    "Trincomalee": (8.5874, 81.2152),
    "Vavuniya": (8.7514, 80.4971),
}


def get_mock_weather() -> dict:
    """Fallback mock weather data based on realistic Sri Lanka conditions."""
    base_hour = datetime.datetime.now().hour
    times = [f"2024-01-01T{(base_hour + i) % 24:02d}:00" for i in range(24)]
    temps  = [27,26,26,25,25,26,27,29,31,33,34,35,35,34,33,32,31,30,29,28,28,27,27,27]
    humids = [82,83,84,85,85,83,80,76,72,68,65,63,62,63,65,68,72,76,79,81,82,83,83,82]
    return {
        "current": {
            "temperature_c": temps[base_hour % 24],
            "humidity": humids[base_hour % 24],
            "apparent_temp_c": temps[base_hour % 24] + 2,
        },
        "hourly": {
            "times": times,
            "temperatures": temps,
            "humidities": humids,
        },
        "is_mock": True,
    }


def get_weather(lat: float, lon: float) -> dict:
    """
    Fetch current temperature, humidity, and 24-hour forecast
    from Open-Meteo API (free, no API key required).
    Falls back to realistic Sri Lanka mock data if API is unreachable.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature"],
        "hourly": ["temperature_2m", "relative_humidity_2m"],
        "forecast_days": 1,
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current"]
        hourly = data["hourly"]
        return {
            "current": {
                "temperature_c": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "apparent_temp_c": current["apparent_temperature"],
            },
            "hourly": {
                "times": hourly["time"],
                "temperatures": hourly["temperature_2m"],
                "humidities": hourly["relative_humidity_2m"],
            },
            "is_mock": False,
        }
    except Exception:
        return get_mock_weather()
