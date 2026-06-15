import streamlit as st
from src.watchlist import WATCHLIST
from src.analyzer import analyze_coin


st.set_page_config(
    page_title="Jarvis Oracle",
    page_icon="📈",
    layout="wide"
)

st.title("Jarvis Oracle")
st.subheader("AI-Powered Market Intelligence & Trading Assistant")

st.write("Scanning selected coins using EMA, liquidity, BOS, FVG, and order block logic.")

interval = st.selectbox(
    "Select Timeframe",
    ["15m", "30m", "1h", "2h", "4h"],
    index=0
)

if st.button("Scan Market"):
    for symbol in WATCHLIST:
        result = analyze_coin(symbol, interval, 200)

        st.divider()
        st.header(result["symbol"])

        col1, col2, col3 = st.columns(3)

        col1.metric("Price", result["price"])
        col2.metric("Score", result["score"])
        col3.metric("Decision", result["decision"])

        st.write("EMA:", result["ema_signal"])
        st.write("Liquidity Sweep:", result["liquidity_sweep"])
        st.write("BOS:", result["bos_signal"])
        st.write("FVG:", result["has_fvg"])
        st.write("Valid Order Block:", result["valid_order_block"])

        if result["setup"]:
            st.success("Trade Setup Found")

            setup = result["setup"]

            st.write("Direction:", setup["direction"])
            st.write("Entry:", setup["entry"])
            st.write("Stop Loss:", setup["stop_loss"])
            st.write("Take Profit:", setup["take_profit"])
            st.write("Risk Reward:", setup["risk_reward"])
        else:
            st.warning("No valid trade setup.")