import csv
import pandas as pd
import numpy as np
from datetime import datetime

filename = 'price_data.csv'
best_i = 18
best_j = 16
length = 365

def calculate_volatility(time, lead, lag):
    try:
        
        # Read the CSV file into a DataFrame
        data = pd.read_csv(filename)

        # Filter data based on the date range
        lower = time - (lag*86400)
        upper = time + (lead*86400)

        filtered_data = data[
            (data['time'] >= lower) & 
            (data['time'] <= upper) 
        ]

        # Calculate the volatility (standard deviation of returns)
        volatility = filtered_data['ln_ratio'].std() * np.sqrt(24) * np.sqrt(365) # verify if length is right to use

        return volatility
    except:
        return 0


with open('output_file.csv', 'w', newline='') as csvfile:
    fieldnames = ['time', 'volatility']
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fieldnames)
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for data in reader:
            time = float(data[0])
            dt = datetime.fromtimestamp(time)
            if dt.hour == 0:
                volatility = calculate_volatility(time, best_i, best_j)
                csvwriter.writerow([time, volatility])