import requests
import pandas as pd
from datetime import datetime

def collect_historical_data(crypto_id, currency='USD', limit=2000, api_key='YOUR_API_KEY'):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    params = {
        'fsym': 'ETH',
        'tsym': 'USD',
        'limit': 2000,
        'api_key': '3b311037957c48cff5cf685396cfff76952c1afd5c6fa18ba5cc124b0b4c5095'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['Data']['Data']
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('timestamp', inplace=True)
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()
