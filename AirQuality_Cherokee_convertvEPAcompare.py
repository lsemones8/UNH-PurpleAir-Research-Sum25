# AirQuality_Cherokee_convertvEPAcompare.py
# Description: Convert Purple Air csv dataset into code, calculate the average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 AQI over time.
# PM2.5 concentration was plotted and converted into AQI. AQI is also plotted. Universal time zone was converted into local, Central time. Background is colored and
# labeled to correspond with the Air Quality health categories set by the EPA. With yearly data plotted. Plots condensed to 24-hour averages, before being plotted
# against EPA data.
# Author: Logan Semones
# First Created: 06/17/2025

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

#df = pd.read_csv('last_500_timepoints.csv', parse_dates=['time_stamp']) # Convert csv file into usable table

### Original csv file with all values ------------------------------------------------------------------------------------------------------------------------------
df = pd.read_csv('2019-12-01_2025-05-01_10-Minute_Average.csv', parse_dates=['time_stamp']) # Convert csv file into usable table
### ----------------------------------------------------------------------------------------------------------------------------------------------------------------

#Convert Universal time zone into local (Central) time for Mississippi
df['Central_time_stamp'] = pd.to_datetime(df['time_stamp']).dt.tz_convert('US/Central')

### To initially decrease size of total csv file -------------------------------------------------------------------------------------------------------------------
# Slice the last 500 rows
# last_500 = df.tail(500)
#
# Save to a new CSV
# last_500.to_csv("last_500_timepoints.csv", index=False)
### --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Replace values > 500.4 with NaN
df['pm2.5_atm_a_clean'] = df['pm2.5_atm_a'].where(df['pm2.5_atm_a'] <= 500.4, np.nan)
df['pm2.5_atm_b_clean'] = df['pm2.5_atm_b'].where(df['pm2.5_atm_b'] <= 500.4, np.nan)

# Calculate row-wise average of the cleaned columns
df['pm2.5 Avg'] = df[['pm2.5_atm_a_clean', 'pm2.5_atm_b_clean']].mean(axis=1) # Takes the average pm2.5 values at each time point

### Convert average concentrations to AQI --------------------------------------------------------------------------------------------------------------------------
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
### ---------------------------------------------------------------------------------------------------------------------------------------------------------------

### Convert 10-minute time averages into 24-hour time periods, based on days --------------------------------------------------------------------------------------
# Set Central time as index for resampling
df.set_index('Central_time_stamp', inplace=True)

# Resample from 10-minute data to 24-hour daily averages
daily_avg = df['pm2.5 Avg'].resample('D').mean()

# Resample from 10-minute data to 24-hour daily AQI
daily_aqi = df['pm2.5 AQI'].resample('D').mean()
### ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# daily_aqi is a Series indexed by daily timestamps
daily_df = pd.DataFrame({
    'pm2.5 AQI': daily_aqi,
    'pm2.5 Avg': daily_avg,
})

### Plot concentration over time ----------------------------------------------------------------------------------------------------------------------------------
fig1, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Time (Central)')
ax1.set_ylabel('PM2.5 Concentration (µg/m³)', color=color)
ax1.plot(daily_avg.index, daily_avg, color=color, label='Concentration')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_title("Daily PM2.5 Concentration Over Time")

# Coloring graph background, identifying Air Quality health categories
ax1.axhspan(0, 9.05, facecolor='green', alpha=0.5)
ax1.axhspan(9.05, 35.45, facecolor='yellow', alpha=0.5)
ax1.axhspan(35.45, 55.45, facecolor='orange', alpha=0.7)
ax1.axhspan(55.45, 125.45, facecolor='red', alpha=0.5)
ax1.axhspan(125.45, 225.45, facecolor='purple', alpha=0.3)
ax1.axhspan(225.45, 500.4, facecolor='purple', alpha=0.6)

# X-axis expansion (time-based)
x_min1 = min(daily_avg.index)
x_max1 = max(daily_avg.index)
x_range1 = x_max1 - x_min1
x_buffer1 = x_range1 * 0.1  # 10% on each side = 120% total
ax1.set_xlim(x_min1 - x_buffer1, x_max1 + x_buffer1)

# Y-axis expansion (numerical)
y_min1 = 0
y_max1 = max(daily_avg)
y_range1 = y_max1 - y_min1
y_buffer1 = y_range1 * 0.25
ax1.set_ylim(y_min1, y_max1 + y_buffer1)

# Create patches that represent your colored areas
good_Patch1 = mpatches.Patch(color='green', alpha=0.5, label='Good (0–9 µg/m³)')
moderate_Patch1 = mpatches.Patch(color='yellow', alpha=0.5, label='Moderate (9.1–35.4 µg/m³)')
somewhatUnhealthy_Patch1 = mpatches.Patch(color='orange', alpha=0.7, label='Unhealthy for sensitive groups (35.5–55.4 µg/m³)')
unhealthy_Patch1 = mpatches.Patch(color='red', alpha=0.5, label='Unhealthy (55.5-125.4 µg/m³)')
veryUnhealthy_Patch1 = mpatches.Patch(color='purple', alpha=0.3, label='Very Unhealthy (125.5-225.4 µg/m³)')
hazardous_Patch1 = mpatches.Patch(color='purple', alpha=0.6, label='Hazardous (225.5-500.4 µg/m³)')

# Making legend to identify Air Quality Health categories
ax1.legend(handles=[good_Patch1, moderate_Patch1, somewhatUnhealthy_Patch1, unhealthy_Patch1, veryUnhealthy_Patch1, hazardous_Patch1], loc = 'best')

plt.grid(True)
fig1.tight_layout()
### -------------------------------------------------------------------------------------------------------------------------------------------------------------

### Plot AQI  over time -----------------------------------------------------------------------------------------------------------------------------------------
fig2, ax2 = plt.subplots()
color = 'tab:red'
ax2.set_xlabel('Time (Central)')
ax2.set_ylabel('AQI', color=color)
ax2.plot(daily_aqi.index, daily_aqi, color=color, label='AQI')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_title("Daily PM2.5 AQI Over Time")

# Coloring graph background, identifying Air Quality health categories
ax2.axhspan(0, 50.5, facecolor='green', alpha=0.5)
ax2.axhspan(50.5, 100.5, facecolor='yellow', alpha=0.5)
ax2.axhspan(100.5, 150.5, facecolor='orange', alpha=0.7)
ax2.axhspan(150.5, 200.5, facecolor='red', alpha=0.5)
ax2.axhspan(200.5, 300.5, facecolor='purple', alpha=0.3)
ax2.axhspan(300.5, 500, facecolor='purple', alpha=0.6)

# X-axis expansion (time-based)
x_min2 = min(daily_aqi.index)
x_max2 = max(daily_aqi.index)
x_range2 = x_max2 - x_min2
x_buffer2 = x_range2 * 0.1  # 10% on each side = 120% total
ax2.set_xlim(x_min2 - x_buffer2, x_max2 + x_buffer2)

# Y-axis expansion (numerical)
y_min2 = 0
y_max2 = max(daily_aqi)
y_range2 = y_max2 - y_min2
y_buffer2 = y_range2 * 0.27
ax2.set_ylim(y_min2, y_max2 + y_buffer2)

# Create patches that represent your colored areas
good_Patch2 = mpatches.Patch(color='green', alpha=0.5, label='Good (0–50)')
moderate_Patch2 = mpatches.Patch(color='yellow', alpha=0.5, label='Moderate (51–100)')
somewhatUnhealthy_Patch2 = mpatches.Patch(color='orange', alpha=0.7, label='Unhealthy for sensitive groups (101-150)')
unhealthy_Patch2 = mpatches.Patch(color='red', alpha=0.5, label='Unhealthy (151-200)')
veryUnhealthy_Patch2 = mpatches.Patch(color='purple', alpha=0.3, label='Very Unhealthy (201-300)')
hazardous_Patch2 = mpatches.Patch(color='purple', alpha=0.6, label='Hazardous (301-500)')

# Making legend to identify Air Quality Health categories
ax2.legend(handles=[good_Patch2, moderate_Patch2, somewhatUnhealthy_Patch2, unhealthy_Patch2, veryUnhealthy_Patch2, hazardous_Patch2], loc = 'best')
plt.grid(True)
fig2.tight_layout()
### ------------------------------------------------------------------------------------------------------------------------------------------------------------

### Filter data from 2024 -----------------------------------------------------------------------------------------------------------------------------------------
# Filter by time (only 2024 data)
mask1 = (daily_aqi.index >= '2024-01-01') & (daily_aqi.index <= '2024-12-31')
df_PurpleAir = daily_df.loc[mask1]

### ------------------------------------------------------------------------------------------------------------------------------------------------------------

### Plot 2024 EPA data to 2024 PurpleAir Data ------------------------------------------------------------------------------------------------------------------
dfEPA = pd.read_csv('daily_avg_EPA_pm25_2024-2025.csv', parse_dates=['Date']) # Convert EPA data csv file into usable table
mask2 = (dfEPA['Date'] >= '2024-01-01') & (dfEPA['Date'] <= '2024-12-31')
df_EPA = dfEPA.loc[mask2]
df_EPA['Date'] = df_EPA['Date'].dt.tz_localize('US/Central')

# Rename for consistency (optional but cleaner)
print("PurpleAir index:", df_PurpleAir.index)
df_PurpleAir = df_PurpleAir.reset_index()
print("PurpleAir columns:", df_PurpleAir.columns)
df_PurpleAir.rename(columns={'Central_time_stamp': 'Date'}, inplace=True)

# Merge on Date — keeps only shared dates
df_merged = pd.merge(df_PurpleAir, df_EPA, on='Date', how='inner')

# Get x and y from the merged dataframe
x = df_merged['pm2.5 AQI']
y = df_merged['Daily AQI Value']

# Clean out rows with missing or non-numeric data
valid = x.notna() & y.notna() & np.isfinite(x) & np.isfinite(y)
x_clean = x[valid]
y_clean = y[valid]

# Now run polyfit on clean data
coeffs = np.polyfit(x_clean, y_clean, 1)
poly_eq = np.poly1d(coeffs)
y_fit = poly_eq(x_clean)

# Plot
fig4, ax4 = plt.subplots()
ax4.plot(x_clean, y_clean, 'o', label='Data', color='blue')
ax4.plot(np.sort(x_clean), poly_eq(np.sort(x_clean)), color='red',
         label=f'Fit: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
ax4.set_xlabel('PurpleAir Sensor data')
ax4.set_ylabel('EPA Sensor data')
ax4.set_title("EPA data vs. PurpleAir data (2024)")
ax4.legend()

### ------------------------------------------------------------------------------------------------------------------------------------------------------------

plt.show()
