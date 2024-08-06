import requests
import csv

import time
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import math

# Define the parameters

offset = 30 # days back we want to start
length = 500 # days of data we want to use
leading_days_max = 20 # days
lagging_days_max = 20 # days
granularity = 1 # hours

filename = 'price_data.csv'
vol_filename = 'ethvol.csv'

url = 'https://min-api.cryptocompare.com/data/v2/histohour'

current_date = datetime.now()
new_date = current_date - timedelta(days=offset)
unix_time = int(time.mktime(new_date.timetuple()))
offset_unix = unix_time - 86400 * length

params = {
  'fsym': 'ETH',
  'tsym': 'USDC',
  'e': 'CCCAGG',
  'limit': 2000,
  'toTs': unix_time,
  'api_key': '789e6a309036edf1bd1fe40f816d94e7aa40b2de642b0e7f5bc7bdccecbcb4d5'
}


csvfile = open(filename, 'w', newline='')
fieldnames = ['time', 'price', 'ln_ratio']
csvwriter = csv.writer(csvfile)
csvwriter.writerow(fieldnames)

while offset_unix < unix_time:
    list = []
    if unix_time - offset_unix < 2000 * 3600:
        params['limit'] = (unix_time - offset_unix) // 3600

    response = requests.get(url, params=params)
    data = response.json()

    offset_unix = offset_unix + 2000 * 3600
    
    params['toTs'] = data['Data']['TimeFrom']

    for item in data['Data']['Data']:
        list.append(item)

    last_close = list[-1]['close']

    for item in reversed(list):
        dt = datetime.fromtimestamp(item['time'])
        if item['time'] != None: # weird parsing issue, in local timezone: and dt.hour == 0
            csvwriter.writerow([item['time'], item['close'], 100*np.log(item['close'] / last_close)]) #
            last_close = item['close']

csvfile.close()

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



min_r = 1000000000000

for i in range(0, leading_days_max):
    for j in range(1, lagging_days_max):
        r = 0
        counter = 0
        with open('new_ethvol.csv') as f:
            reader = csv.reader(f)
            for data in reader:
                if float(data[0]) >= 1685937600 and float(data[0]) <= 1717560000:
                    implied_volatility = float(data[1])
                    realized_volatility = calculate_volatility(float(data[0]), i, j)

                    if not math.isnan(realized_volatility):
                        if abs(implied_volatility - realized_volatility) ** 2 > 10000:
                            print('fail:', implied_volatility, realized_volatility)
                        #print(abs(implied_volatility - realized_volatility) ** 2)
                        r += (abs(implied_volatility - realized_volatility) ** 2)
                        counter += 1
        print(i, j, r, counter, r/counter)
        if r/counter < min_r:
            min_r = r/counter
            best_i = i
            best_j = j

print('FINAL: ')
print(best_i, best_j, min_r)

#API: 789e6a309036edf1bd1fe40f816d94e7aa40b2de642b0e7f5bc7bdccecbcb4d5