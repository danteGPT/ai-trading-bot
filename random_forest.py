import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def load_data(filename):
    return pd.read_csv(filename)

def prepare_data(data):
    features = data[['SMA_15', 'EMA_15', 'RSI', 'MACD', 'Upper_Band', 'Lower_Band', '%K', '%D', 'ATR', 'VWAP']]
    features = features.fillna(features.mean())
    
    target = data['target']
    
    # Fill NaN values in the target with the mean
    target = target.fillna(target.mean())
    
    return train_test_split(features, target, test_size=0.2, random_state=42)

def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

def main():
    data = load_data('Data.csv')
    X_train, X_test, y_train, y_test = prepare_data(data)
    model = train_random_forest(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()
