import yfinance as yf


def get_dividends_date(symbol: str, verbose: bool = False):
    pays_dividends = False
    # last_dividend = 0
    dividend_date = None
    ex_dividend_date = None

    try:
        ticker = yf.Ticker(symbol)
        dividends = ticker.dividends
    except:
        print(f"Unable to retrieve data for {symbol}")
        # break

    if len(dividends) == 0:
        pass
        # return(pays_dividends, dividend_date, ex_dividend_date, ticker)
    else:
        pays_dividends = True
        dividend_date = ticker.calendar["Dividend Date"]
        ex_dividend_date = ticker.calendar["Ex-Dividend Date"]
    if verbose:
        print(
            f"{symbol} - dividend date: {dividend_date} / ex-dividend date: {ex_dividend_date}"
        )

    return (pays_dividends, dividend_date, ex_dividend_date, ticker)
