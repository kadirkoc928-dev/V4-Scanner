import streamlit as st
import pandas as pd
from model import train_model
from scanner import scan_ticker

st.set_page_config(page_title="TradeScanner V4", layout="wide")

st.title("📊 TradeScanner V4 (AI + Live Scan)")

@st.cache_resource
def load_model():
    return train_model()

model = load_model()

tickers = st.text_input("Tickers (kommagetrennt)", "AAPL,TSLA,NVDA").upper()
tickers = [t.strip() for t in tickers.split(",")]

send = st.checkbox("Telegram Alerts (optional - später erweiterbar)")

if st.button("🚀 LIVE SCAN STARTEN"):
    results = []

    with st.spinner("Scanne Aktien..."):

        for t in tickers:
            res = scan_ticker(t, model)
            if res:
                results.append(res)

    if len(results) == 0:
        st.warning("Keine Signale gefunden")
    else:
        df = pd.DataFrame(results)
        df = df.sort_values("Probability", ascending=False)

        st.success(f"{len(df)} Signale gefunden")
        st.dataframe(df, use_container_width=True)
