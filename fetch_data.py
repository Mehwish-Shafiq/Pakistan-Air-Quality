import requests
import csv
import os
from datetime import datetime
from config import OPENWEATHER_API_KEY

# ---- Cities dictionary: name -> (latitude, longitude) ----
cities = {
    "Lahore": (31.5497, 74.3436),
    "Faisalabad": (31.4180, 73.0790),
    "Karachi": (24.8607, 67.0011),
    "Islamabad": (33.6844, 73.0479),
    "Multan": (30.1575, 71.5249),
    "Peshawar": (34.0151, 71.5249),
    "Quetta": (30.1798, 66.9750),
    "Rahim Yar Khan": (28.4202, 70.2952),
    "Rawalpindi": (33.5651, 73.0169),
    "Sialkot": (32.4945, 74.5229),
}


def get_air_quality_data(lat, lon):
    """Fetch pollutant data for one location from OpenWeather Air Pollution API."""
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        components = data["list"][0]["components"]

        pollutant_dict = {
            "pm10": components["pm10"],
            "pm2_5": components["pm2_5"],
            "carbon_monoxide": components["co"],
            "nitrogen_dioxide": components["no2"],
            "sulphur_dioxide": components["so2"],
            "ozone": components["o3"],
        }
        return pollutant_dict
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def get_season(month):
    """Roughly map month -> season (adjust to your local convention if needed)."""
    if month in (12, 1, 2):
        return "Winter"
    elif month in (3, 4, 5):
        return "Spring"
    elif month in (6, 7, 8):
        return "Summer"
    else:
        return "Autumn"


def get_time_features():
    """Generate the same time-based columns your historical dataset has."""
    now = datetime.now()

    return {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "hour": now.hour,
        "day_of_week": now.strftime("%A"),
        "month": now.month,
        "month_name": now.strftime("%B"),
        "year": now.year,
        "is_weekend": now.weekday() >= 5,  # Saturday=5, Sunday=6
        "season": get_season(now.month),
    }


def fetch_all_cities():
    """Loop through every city, fetch live data, and combine with time features."""
    all_rows = []

    for city, (lat, lon) in cities.items():
        pollutants = get_air_quality_data(lat, lon)

        if pollutants is not None:
            time_features = get_time_features()

            row = {
                "city": city,
                "latitude": lat,
                "longitude": lon,
                **pollutants,
                **time_features,
            }
            all_rows.append(row)
            print(f"Fetched: {city}")
        else:
            print(f"Skipped: {city} (request failed)")

    return all_rows


def save_to_csv(rows, filename="live_air_quality.csv"):
    """Append the fetched rows to a CSV file, matching your historical columns."""
    if not rows:
        print("No data to save.")
        return

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)

    print(f"Saved {len(rows)} rows to {filename}")


if __name__ == "__main__":
    data = fetch_all_cities()
    save_to_csv(data)