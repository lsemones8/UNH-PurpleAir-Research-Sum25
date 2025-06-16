# AirQuality_Cherokee_SD_data.py
# Description: Convert Purple Air csv dataset into code from SD card in Durham, NH, calculate the average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 over time.
# Multiple csv files were combined and sorted, and Universal time zone was converted into local, Central time.    
# Author: Logan Semones
# First Created: 06/11/2025

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

#df = pd.read_csv('last_500_timepoints.csv', parse_dates=['time_stamp']) # Convert csv file into usable table

### Original csv file with all values
#df = pd.read_csv('2019-01-01_2025-05-01_10-Minute_Average.csv', parse_dates=['time_stamp']) # Convert csv file into usable table
###

### Merge csv files into one single graph
file_list = ['20250610.csv', '20250611.csv', '20250611p2.csv', '20250612.csv', '20250613.csv', '20250614.csv','20250615.csv',
             '20250616p1.csv']  # Add as many as you need

dfs = [pd.read_csv(file) for file in file_list]
df = pd.concat(dfs, ignore_index=True)
###

# Convert Universal time zone into local (Central) time for Mississippi
# Make sure your UTC time column is datetime and timezone-aware
df['UTCDateTime'] = pd.to_datetime(df['UTCDateTime'], utc=True)

df['Eastern_time_stamp'] = pd.to_datetime(df['UTCDateTime']).dt.tz_convert('US/Eastern') 

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
df['pm2.5 AQI'] = df[['pm2.5_aqi_a_clean', 'pm2.5_aqi_b_clean']].mean(axis=1) # Takes the average pm2.5 values at each time point

# Plot
plt.plot(df['Eastern_time_stamp'], df['pm2.5 AQI'], label='pm2.5')
plt.xlabel('Time (Eastern)')
plt.ylabel('pm2.5 AQI')
plt.title('Average pm2.5 Air Quality Index (AQI) Over Time in Durham, NH')

# Coloring graph background, identifying Air Quality health categories
plt.axhspan(0, 50.5, facecolor='green', alpha=0.5)
plt.axhspan(50.5, 100.5, facecolor='yellow', alpha=0.5)
plt.axhspan(100.5, 150.5, facecolor='orange', alpha=0.7)
plt.axhspan(150.5, 200.5, facecolor='red', alpha=0.5)
plt.axhspan(200.5, 300.5, facecolor='purple', alpha=0.3)
plt.axhspan(300.5, 500, facecolor='purple', alpha=0.6)

# X-axis expansion (time-based)
x_min2 = min(df['Eastern_time_stamp'])
x_max2 = max(df['Eastern_time_stamp'])
x_range2 = x_max2 - x_min2
x_buffer2 = x_range2 * 0.1  # 10% on each side = 120% total
plt.xlim(x_min2 - x_buffer2, x_max2 + x_buffer2)

# Y-axis expansion (numerical)
y_min2 = 0
y_max2 = max(df['pm2.5 AQI'])
y_range2 = y_max2 - y_min2
y_buffer2 = y_range2 * 0.25
plt.ylim(y_min2, y_max2 + y_buffer2)

# Create patches that represent your colored areas
good_Patch2 = mpatches.Patch(color='green', alpha=0.5, label='Good (0–50)')
moderate_Patch2 = mpatches.Patch(color='yellow', alpha=0.5, label='Moderate (51–100)')
somewhatUnhealthy_Patch2 = mpatches.Patch(color='orange', alpha=0.7, label='Unhealthy for sensitive groups (101-150)')
unhealthy_Patch2 = mpatches.Patch(color='red', alpha=0.5, label='Unhealthy (151-200)')
veryUnhealthy_Patch2 = mpatches.Patch(color='purple', alpha=0.3, label='Very Unhealthy (201-300)')
hazardous_Patch2 = mpatches.Patch(color='purple', alpha=0.6, label='Hazardous (301-500)')

# Making legend to identify Air Quality Health categories
plt.legend(handles=[good_Patch2, moderate_Patch2, somewhatUnhealthy_Patch2, unhealthy_Patch2, veryUnhealthy_Patch2, hazardous_Patch2], loc = 'best')

plt.grid(True)
plt.show()


