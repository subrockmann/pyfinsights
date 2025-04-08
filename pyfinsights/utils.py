import pandas as pd
from typing import List, Union, Tuple, Optional


def get_earnings_date_from_df(
    df: pd.DataFrame, symbol: str
) -> Tuple[Optional[pd.Timestamp], bool]:
    """
    Retrieves the earnings date and its confirmation status for a given stock symbol from a DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame extracted from yfinance containing stock symbols and their earnings dates.
        symbol (str): The stock symbol for which to retrieve the earnings date.

    Returns:
        Tuple[Optional[pd.Timestamp], bool]: A tuple containing the earnings date and a boolean indicating
                                              whether the date is confirmed. If the symbol is not found,
                                              returns (None, False).
    """
    try:
        earnings_date = df.loc[df["symbol"] == symbol, "earnings_date_1"].iloc[0]
        earnings_date_confirmed = df.loc[df["symbol"] == symbol, "date_confirmed"].iloc[
            0
        ]

    except IndexError:
        print(f"{symbol} is not in the dataframe")
        earnings_date = None
        earnings_date_confirmed = False

    return earnings_date, earnings_date_confirmed
