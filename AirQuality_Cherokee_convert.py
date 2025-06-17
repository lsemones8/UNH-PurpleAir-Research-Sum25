# AirQuality_Cherokee_convertv3.py
# Description: Convert Purple Air csv dataset into code, calculate the average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 AQI over time.
# PM2.5 concentration was plotted and converted into AQI. AQI is also plotted. Universal time zone was converted into local, Central time. Background is colored and
# labeled to correspond with the Air Quality health categories set by the EPA. Also has yearly data plotted.
# Author: Logan Semones
# First Created: 06/16/2025

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# df = pd.read_csv('last_500_timepoints.csv', parse_dates=['time_stamp']) # Convert csv file into usable table

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

### Plot yearly data -------------------------------------------------------------------------------------------------------------------------------------------
df['year'] = df['Central_time_stamp'].dt.year

# Define the list of years to exclude
exclude_years = [2019]  # Years to exclude

# Group data by year
grouped = df.groupby('year')

# Get Figure 2 properties
fig2_size = fig2.get_size_inches()  # Window size
plot_color = 'tab:red'  # Line color from Figure 2
fig2_facecolor = fig2.get_facecolor()  # Figure background color
ax2_facecolor = ax2.get_facecolor()  # Axes background color

# Create a new figure for each year, excluding specified years
for year, group in grouped:
    if year in exclude_years:
        continue  # Skip plotting for this year
    fig, ax = plt.subplots(figsize=fig2_size)  # Match Figure 2 size
    # Apply background colors
    fig.set_facecolor(fig2_facecolor)
    ax.set_facecolor(ax2_facecolor)
    # Plot AQI data
    ax.plot(group['Central_time_stamp'], group['pm2.5 AQI'], color=plot_color, label='AQI')
    ax.tick_params(axis='y', labelcolor=plot_color)
    # Add AQI health category background spans (same as Figure 2)
    ax.axhspan(0, 50.5, facecolor='green', alpha=0.5)
    ax.axhspan(50.5, 100.5, facecolor='yellow', alpha=0.5)
    ax.axhspan(100.5, 150.5, facecolor='orange', alpha=0.7)
    ax.axhspan(150.5, 200.5, facecolor='red', alpha=0.5)
    ax.axhspan(200.5, 300.5, facecolor='purple', alpha=0.3)
    ax.axhspan(300.5, 500, facecolor='purple', alpha=0.6)
    # Set title and labels
    ax.set_title(f"PM2.5 AQI Over Time - {year}")
    ax.set_xlabel('Time (Central)')
    ax.set_ylabel('AQI', color=plot_color)
    # X-axis limits with buffer
    x_min = min(group['Central_time_stamp'])
    x_max = max(group['Central_time_stamp'])
    x_range = x_max - x_min
    x_buffer = x_range * 0.1  # 10% buffer
    ax.set_xlim(x_min - x_buffer, x_max + x_buffer)
    y_buffer3 = y_range2 * 0.18
    # Y-axis limits with buffer
    ax.set_ylim(y_min2, y_max2 + y_buffer3)
    # Add legend with AQI health categories (same as Figure 2)
    ax.legend(handles=[good_Patch2, moderate_Patch2, somewhatUnhealthy_Patch2, unhealthy_Patch2, veryUnhealthy_Patch2, hazardous_Patch2], loc='best')
    # Add grid and adjust layout
    ax.grid(True)
    fig.tight_layout()
### ------------------------------------------------------------------------------------------------------------------------------------------------------
    
plt.show()
