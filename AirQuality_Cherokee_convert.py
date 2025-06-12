# AirQuality_Cherokee_convert.py
# Description: Convert Purple Air csv dataset into code, calculate the average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 AQI over time.
# PM2.5 concentration was plotted and converted into AQI. AQI is also plotted. Universal time zone was converted into local, Central time. 
# Author: Logan Semones
# First Created: 06/11/2025

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# df = pd.read_csv('last_500_timepoints.csv', parse_dates=['time_stamp']) # Convert csv file into usable table

### Original csv file with all values
df = pd.read_csv('2019-01-01_2025-05-01_10-Minute_Average.csv', parse_dates=['time_stamp']) # Convert csv file into usable table
###

#Convert Universal time zone into local (Central) time for Mississippi
df['Central_time_stamp'] = pd.to_datetime(df['time_stamp']).dt.tz_convert('US/Central') 

### To initially decrease size of total csv file
# Slice the last 500 rows
# last_500 = df.tail(500)
#
# Save to a new CSV
# last_500.to_csv("last_500_timepoints.csv", index=False)
###

# Replace values > 500.4 with NaN
df['pm2.5_atm_a_clean'] = df['pm2.5_atm_a'].where(df['pm2.5_atm_a'] <= 500.4, np.nan)
df['pm2.5_atm_b_clean'] = df['pm2.5_atm_b'].where(df['pm2.5_atm_b'] <= 500.4, np.nan)

# Calculate row-wise average of the cleaned columns
df['pm2.5 Avg'] = df[['pm2.5_atm_a_clean', 'pm2.5_atm_b_clean']].mean(axis=1) # Takes the average pm2.5 values at each time point

### Convert average concentrations to AQI
# AQI Breakpoints (EPA 24-hour PM2.5)
breakpoints_pm25 = [
    (0.0, 9.0, 0, 50),
    (9.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 125.4, 151, 200),
    (125.5, 225.4, 201, 300),
    (225.5, 500.4, 301, 500),
]

def pm25_to_aqi(concentration):
    if pd.isna(concentration):
        return np.nan
    concentration = round(concentration, 1)  # EPA rounding rule
    
    for c_low, c_high, aqi_low, aqi_high in breakpoints_pm25:
        if c_low <= concentration <= c_high:
            return round(((aqi_high - aqi_low) / (c_high - c_low)) * (concentration - c_low) + aqi_low)
    if concentration > 500.4:
        return 500  # Cap at max AQI
    return np.nan  # Return NaN for negative or nonsense values

df['pm2.5 AQI'] = df['pm2.5 Avg'].apply(pm25_to_aqi)

fig1, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Time (Central)')
ax1.set_ylabel('PM2.5 Concentration (µg/m³)', color=color)
ax1.plot(df['Central_time_stamp'], df['pm2.5 Avg'], color=color, label='Concentration')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_title("PM2.5 Concentration Over Time")
plt.grid(True)

fig2, ax2 = plt.subplots()
color = 'tab:red'
ax2.set_ylabel('AQI', color=color)
ax2.plot(df['Central_time_stamp'], df['pm2.5 AQI'], color=color, label='AQI')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_title("PM2.5 AQI Over Time")

fig1.tight_layout()
fig2.tight_layout()
plt.grid(True)
plt.show()


