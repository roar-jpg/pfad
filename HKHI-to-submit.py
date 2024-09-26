# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from calendar import month_abbr

# import numpy as np

# Load the CSV file from URL
file_path = 'https://data.weather.gov.hk/weatherAPI/cis/csvfile/KP/ALL/daily_KP_MEANHKHI_ALL.csv'

# Make the data frame clean
df = pd.read_csv(file_path, header=2, skipfooter=3) # Skip the irrelevant lines in the CSV
df = df.drop("數據完整性/data Completeness", axis='columns') # Drop the irrelevant data column in the CSV
df = df.rename(columns={'年/Year':'Year', '月/Month':'Month', '日/Day':'Day', '數值/Value':'Temperature'}) # Rename the columns

# Blend year, month, day into date
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

# Create a figure
plt.figure(figsize=(10, 6))

# Loop through each year to plot separate lines
for year in df['Year'].unique():
    # Filter data for the current year
    yearly_data = df[df['Year'] == year]
    
    # Plot the temperature data for this year
    plt.plot(yearly_data['Date'], yearly_data['Temperature'], label=str(year))

# Show the legend with labels for each year
plt.legend(title='Year')

# Set labels and title
plt.xlabel('Year')  # X-axis label (will display as month-day but months will be visible)
plt.ylabel('Temperature (°C)')  # Y-axis label
plt.title('Daily Temperatures (2014-2024)')  # Title of the graph

plt.show()