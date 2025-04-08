
import yfinance as yf
import pandas as pd
from typing import List, Union


def get_dividends_date(symbol: str, verbose: bool = False):
    ticker = None
    dividends = None
    pays_dividends = False
    dividend_date = None
    ex_dividend_date = None

    try:
        ticker = yf.Ticker(symbol)
        dividends = ticker.dividends
    except Exception as e:
        print(f"Unable to retrieve data for {symbol}: {e}")
        return (pays_dividends, dividend_date, ex_dividend_date, ticker)

    if dividends is not None and not dividends.empty:
        pays_dividends = True
        try:
            # Get the most recent dividend date
            dividend_date = dividends.index[-1]
        except Exception as e:
            print(f"Error retrieving dividend date for {symbol}: {e}")
            dividend_date = None

        # Note: yfinance does not provide "Ex-Dividend Date" directly
        ex_dividend_date = None  # Placeholder if needed

    if verbose:
        print(
            f"{symbol} - dividend date: {dividend_date} / ex-dividend date: {ex_dividend_date}"
        )

    return (pays_dividends, dividend_date, ex_dividend_date, ticker)   


def get_earnings_dates(symbols: Union[str, List[str]]) -> pd.DataFrame:
    """
    Fetches earnings dates for the given stock symbols using yfinance.

    Args:
        symbols (Union[str, List[str]]): A single stock symbol as a string or a list of stock symbols as strings.

    Returns:
        pd.DataFrame: A DataFrame containing the symbols, whether the date is confirmed,
                      and the earnings dates (with the second date being None if there's only one date).

                      The DataFrame has the following columns:
                      - 'symbol': The stock symbol.
                      - 'date_confirmed': A boolean indicating if the earnings date is confirmed.
                      - 'earnings_date_1': The first earnings date.
                      - 'earnings_date_2': The second earnings date, if available.
    """
    earnings = []
    symbol_errors = []

    if isinstance(symbols, str):
        symbols = [symbols]

    for i, symbol in enumerate(symbols):
        print(f"{i} - Fetching earnings dates for {symbol}")

        try:
            ticker = yf.Ticker(symbol)
            earnings_list = ticker.calendar["Earnings Date"]

            if len(earnings_list) == 1:
                date_confirmed = True
                earnings.append([symbol, date_confirmed, earnings_list[0], None])

            elif len(earnings_list) == 2:
                date_confirmed = False
                earnings.append(
                    [symbol, date_confirmed, earnings_list[0], earnings_list[-1]]
                )
        except:
            print(f"Unable to retrieve data for {symbol}")
            symbol_errors.append(symbol)
            date_confirmed = False
            earnings.append([symbol, date_confirmed, None, None])

    df = pd.DataFrame(
        earnings,
        columns=["symbol", "date_confirmed", "earnings_date_1", "earnings_date_2"],
    )
    df["earnings_date_1"] = pd.to_datetime(df["earnings_date_1"])
    df["earnings_date_2"] = pd.to_datetime(df["earnings_date_2"])

    return df
