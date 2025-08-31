import mplfinance as mpf
import yfinance as yf


async def wrapper(client, coroutine):
    async with client:
        return await coroutine


def is_valid_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return not data.empty
    except Exception:
        return False


def company_name_n_currency(ticker):
    stock = yf.Ticker(ticker)
    company = stock.info.get("longName", "")
    currency = stock.info.get("currency", "")
    return company, currency


def make_plot(data, currency):
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()  # type: ignore
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()  # type: ignore

    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    # Compute moving average and standard deviation
    data["Middle_Band"] = data["Close"].rolling(window=20).mean()
    data["Upper_Band"] = data["Middle_Band"] + (data["Close"].rolling(window=20).std() * 2)
    data["Lower_Band"] = data["Middle_Band"] - (data["Close"].rolling(window=20).std() * 2)
    # Create additional plots
    apdict = [
        mpf.make_addplot(data["Upper_Band"], color="teal", alpha=0.7),
        mpf.make_addplot(
            data["Middle_Band"],
            color="dodgerblue",
            alpha=0.7,
        ),
        mpf.make_addplot(
            data["Lower_Band"],
            color="lightseagreen",
            alpha=0.7,
        ),
        mpf.make_addplot(
            data["RSI"],
            panel=1,
            ylabel="RSI",
            color="purple",
            alpha=0.6,
        ),
        mpf.make_addplot(
            [70] * len(data),
            panel=1,
            color="purple",
            linestyle="dashed",
        ),
        mpf.make_addplot(
            [30] * len(data),
            panel=1,
            color="purple",
            linestyle="dashed",
        ),
    ]

    fig, ax = mpf.plot(
        data,
        type="candle",
        style="binance",
        addplot=apdict,
        title="Candlestick with RSI on Subplot",
        ylabel=f"Price ({currency})",
        returnfig=True,
    )
    return fig
