import pandas as pd
import requests
from datetime import datetime

def calculate_rsi(data, window=14):
    delta = data['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
    
def calculate_macd(data, short_window=12, long_window=26, signal=9):
    data['EMA_short'] = data['price'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['price'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['MACD_Signal'] = data['MACD'].ewm(span=signal, adjust=False).mean()
    return data

def calculate_bollinger_bands(data, window=20):
    data['SMA'] = data['price'].rolling(window=window).mean()
    data['BB_std'] = data['price'].rolling(window=window).std()
    data['Upper_Band'] = data['SMA'] + (data['BB_std'] * 2)
    data['Lower_Band'] = data['SMA'] - (data['BB_std'] * 2)
    return data

def calculate_stochastic_oscillator(data, k_window=14, d_window=3):
    data['L14'] = data['low'].rolling(window=k_window).min()
    data['H14'] = data['high'].rolling(window=k_window).max()
    data['%K'] = 100 * ((data['price'] - data['L14']) / (data['H14'] - data['L14']))
    data['%D'] = data['%K'].rolling(window=d_window).mean()
    return data

def calculate_atr(data, window=14):
    data['High-Low'] = data['high'] - data['low']
    data['High-PrevClose'] = abs(data['high'] - data['price'].shift(1))
    data['Low-PrevClose'] = abs(data['low'] - data['price'].shift(1))
    data['TR'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
    data['ATR'] = data['TR'].rolling(window=window).mean()
    return data

def calculate_vwap(data):
    data['Cum_Volume'] = data['volume'].cumsum()
    data['Cum_Vol_Price'] = (data['volume'] * data['price']).cumsum()
    data['VWAP'] = data['Cum_Vol_Price'] / data['Cum_Volume']
    return data

def preprocess_data(data):
    data = calculate_macd(data)
    data = calculate_bollinger_bands(data)
    data = calculate_stochastic_oscillator(data)
    data = calculate_atr(data)
    data = calculate_vwap(data)
    data['SMA_15'] = data['price'].rolling(window=15).mean()
    data['EMA_15'] = data['price'].ewm(span=15, adjust=False).mean()
    data['RSI'] = calculate_rsi(data)
    data['target'] = data['price'].shift(-1)  # Example: next period's price

    # Debugging: Print to check if calculations are done
    print("Data after preprocessing:", data.head())

    return data

def collect_historical_data(crypto_id, api_key, start_date, end_date):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    params = {
        'fsym': crypto_id,
        'tsym': 'USD',
        'limit': 2000,  # Adjust as necessary
        'toTs': int(end_date.timestamp()),
        'api_key': '3b311037957c48cff5cf685396cfff76952c1afd5c6fa18ba5cc124b0b4c5095'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['Data']['Data']
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df['price'] = df['close']  # Closing price as 'price'
        df['open'] = df['open']
        df['high'] = df['high']
        df['low'] = df['low']
        df['volume'] = df['volumeto']
        # Additional fields like market cap can be added if available from the API
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

def append_data_to_csv(new_data, file_name):
    try:
        existing_data = pd.read_csv(file_name)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
        updated_data.to_csv(file_name, index=False)
    except FileNotFoundError:
        new_data.to_csv(file_name, index=False)

if __name__ == "__main__":
    API_KEY = '3b311037957c48cff5cf685396cfff76952c1afd5c6fa18ba5cc124b0b4c5095'
    crypto_id = 'BTC'
    start_date = datetime(2008, 1, 1)  # Adjust the start date as needed
    end_date = datetime.now()  # Current date as the end date

    new_data = collect_historical_data(crypto_id, API_KEY, start_date, end_date)
    new_data = preprocess_data(new_data)  # Add this line
    append_data_to_csv(new_data, 'Data.csv')
