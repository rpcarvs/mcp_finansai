import asyncio
import time

import streamlit as st
import yfinance as yf
from fastmcp import Client

from utils import company_name_n_currency, make_plot, wrapper

models = ["mistral-nemo", "llama3.1:8b", "qwen3:14b", "magistral:24b", "qwen3:1.7b", "mistral:7b"]
model = models[4]
# best models: 2, 3
# fastest: 1, 4


st.set_page_config(layout="wide")
currency = "Currency not found"
left, right = st.columns([0.35, 0.65], vertical_alignment="top", gap="large")

with st.container():
    with left:
        st.title("Write a valid ticker")
        model = st.selectbox("Choose model", models, index=models.index(model))
        col1, col2 = st.columns([0.7, 0.3], vertical_alignment="bottom")
        with col1:
            ticker = st.text_input(
                "Ticker",
                value="NVDA",
            )
        with col2:
            analyze = st.button(
                "**Analyze!**",
                type="primary",
                use_container_width=True,
            )

        if analyze and ticker:
            time_start = time.time()
            company, currency = company_name_n_currency(ticker)
            client_financial = Client("http://localhost:9001/mcp")
            awaitable_financial = client_financial.call_tool(
                "get_financial_news",
                {"ticker": ticker, "company": company, "model": model},
            )
            results_financial = asyncio.run(wrapper(client_financial, awaitable_financial))

            client_social = Client("http://localhost:9002/mcp")
            awaitable_social = client_social.call_tool(
                "get_social_sentiment",
                {"ticker": ticker, "company": company, "model": model},
            )
            results_social = asyncio.run(wrapper(client_social, awaitable_social))

            time_end = time.time()

            st.write(
                f"**Model**: {model}  |  **Total time**: {int(time_end - time_start)} seconds",
            )

            st.header("Financial News Analysis")
            st.subheader("Query")
            st.text(results_financial.data["query"])
            st.subheader("Summary")
            fin_summary = results_financial.data["summary"]
            if not fin_summary or "empty" in fin_summary:
                st.text("No financial news was retrieved for the ticker.")
            else:
                st.text(fin_summary)
                st.subheader("Sentiment")
                st.text(f"Score: {results_financial.data['sentiment']}/5.0")

            st.header("Social Analysis")
            st.subheader("Query")
            st.text(results_social.data["query"])
            st.subheader("Summary")
            soc_summary = results_social.data["summary"]
            if not soc_summary or "empty" in soc_summary:
                st.text("No social info was retrieved for the ticker.")
            else:
                st.text(soc_summary)
                st.subheader("Sentiment")
                st.text(f"Score: {results_social.data['sentiment']}/5.0")

    with right:
        st.title("Ploting Market data")
        if analyze and ticker:
            try:
                data = yf.download(
                    ticker,
                    period="1mo",
                    interval="1h",
                    multi_level_index=False,
                )

                # Calculate RSI
                if data is not None:
                    fig = make_plot(data, currency)
                    st.pyplot(fig)
                else:
                    st.error("Problem with the stock market API")

            except Exception:
                st.write("Problem loading market data")


with st.container():
    # add space
    for _ in range(6):
        st.text("")
    st.header("How it works")
    st.subheader("The agentic Worklow:")
    st.image("src/static/workflow.png")
