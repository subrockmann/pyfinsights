from pyfinsights import yfinance


# yfinance.get_dividends_date

def test_get_dividends_date_1():
    symbol = "AAPL"
    pays_dividends, dividend_date, ex_dividend_date, ticker = yfinance.get_dividends_date(symbol)

    assert pays_dividends == True
    assert dividend_date != None


def test_get_dividends_date_2():
    symbol = "VIX"
    pays_dividends, dividend_date, ex_dividend_date, ticker = (
        yfinance.get_dividends_date(symbol)
    )

    assert pays_dividends == False
    assert dividend_date == None
