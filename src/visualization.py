import pandas as pd
import matplotlib.pyplot as plt

# Read the cleaned air quality dataset
df = pd.read_csv("database/cleaned_air_quality.csv")

# ==========================================================
# 1. Bar Chart - Average PM2.5 by City
# ==========================================================

city_pm25 = df.groupby("city")["pm2_5"].mean()

plt.figure(figsize=(10, 6))
city_pm25.plot(kind="bar", color="skyblue")

plt.title("Average PM2.5 by City")
plt.xlabel("City")
plt.ylabel("Average PM2.5")

plt.tight_layout()
plt.savefig("images/average_pm25_by_city.png")
plt.show()


# ==========================================================
# 2. Line Chart - Maximum Ozone by City
# ==========================================================

city_ozone = df.groupby("city")["ozone"].max()

plt.figure(figsize=(10, 6))
city_ozone.plot(kind="line", color="green", marker="o")

plt.title("Maximum Ozone by City")
plt.xlabel("City")
plt.ylabel("Maximum Ozone")

plt.tight_layout()
plt.savefig("images/maximum_ozone_by_city.png")
plt.show()


# ==========================================================
# 3. Pie Chart - Average Percentage of Air Pollutants
# ==========================================================

labels = [
    "PM10",
    "PM2.5",
    "Carbon Monoxide",
    "Nitrogen Dioxide",
    "Sulphur Dioxide"
]

values = [
    df["pm10"].mean(),
    df["pm2_5"].mean(),
    df["carbon_monoxide"].mean(),
    df["nitrogen_dioxide"].mean(),
    df["sulphur_dioxide"].mean()
]

plt.figure(figsize=(8, 8))

plt.pie(
    values,
    labels=labels,
    colors=["green", "blue", "skyblue", "orange", "red"],
    autopct="%1.1f%%"
)

plt.title("Average Percentage of Air Pollutants")

plt.savefig("images/air_pollutants_percentage.png")
plt.show()


# ==========================================================
# 4. Histogram - Distribution of Dust Levels
# ==========================================================

plt.figure(figsize=(10, 6))

df["dust"].plot(kind="hist", color="green", bins=20)

plt.title("Distribution of Dust Levels")
plt.xlabel("Dust")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig("images/dust_distribution.png")
plt.show()


# ==========================================================
# 5. Scatter Plot - Humidity vs Temperature
# ==========================================================

plt.figure(figsize=(10, 6))

df.plot(
    kind="scatter",
    x="humidity",
    y="temperature",
    color="purple"
)

plt.title("Relationship Between Humidity and Temperature")
plt.xlabel("Humidity")
plt.ylabel("Temperature")

plt.tight_layout()
plt.savefig("images/humidity_vs_temperature.png")
plt.show()


# ==========================================================
# 6. Box Plot - PM2.5 Distribution by City
# ==========================================================

plt.figure(figsize=(10, 6))

df.boxplot(column="pm2_5", by="city")

plt.title("PM2.5 Distribution by City")
plt.suptitle("")
plt.xlabel("City")
plt.ylabel("PM2.5")

plt.tight_layout()
plt.savefig("images/pm25_distribution_by_city.png")
plt.show()