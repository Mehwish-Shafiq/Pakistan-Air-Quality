import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("database/pakistan_air_quality.csv")

# ==========================
# Dataset Overview
# ==========================
print(df.head(5))
print(df.tail(5))
print(df.columns)
print(df.dtypes)
df.info()
print(df.shape)

# ==========================
# Statistical Summary
# ==========================
print(df.describe())

print("ozone mean:", df["ozone"].mean())
print("pm10 mean:", df["pm10"].mean())
print("pm2_5 mean:", df["pm2_5"].mean())
print("carbon_monoxide mean:", df["carbon_monoxide"].mean())
print("nitrogen_dioxide mean:", df["nitrogen_dioxide"].mean())
print("sulphur_dioxide mean:", df["sulphur_dioxide"].mean())
print("dust mean:", df["dust"].mean())
print("temperature mean:", df["temperature"].mean())
print("humidity mean:", df["humidity"].mean())

print("ozone median:", df["ozone"].median())
print("ozone mode:", df["ozone"].mode())
print("ozone min:", df["ozone"].min())
print("ozone max:", df["ozone"].max())
print("ozone std:", df["ozone"].std())
print("ozone var:", df["ozone"].var())

# ==========================
# Data Quality Check
# ==========================
print(df.isnull().sum())
print(df.duplicated().sum())

if (df["pm10"] >= 0).all():
    print("Valid values in PM10")
else:
    print("Invalid values in PM10")

# ==========================
# Categorical Analysis
# ==========================
print(df["city"].value_counts())
print(df["city"].unique())

print(df["aqi_category"].value_counts())
print(df["aqi_category"].unique())

print(df["ozone"].unique())

# ==========================
# GroupBy Analysis
# ==========================
print(df.groupby("city")["pm2_5"].mean())

print(df.groupby("city")["humidity"].mean())

print(df.groupby("city")["pm2_5"].min())

print(df.groupby("city")["humidity"].min())

# ==========================
# Filtering Analysis
# ==========================

# Cities having Very Unhealthy AQI
very_unhealthy = df[df["aqi_category"] == "Very Unhealthy"]
print(very_unhealthy.groupby("city").size())

# City having maximum wind speed
max_speed = df["wind_speed"].max()
max_speed_city = df[df["wind_speed"] == max_speed]
print(max_speed_city.groupby("city").size())

# Month having minimum humidity
min_humidity = df["humidity"].min()
month_min_humidity = df[df["humidity"] == min_humidity]
print(month_min_humidity.groupby("month_name").size())

# City having maximum dust
highest_dust = df["dust"].max()
highest_dust_city = df[df["dust"] == highest_dust]
print(highest_dust_city.groupby("city").size())

# ==========================
# Correlation Analysis
# ==========================
print(df[["pm10", "pm2_5"]].corr())

print(df[["ozone", "dust"]].corr())

# ==========================
# Sorting & Ranking
# ==========================

# Top 5 cities with highest average PM2.5
print(df.groupby("city")["pm2_5"].mean().sort_values(ascending=False).head(5))

# Months sorted by average ozone level
print(df.groupby("month_name")["ozone"].mean().sort_values().head())

# ==========================
# Datetime Conversion
# ==========================
df["timestamp"] = pd.to_datetime(df["timestamp"])