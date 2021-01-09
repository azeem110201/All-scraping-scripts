import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import random

headers = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
           "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
           "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
           ]

def extract(stock_list: list):
    for stock in stock_list:
        url = "https://in.finance.yahoo.com/quote/{}?p={}".format(stock, stock)
        random_header = random.choice(headers)
        r = requests.get(url, random_header)

        soup = BeautifulSoup(r.content, "html.parser")

        close_price = [entry.text.strip() for entry in soup.find_all(
            'span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]

        previous_close = [entry.text.strip() for entry in soup.find_all(
            'span', {'class': 'Trsdu(0.3s)'})]

        range_ = [entry.text.strip() for entry in soup.find_all(
            'td', {'class': 'Ta(end) Fw(600) Lh(14px)'})]
        
        return {
            "Stock name":stock,
            "Close price":close_price,
            "Percentage change":previous_close[10],
            "Previous close":previous_close[11],
            "Open":previous_close[12],
            "Volumne":previous_close[15],
            "Average volumne":previous_close[16],
            "Market cap":previous_close[17],
            "P/E Ratio":previous_close[19],
            "EPS":previous_close[20],
            "1 year Target EST":previous_close[21],
            "Today's range":range_[4],
            "52-week range":range_[5],
            "Forward dividend & yield":range_[13]
        }

close_price = extract(["MSFT"])

print(close_price)

