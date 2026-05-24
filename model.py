import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from indicators import add_indicators

def build_dataset():
    df = yf.Ticker("AAPL").history(period="2y")
    df = add_indicators(df)

    df["FUTURE_RETURN"] = df["Close"].shift(-5) / df["Close"] - 1
    df["TARGET"] = (df["FUTURE_RETURN"] > 0.03).astype(int)

    df = df.dropna()
    return df

def train_model():
    df = build_dataset()

    features = ["SMA20","SMA50","RSI","ADX","MACD","MACD_SIGNAL","VOL_RATIO"]

    X = df[features]
    y = df["TARGET"]

    model = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
    model.fit(X, y)

    return model
