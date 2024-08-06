import pandas as pd

def parse_volatility(filename, new_filename):
    # Calculate the volatility
    volfile = pd.read_csv(filename, delimiter=';')
    
    # Convert 'Date' column to datetime
    volfile['Date'] = pd.to_datetime(volfile['Date'], format='%Y-%m-%d %H:%M:%S')
    
    # Convert datetime to Unix timestamp
    volfile['Date'] = volfile['Date'].apply(lambda x: int(time.mktime(x.timetuple())))

    volfile.to_csv(new_filename, index=False)

parse_volatility(vol_filename, 'new_ethvol.csv')