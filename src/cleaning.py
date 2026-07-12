import pandas as pd
import numpy as np

# ==========================================
# Load Dataset
# ==========================================
df = pd.read_csv("database/pakistan_air_quality.csv")

# ==========================================
# Display First and Last 5 Rows
# ==========================================
print(df.head())
print(df.tail())

# ==========================================
# Check Data Types of All Columns
# ==========================================
print(df.dtypes)

# ==========================================
# Display Dataset Information
# ==========================================
df.info()

# ==========================================
# Check Dataset Shape (Rows, Columns)
# ==========================================
print(df.shape)

# ==========================================
# Display All Column Names
# ==========================================
print(df.columns)

# ==========================================
# Check Missing Values in Each Column
# ==========================================
print(df.isnull().sum())

# ==========================================
# Remove Missing Values (If Any)
# ==========================================
if df.isnull().sum().sum() == 0:
    print("No missing values found.")
else:
    df.dropna(inplace=True)
    print("Missing values removed.")

# ==========================================
# Fill Missing Values in PM2.5 using Mean
# ==========================================
if df.isnull().sum().sum() > 0:
    df["pm2_5"] = df["pm2_5"].fillna(df["pm2_5"].mean())
    print("Missing values filled.")
else:
    print("There is no need to fill missing values.")

# ==========================================
# Fill Missing Values in City using Mode
# ==========================================
df["city"] = df["city"].fillna(df["city"].mode()[0])

# ==========================================
# Fill Missing Values in Temperature using Mean
# ==========================================
df["temperature"] = df["temperature"].fillna(df["temperature"].mean())

# ==========================================
# Check Duplicate Records
# ==========================================
print(df.duplicated().sum())

duplicates = df.duplicated().sum()

# ==========================================
# Remove Duplicate Records (If Any)
# ==========================================
if duplicates > 0:
    df.drop_duplicates(inplace=True)
    print("Duplicate records removed.")
else:
    print("No duplicate records found.")

# ==========================================
# Check for Invalid Negative Values
# ==========================================
numerical_columns = df.select_dtypes(include="number")

if (numerical_columns < 0).any().any():
    print("Invalid negative values found.")
else:
    print("No invalid negative values found.")

# ==========================================
# Validate Temperature Range
# ==========================================
if ((df["temperature"] >= 0) & (df["temperature"] <= 100)).all():
    print("Temperature values are valid.")
else:
    print("Invalid temperature values found.")

# ==========================================
# Validate Wind Speed Values
# ==========================================
if (df["wind_speed"] > 0).all():
    print("Wind speed values are valid.")
else:
    print("Invalid wind speed values found.")

# ==========================================
# Save Cleaned Dataset
# ==========================================
df.to_csv("database/cleaned_air_quality.csv", index=False)

print("Cleaned dataset saved successfully.")