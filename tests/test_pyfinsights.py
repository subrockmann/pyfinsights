from pyfinsights import yfin, utils
import pandas as pd
import numpy as np


# yfinance.get_dividends_date

def test_get_dividends_date_1():
    symbol = "MSFT"
    pays_dividends, dividend_date, ex_dividend_date, ticker = yfin.get_dividends_date(symbol)

    assert pays_dividends == True
    assert dividend_date != None


def test_get_dividends_date_2():
    symbol = "VIX"
    pays_dividends, dividend_date, ex_dividend_date, ticker = (
        yfin.get_dividends_date(symbol)
    )

    assert pays_dividends == False
    assert dividend_date == None


# yfinance.get_earnings_dates
def test_get_earnings_dates_1():
    symbol = "AAPL"

    df = yfin.get_earnings_dates(symbol)
    assert isinstance(df, pd.DataFrame)


def test_get_earnings_dates_2():
    symbol = ["AAPL", "TSLA"]

    df = yfin.get_earnings_dates(symbol)
    assert isinstance(df, pd.DataFrame)


# Sample DataFrame
data = {
    "symbol": ["AAPL", "TSLA", "TSM"],
    "date_confirmed": [False, False, False],
    "earnings_date_1": ["2024-10-31", "2024-10-18", "2024-10-17"],
    "earnings_date_2": ["2024-11-04", "2024-10-28", "2024-10-21"],
}

df = pd.DataFrame(data)
df["earnings_date_1"] = pd.to_datetime(df["earnings_date_1"])
df["earnings_date_2"] = pd.to_datetime(df["earnings_date_2"])

#earnings_df = yfinance.get_earnings_dates(["AAPL", "TSLA"])

def test_get_earnings_date_from_df():
    symbol = "TYL" #"AAPL"
    global df
    earnings_date, earnings_date_confirmed = utils.get_earnings_date_from_df(df, symbol)
    if earnings_date is not None:
        assert isinstance(earnings_date, pd.Timestamp), "The object is not a pandas Timestamp"
    assert earnings_date_confirmed in [True, False]
