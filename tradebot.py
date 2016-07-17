import threading
from bitfinex.client import Client
import time
import pickle


'''define our bot'''
class tradebot(object):
	
	def __init__(self):
		self.tradebalanceinit = 10000.00
		self.oldbtclent = 0
		self.newbtclent = 0
		self.oldbtcused = 0
		self.newbtcused = 0
		self.oldethlent = 0
		self.newethlent = 0
		self.oldethused = 0
		self.newethused = 0
		self.keepgoing = 0
		
	'''grab BTC and ETH price data from Finex'''
	def getprices(self):
		try:
			client = Client()
			symbols = client.symbols()
			btcsymbol = 'btc'
			ethsymbol = 'eth'
			symbol = 'btcusd'
			lastprice = client.ticker(symbol)['last_price']
			btcresponse = client.lends(btcsymbol)
			ethresponse = client.lends(ethsymbol)
			self.newbtclent = float(btcresponse[0]['amount_lent'])
			self.newbtcused = float(btcresponse[0]['amount_used'])
			self.newethlent = float(ethresponse[0]['amount_lent'])
			self.newethused = float(ethresponse[0]['amount_used'])
			self.keepgoing = 1
		except:
			print ('unable to get price data')
			
	'''do stuff with data to get swaps info'''
	def calculate_swap(self):
		btccentborrowed = (self.newbtcused / self.newbtclent) * 100
		ethcentborrowed = (self.newethused / self.newethlent) * 100
		
	def calculate_change(self):
		btcentchange = ((self.newbtcused - self.oldbtcused) / self.oldbtcused) * 100
		ethcentchange = ((self.newethused - self.oldethused) / self.oldethused) * 100
		
			
		