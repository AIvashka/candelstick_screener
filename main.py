import os, csv
import talib
import yfinance as yf
import pandas
import datetime
from flask import Flask, escape, request, render_template
from patterns import candlestick_patterns
app = Flask(__name__)
@app.route('/')
def index():
    pattern = request.args.get('pattern', False)
    stocks = {}
    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
    if pattern:
        with open('datasets/companies.csv') as f:
            for line in f:
                if "," not in line:
                    continue
                symbol = line.split(",")[0]
                df = yf.download(symbol, start="2020-01-01", end=datetime.date.today().isoformat())
                pattern_function = getattr(talib, pattern)
            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]
                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                print(e)
                print('failed on filename: ', symbol)
    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)
app.run()
