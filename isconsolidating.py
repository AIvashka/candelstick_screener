import os
import pandas


def is_consolidating(df, percentage=2):
    recent_candlesticks = df[-15:]

    max_close = recent_candlesticks['Close'].max()
    min_close = recent_candlesticks['Close'].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True

    return False


def is_breaking_out(df, percentage=2.5):
    try:
        last_close = df[-1:]['Close'].values[0]
    except IndexError:
        return False
    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[-16:-1]

        if last_close > recent_closes['Close'].max():
            return True

    return False


for filename in os.listdir('datasets/daily'):
    df = pandas.read_csv('datasets/daily/{}'.format(filename))

    if is_consolidating(df, percentage=2.5):
        print("{} is consolidating".format(filename[:-4]))

    if is_breaking_out(df):
        print("{} is breaking out".format(filename[:-4]))
