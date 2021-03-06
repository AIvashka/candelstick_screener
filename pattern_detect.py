import talib
import yfinance as yf
talib_doc = "https://github.com/mrjbq7/ta-lib"

data = yf.download('SPY', start='2020-01-01', end='2020-08-01')

#print(data)

morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])

engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

data['Morning Star'] = morning_star
data['Engulfing'] = engulfing

engulfing_days = data[data['Engulfing'] != 0]

print(engulfing_days)