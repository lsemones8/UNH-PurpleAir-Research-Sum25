# AirQuality_Cherokee_convertvBoxPlot.py
# Description: Convert Purple Air csv dataset into code, calculate the average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 AQI over time.
# PM2.5 concentration was plotted and converted into AQI. AQI is also plotted. Universal time zone was converted into local, Central time. Background is colored and
# labeled to correspond with the Air Quality health categories set by the EPA. Diurnal (daily variation) plotted as well
# Author: Logan Semones
# First Created: 06/20/2025

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
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

### Plot concentration over time ----------------------------------------------------------------------------------------------------------------------------------
fig1, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Time (Central)')
ax1.set_ylabel('PM2.5 Concentration (µg/m³)', color=color)
ax1.plot(df['Central_time_stamp'], df['pm2.5 Avg'], color=color, label='Concentration')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_title("PM2.5 Concentration Over Time")

# Coloring graph background, identifying Air Quality health categories
ax1.axhspan(0, 9.05, facecolor='green', alpha=0.5)
ax1.axhspan(9.05, 35.45, facecolor='yellow', alpha=0.5)
ax1.axhspan(35.45, 55.45, facecolor='orange', alpha=0.7)
ax1.axhspan(55.45, 125.45, facecolor='red', alpha=0.5)
ax1.axhspan(125.45, 225.45, facecolor='purple', alpha=0.3)
ax1.axhspan(225.45, 500.4, facecolor='purple', alpha=0.6)

# X-axis expansion (time-based)
x_min1 = min(df['Central_time_stamp'])
x_max1 = max(df['Central_time_stamp'])
x_range1 = x_max1 - x_min1
x_buffer1 = x_range1 * 0.1  # 10% on each side = 120% total
ax1.set_xlim(x_min1 - x_buffer1, x_max1 + x_buffer1)

# Y-axis expansion (numerical)
y_min1 = 0
y_max1 = max(df['pm2.5 Avg'])
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
ax2.plot(df['Central_time_stamp'], df['pm2.5 AQI'], color=color, label='AQI')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_title("PM2.5 AQI Over Time")

# Coloring graph background, identifying Air Quality health categories
ax2.axhspan(0, 50.5, facecolor='green', alpha=0.5)
ax2.axhspan(50.5, 100.5, facecolor='yellow', alpha=0.5)
ax2.axhspan(100.5, 150.5, facecolor='orange', alpha=0.7)
ax2.axhspan(150.5, 200.5, facecolor='red', alpha=0.5)
ax2.axhspan(200.5, 300.5, facecolor='purple', alpha=0.3)
ax2.axhspan(300.5, 500, facecolor='purple', alpha=0.6)

# X-axis expansion (time-based)
x_min2 = min(df['Central_time_stamp'])
x_max2 = max(df['Central_time_stamp'])
x_range2 = x_max2 - x_min2
x_buffer2 = x_range2 * 0.1  # 10% on each side = 120% total
ax2.set_xlim(x_min2 - x_buffer2, x_max2 + x_buffer2)

# Y-axis expansion (numerical)
y_min2 = 0
y_max2 = max(df['pm2.5 AQI'])
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

### Make box plots for each hour of the day --------------------------------------------------------------------------------------------------------------------

# Drop rows where timestamp or AQI is missing
df = df.dropna(subset=['Central_time_stamp', 'pm2.5 AQI'])

# Convert AQI to numeric (in-place to update the DataFrame)
df['pm2.5 AQI'] = pd.to_numeric(df['pm2.5 AQI'], errors='coerce')

# Drop rows with invalid AQI values
df = df.dropna(subset=['pm2.5 AQI'])

# Extract hour from timestamp
df['hour'] = df['Central_time_stamp'].dt.hour

# Group AQI values by hour
hourly_data = [df[df['hour'] == h]['pm2.5 AQI'].values for h in range(24)]

# Plot
fig3, ax3 = plt.subplots(figsize=(15, 8))
ax3.boxplot(hourly_data, positions=range(24), meanline=True, medianprops={'color': 'red'}, showmeans=True, whis=[0,100], patch_artist=True,
            boxprops=dict(facecolor='silver'), meanprops={'linestyle': '--', 'color': 'blue'}, showfliers=True)

ax3.set_title("Hourly Distribution of AQI (24-hour Format)")
ax3.set_xlabel("Hour of Day")
ax3.set_ylabel("PM2.5 AQI")

# Custom tick labels
tick_labels = [f"{h}-{h+1}" for h in range(24)]
ax3.set_xticks(ticks=range(24), labels=tick_labels, rotation=45)

# Coloring graph background, identifying Air Quality health categories
ax3.axhspan(-3, 50.5, facecolor='green', alpha=0.5)
ax3.axhspan(50.5, 100.5, facecolor='yellow', alpha=0.5)
ax3.axhspan(100.5, 150.5, facecolor='orange', alpha=0.7)
ax3.axhspan(150.5, 200.5, facecolor='red', alpha=0.5)
ax3.axhspan(200.5, 300.5, facecolor='purple', alpha=0.3)
ax3.axhspan(300.5, 550, facecolor='purple', alpha=0.6)

# Y-axis expansion (numerical)
y_min3 = -3
y_max3 = max(df['pm2.5 AQI'])
y_range3 = y_max3 - y_min3
y_buffer3 = y_range3 * 0.6
ax3.set_ylim(y_min3, y_max3 + y_buffer3)

# Create patches that represent colored areas
good_Patch2 = mpatches.Patch(color='green', alpha=0.5, label='Good (0–50)')
moderate_Patch2 = mpatches.Patch(color='yellow', alpha=0.5, label='Moderate (51–100)')
somewhatUnhealthy_Patch2 = mpatches.Patch(color='orange', alpha=0.7, label='Unhealthy for sensitive groups (101-150)')
unhealthy_Patch2 = mpatches.Patch(color='red', alpha=0.5, label='Unhealthy (151-200)')
veryUnhealthy_Patch2 = mpatches.Patch(color='purple', alpha=0.3, label='Very Unhealthy (201-300)')
hazardous_Patch2 = mpatches.Patch(color='purple', alpha=0.6, label='Hazardous (301-500)')

# Create patches that represnt box plot
box_patch = mpatches.Patch(facecolor='silver', edgecolor='black', label='Interquartile Range (Box)')
median_line = mlines.Line2D([], [], color='red', label='Median')
mean_line = mlines.Line2D([], [], color='blue', linestyle='--', label='Mean')
whisker_line = mlines.Line2D([], [], color='black', linestyle='-', label='Whiskers')

all_handles = [
    good_Patch2, moderate_Patch2, somewhatUnhealthy_Patch2, unhealthy_Patch2, veryUnhealthy_Patch2, hazardous_Patch2,
    box_patch, whisker_line, median_line, mean_line] 
# Making legend to identify Air Quality Health categories
ax3.legend(handles=all_handles, loc = 'upper center')

ax3.grid(True)
plt.tight_layout()
### ------------------------------------------------------------------------------------------------------------------------------------------------------------
    
plt.show()
