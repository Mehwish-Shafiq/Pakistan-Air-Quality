# Import required libraries
import pandas as pd
import numpy as np
import joblib
# Import train-test split function
from sklearn.model_selection import train_test_split
# Import RandomForestRegressor function
from sklearn.ensemble import RandomForestRegressor
# Import Linear Regression model
from sklearn.linear_model import LinearRegression
# Import GradientBoostingRegressor model
from sklearn.ensemble import GradientBoostingRegressor
# Import evaluation metrics
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score)


# Read the cleaned air quality dataset
df = pd.read_csv("database/cleaned_air_quality.csv")


# Define target variable (what we want to predict)
# Here we are predicting ozone level
y = df["ozone"]


# Define input features (factors used to predict ozone)
x = df[[
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide"
]]


# Split data into training and testing sets
# 80% data for training and 20% for testing
X_train, X_test, Y_train, Y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42
)


# Create Linear Regression model
model = LinearRegression()


# Train the model using training data
model.fit(X_train, Y_train)


# Generate predictions using test data
y_pred = model.predict(X_test)


# Calculate Mean Absolute Error (average prediction error)
mae = mean_absolute_error(Y_test, y_pred)
print("MAE:", mae)


# Calculate Mean Squared Error (squared prediction error)
mse = mean_squared_error(Y_test, y_pred)
print("MSE:", mse)


# Calculate Root Mean Squared Error
# RMSE is the square root of MSE and shows error in original units
rmse = np.sqrt(mse)
print("RMSE:", rmse)


# Calculate R2 Score
# Shows how well the model explains the variation in data
r_score = r2_score(Y_test, y_pred)
print("R2 Score:", r_score)

joblib.dump(model, "models/linear_regression_model.pkl")
LR_mae = mae
LR_mse = mse
LR_rmse = rmse
LR_r_score = r_score


#model 2 
print("Random Forest Regressor model")
# Target
y = df["ozone"]

# Features
x = df[
    [
        "pm10",
        "pm2_5",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide"
    ]
]

# Model
model = RandomForestRegressor(random_state=42)

# Split
X_train, X_test, Y_train, Y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# Train
model.fit(X_train, Y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(Y_test, y_pred)
print("MAE:", mae)

mse = mean_squared_error(Y_test, y_pred)
print("MSE:", mse)

rmse = np.sqrt(mse)
print("RMSE:", rmse)

r2 = r2_score(Y_test, y_pred)
print("R2 Score:", r2)

joblib.dump(model,"models/RandomForestRegressor.pkl")
RF_mae = mae
RF_mse = mse
RF_rmse = rmse
RF_r2 = r2


print("Gradient Boosting Regressor")
#model 3
# Target variable (what we want to predict)
y = df["ozone"]

# Feature variables (input columns)
x = df[[
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide"
]]

# Create the Gradient Boosting Regressor model
model = GradientBoostingRegressor()

# Split the dataset into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# Train the model using the training data
model.fit(X_train, Y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate Mean Absolute Error (MAE)
mae = mean_absolute_error(Y_test, y_pred)
print(mae)

# Calculate Mean Squared Error (MSE)
mse = mean_squared_error(Y_test, y_pred)
print(mse)

# Calculate Root Mean Squared Error (RMSE)
rmse = np.sqrt(mse)
print(rmse)

# Calculate R² Score
r_score = r2_score(Y_test, y_pred)
print(r_score)

joblib.dump(model,"models/GradientBoostingRegressor.pkl")
GB_mae = mae
GB_mse = mse
GB_rmse = rmse
GB_r_score = r_score

# Comparison of Models

LR_results = {
    "Model": "Linear Regression",
    "MAE": LR_mae,
    "MSE": LR_mse,
    "RMSE": LR_rmse,
    "R2 Score": LR_r_score
}

RF_results = {
    "Model": "Random Forest",
    "MAE": RF_mae,
    "MSE": RF_mse,
    "RMSE": RF_rmse,
    "R2 Score": RF_r2
}

GB_results = {
    "Model": "Gradient Boosting",
    "MAE": GB_mae,
    "MSE": GB_mse,
    "RMSE": GB_rmse,
    "R2 Score": GB_r_score
}

comparison = pd.DataFrame([
    LR_results,
    RF_results,
    GB_results
])

print(comparison)