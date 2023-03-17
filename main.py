import os
import time
import datetime
from pathlib import Path
from binance import Client
from dotenv import load_dotenv

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_KEY_SECRET')

client = Client(api_key, api_secret)

prices = []

while True:
    try:
        ticker = client.futures_ticker(symbol='ETHUSDT')
        price = float(ticker['lastPrice'])
        current_time = datetime.datetime.now()

        prices.append({'price': price, 'time': current_time})

        while len(prices) > 0 and (current_time - prices[0]['time']).seconds > 3600:
            prices.pop(0)

        if len(prices) > 1:
            price_change = (prices[-1]['price'] - prices[0]['price']) / prices[0]['price'] * 100
            if abs(price_change) > 1:
                print(f"Price change in the last hour: {price_change:.2f}%")

        time.sleep(1)
    except Exception as e:
        print(e)
        break


    