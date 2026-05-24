import ta

def add_indicators(df):
    df = df.copy()

    df["SMA20"] = ta.trend.sma_indicator(df["Close"], 20)
    df["SMA50"] = ta.trend.sma_indicator(df["Close"], 50)

    df["RSI"] = ta.momentum.rsi(df["Close"], 14)
    df["ADX"] = ta.trend.adx(df["High"], df["Low"], df["Close"], 14)

    df["MACD"] = ta.trend.macd(df["Close"])
    df["MACD_SIGNAL"] = ta.trend.macd_signal(df["Close"])

    df["VOL_SMA"] = df["Volume"].rolling(20).mean()
    df["VOL_RATIO"] = df["Volume"] / df["VOL_SMA"]

    return df
