# AirQuality_Cherokee_SD_data.py
# Description: Convert Purple Air csv dataset into code from SD card, calculate the average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 over time.
# Multiple csv files were combined and sorted, and Universal time zone was converted into local, Central time.    
# Author: Logan Semones
# First Created: 06/11/2025

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#df = pd.read_csv('last_500_timepoints.csv', parse_dates=['time_stamp']) # Convert csv file into usable table

### Original csv file with all values
#df = pd.read_csv('2019-01-01_2025-05-01_10-Minute_Average.csv', parse_dates=['time_stamp']) # Convert csv file into usable table
###

### Merge csv files into one single graph
df1 = pd.read_csv('20250610.csv', parse_dates=['UTCDateTime'])
df2 = pd.read_csv('20250611.csv', parse_dates=['UTCDateTime'])
df3 = pd.read_csv('20250611p2.csv', parse_dates=['UTCDateTime'])
df1combo = df1.merge(df2, how='outer')
df = df1combo.merge(df3, how ='outer')
###

# Convert Universal time zone into local (Central) time for Mississippi
# Make sure your UTC time column is datetime and timezone-aware
df['UTCDateTime'] = pd.to_datetime(df['UTCDateTime'], utc=True)

df['Central_time_stamp'] = pd.to_datetime(df['UTCDateTime']).dt.tz_convert('US/Central') 

### To initially decrease size of total csv file
# Slice the last 500 rows
# last_500 = df.tail(500)
#
# Save to a new CSV file
# last_500.to_csv("last_500_timepoints.csv", index=False)
###

# Replace values > 500 with NaN
df['pm2.5_aqi_a_clean'] = df['pm2.5_aqi_atm'].where(df['pm2.5_aqi_atm'] <= 500, np.nan) 
df['pm2.5_aqi_b_clean'] = df['pm2.5_aqi_atm_b'].where(df['pm2.5_aqi_atm_b'] <= 500, np.nan)

# Calculate row-wise average of the cleaned columns
df['pm2.5 Avg'] = df[['pm2.5_aqi_a_clean', 'pm2.5_aqi_b_clean']].mean(axis=1) # Takes the average pm2.5 values at each time point

# Plot
plt.plot(df['Central_time_stamp'], df['pm2.5 Avg'], label='pm2.5')
plt.xlabel('Time')
plt.ylabel('pm2.5 AQI')
plt.title('Average pm2.5 Air Quality Index (AQI) Over Time')
plt.legend()
plt.grid(True)
plt.show()

