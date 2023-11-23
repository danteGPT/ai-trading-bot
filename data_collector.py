import pandas as pd
import requests
from datetime import datetime

def collect_historical_data(crypto_id, api_key, start_date, end_date):
    url = f'https://min-api.cryptocompare.com/data/v2/histoday'
    params = {
        'fsym': crypto_id,
        'tsym': 'USD',
        'limit': 2000,
        'toTs': int(end_date.timestamp()),
        'api_key': '3b311037957c48cff5cf685396cfff76952c1afd5c6fa18ba5cc124b0b4c5095'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['Data']['Data']
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('timestamp', inplace=True)
        return df[['close', 'volumeto']]  # You can select the columns you need
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

def append_data_to_csv(new_data, file_name):
    try:
        existing_data = pd.read_csv(file_name)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
        updated_data.sort_values(by='timestamp', inplace=True)
        updated_data.to_csv(file_name, index=False)
    except FileNotFoundError:
        new_data.to_csv(file_name, index=False)

# Example usage of the functions
if __name__ == "__main__":
    API_KEY = '3b311037957c48cff5cf685396cfff76952c1afd5c6fa18ba5cc124b0b4c5095'
    crypto_id = 'BTC'
    start_date = datetime(2020, 1, 1)  # Example start date
    end_date = datetime.now()  # Current date as end date

    new_data = collect_historical_data(crypto_id, API_KEY, start_date, end_date)
    append_data_to_csv(new_data, 'Data.csv')
