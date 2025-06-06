# AirQualityPlots_0601-0604.py
# Description: Convert Purple Air csv dataset into code, calculate the
# average of pm2.5a and pm2.5b at each timepoint, and plot average pm2.5 over time.   
# Author: Logan Semones
# First Created: 06/04/2025

import pandas as pd
import matplotlib.pyplot as plt
# import numpy

df = pd.read_csv('0601-0604_PurpleAir_data.csv', parse_dates=['DateTime']) # Convert csv file into usable table

df['Funk Avg'] = df[['Funk A', 'Funk B']].mean(axis=1) # Takes the average pm2.5 values at each time point

plt.plot(df['DateTime'], df['Funk Avg'], label='Funk Avg')
plt.xlabel('DateTime')
plt.ylabel('pm2.5 AQI')
plt.title('Average pm2.5 Air Quality Index (AQI) Over Time')
plt.legend()
plt.grid(True)
plt.show()

