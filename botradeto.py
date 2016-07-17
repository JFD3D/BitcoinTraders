import irc.client
from googlefinance import getQuotes
import time
import random
import redis
import pickle
import shelve

class Tradebot(object):
	
	def __init__(self, nick, server, password="xxxx", port=6667):
		d = shelve.open('Botato/Shelf.gdb')
		self.client = irc.client.Reactor()
		self.nick = nick
		self.server = server
		self.port = port
		self.channels = ['#botato']
		self.c = None
		self.redis_conn = redis.Redis()
		self.stocklist = d['stocklist']
		self.mybalance = d['mybalance']
		d.close()
		
	def start(self):
		try:
			self.c = self.client.server();
			print("connecting")
			self.c.connect(self.server, self.port, self.nick)
		except irc.client.ServerConnectionError:
			print ("failed connecting")
			raise SystemExit(1)
			
		self.c.add_global_handler("welcome", self.on_connect)
		self.c.add_global_handler("disconnect", self.on_disconnect)
		self.c.add_global_handler("privmsg", self.on_privmsg)
		self.c.add_global_handler("pubmsg", self.on_pubmsg)
		
	def msg_all(self, msg):
		if self.c != None:
			for channel in self.channels:
				self.c.privmsg(channel, msg)  # TODO use privmsg many

	def msg_one(self, e, msg):
		if e.target == self.nick:
			self.c.privmsg(e.source.nick, msg)
		else:
			self.c.privmsg(e.target, msg)

	def on_connect(self, c, e):
		print ("connected")
		self.time_connected = time.ctime()
		for channel in self.channels:
				c.join(channel)

	def on_join(self, c, e):
		pass

	def on_disconnect(self, c, e):
		print ("DISCONNECTED {}")
		self.start()
		
	def on_privmsg(self, c, e):
		self.parse_msg(e, e.arguments[0])

	def on_pubmsg(self, c, e):
		if e.source.nick == "Aquent" or e.source.nick == "Aquent1":
			pass
		if e.source.nick == "pennies":
			return
		if e.source.nick == 'Chainbot':
			return
		if e.source.nick == 'twobitbot':
			return
		if e.source.nick == 'shovel_boss':
			return
		if e.source.nick == 'rake_boss':
			return
		if e.source.nick == 'litecamel':
			return
		if '_boss' in e.source.nick:
			return
		if random.random()*100 < 1:
			pass
		self.parse_msg(e, e.arguments[0])
		
	def buystock(self, e):
		stock2buy = random.choice(self.stocklist)
		quote = getQuotes(stock2buy)[0]
		price = quote['LastTradePrice']
		price = price.strip("'")
		price = float(price)
		self.msg_one(e,"I think I'll buy %s for %.2f" % (stock2buy, price))
		self.mybalance = self.mybalance - price
		self.msg_one(e,"My new balance is %.2f" % self.mybalance)
		
	def initialize(self):
		d = shelve.open('Botato/Shelf.gdb', writeback=True)
		d['mybalance'] = 1000.00
		print("saved the DB")
		d.close()
		
		
	def parse_msg(self, e, data):
		nick = e.source.nick
		cmd = data.split(" ", 1)
		print (data)
		if cmd[0] == "~buyit":
			#try:
			self.buystock(e)
			#except:
			#	self.msg_one(e, "Now look what you've done. You've gone and broken it. Try again later you twit")
				
		if cmd[0] == "~initialize":
			self.initialize()
	
def main():
	botato = Tradebot("botradeto", "wolfe.freenode.net")
	botato.start()
	botato.client.process_forever()
	
if __name__ == "__main__":
	main()