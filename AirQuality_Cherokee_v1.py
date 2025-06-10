# AirQuality_Cherokee_v1.py
# Description: Convert Purple Air csv dataset into code, calculate the
# average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 over time.   
# Author: Logan Semones
# First Created: 06/06/2025

import pandas as pd
import matplotlib.pyplot as plt

#df = pd.read_csv('last_500_timepoints.csv', parse_dates=['time_stamp']) # Convert csv file into usable table

### Original csv file with all values
df = pd.read_csv('2019-01-01_2025-05-01_10-Minute_Average.csv', parse_dates=['time_stamp']) # Convert csv file into usable table
###

### To initially decrease size of total csv file
# Slice the last 500 rows
# last_500 = df.tail(500)
#
# Save to a new CSV
# last_500.to_csv("last_500_timepoints.csv", index=False)
###

df['pm2.5 Avg'] = df[['pm2.5_atm_a', 'pm2.5_atm_b']].mean(axis=1) # Takes the average pm2.5 values at each time point

plt.plot(df['time_stamp'], df['pm2.5 Avg'], label='pm2.5')
plt.xlabel('Time')
plt.ylabel('pm2.5 AQI')
plt.title('Average pm2.5 Air Quality Index (AQI) Over Time')
plt.legend()
plt.grid(True)
plt.show()

