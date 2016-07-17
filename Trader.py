import time
import random
import redis
import re
import pickle
import threading
from bitfinex.client import Client

def paper_trade():
	try:
		client = Client()
		symbols = client.symbols()
		symbol = 'btcusd'
		lastprice = client.ticker(symbol)['last_price']
		print (lastprice)
		threading.Timer(0.5, paper_trade).start()
	except:
		print('couldnt get price data')
		threading.Timer(0.5, paper_trade).start()

paper_trade()

