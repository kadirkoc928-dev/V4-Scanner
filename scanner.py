import yfinance as yf
import pandas as pd
from indicators import add_indicators

def filter_signal(row):
    score = 0

    if row["VOL_RATIO"] > 1.3:
        score += 1
    if row["RSI"] > 45:
        score += 1
    if row["ADX"] > 20:
        score += 1
    if row["MACD"] > row["MACD_SIGNAL"]:
        score += 1
    if row["Close"] > row["SMA20"]:
        score += 1

    return score >= 3

def generate_signal(model, row):
    features = ["SMA20","SMA50","RSI","ADX","MACD","MACD_SIGNAL","VOL_RATIO"]

    prob = model.predict_proba([row[features]])[0][1]

    if prob > 0.7:
        return "STRONG_BUY", prob
    elif prob > 0.6:
        return "BUY", prob
    elif prob < 0.4:
        return "SELL", prob
    return "NO_TRADE", prob

def scan_ticker(ticker, model):
    try:
        df = yf.Ticker(ticker).history(period="6mo")
        if df.empty:
            return None

        df = add_indicators(df)
        latest = df.iloc[-1]

        if not filter_signal(latest):
            return None

        signal, prob = generate_signal(model, latest)

        return {
            "Ticker": ticker,
            "Price": latest["Close"],
            "Signal": signal,
            "Probability": round(prob,3),
            "RSI": latest["RSI"],
            "ADX": latest["ADX"],
            "VolumeRatio": latest["VOL_RATIO"]
        }

    except:
        return None
