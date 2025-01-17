# -*- coding: utf-8 -*-
"""Climate change analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wGKbR5nZryXTp4ekcchwzEPvwzw0IHSu

# **important libraries**
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

"""# **Read the data**"""

df = pd.read_csv('/content/Africa_climate_change.csv')
df

"""# **Check on data types of data set and no of col and rows**

"""

print(df.dtypes)

#updating date column data type
df['DATE'] = pd.to_datetime(df['DATE'])

print(df.dtypes)

#checking data details


num_rows = len(df)

num_columns = len(df.columns)

print(num_rows,num_columns)

"""# **check missing values**"""

missing_values = df.isnull().sum()
print(missing_values)
# detect the %
missing_percentage = df.isnull().sum() / len(df) * 100
print(missing_percentage)

"""# from this we deduce that
-first column has missing values is PRCP
-second is TMIN
-Third is TMAX

# **Imputing**
"""

df_statistics = df.describe()
print(df_statistics)

TMIN_skewness = df['TMIN'].skew()
print(TMIN_skewness)

"""# impute with median due to the left sekewed data"""

prcp_skewness = df['PRCP'].skew()
print(prcp_skewness)

"""# impute with mean due to the deep right sekwenss value"""

mean_prcp=df['PRCP'].mean()
print(mean_prcp)

df['PRCP'] = df['PRCP'].fillna(mean_prcp)
print(df['PRCP'])

TMIN_skewness = df['TMIN'].skew()
print(TMIN_skewness)

"""# impute tmin with median due to the left sekewed"""

median_TMIN = df['TMIN'].median()
print(median_TMIN)
df['TMIN'] = df['TMIN'].fillna(median_TMIN)

TMAX_skewness = df['TMAX'].skew()
print(TMAX_skewness)

"""# impute with median due to left sekwed"""

median_TMAX = df['TMAX'].median()
print(median_TMAX)
df['TMAX'] = df['TMAX'].fillna(median_TMAX)

"""# impute TAVG with mode dur to the small ratio of NAN"""

mode_TAVG = df['TAVG'].mode()[0]
print(mode_TAVG)
df['TAVG'] = df['TAVG'].fillna(mode_TAVG)

"""# check the imputation effect on percentages"""

missing_percentage = df.isnull().sum() / len(df) * 100
print(missing_percentage)

"""# Encoding the country column to high the sensitivity towards any changes in the data"""

df_encoded = pd.get_dummies(df, columns=['COUNTRY'], drop_first=True)

print(df_encoded)

"""# Separete the target and other variables to highlight the meaning of the relation between data set`s columns

"""

X = df_encoded.drop('TAVG', axis=1)  # Features
y = df_encoded['TAVG']  #target

"""# split the data

"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""# converting date column to numeric"""

X_train['DATE'] = X_train['DATE'].astype('datetime64[ns]').astype('int64')
X_test['DATE'] = X_test['DATE'].astype('datetime64[ns]').astype('int64')

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

"""# Evaluating the model"""

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual TAVG")
plt.ylabel("Predicted TAVG")
plt.title("Actual vs Predicted TAVG")
plt.show()

residuals = y_test - y_pred
plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.xlabel("Predicted TAVG")
plt.ylabel("Residuals")
plt.title("Residuals vs Predicted TAVG")
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

"""#detect the MSE"""

mse = mean_squared_error(y_test, y_pred)
print(f"MSE: {mse}")

"""# Detect the baseline MSE  model"""

from sklearn.dummy import DummyRegressor
dummy_model = DummyRegressor(strategy="mean")
dummy_model.fit(X_train, y_train)
y_dummy_pred = dummy_model.predict(X_test)
baseline_mse = mean_squared_error(y_test, y_dummy_pred)
print(f'Baseline MSE: {baseline_mse}')