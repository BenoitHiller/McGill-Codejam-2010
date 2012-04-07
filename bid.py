import time
import re

class Bid:
	#max,min and close are external things I will deal with later
	close = False
	pmax = 100000
	pmin = 0
	shares = 10000
	a = "A\r\n"
	e = "E\r\n"
	c = "C\r\n"

	num = re.compile("\d{1,8}")
	name = re.compile("[A-Za-z 0-9]{1,32}\r\n$")
	name2 = re.compile("[A-Za-z0-9][A-Za-z 0-9]*")
	def __init__(self, string, time, dataset):
		self.dataset = dataset
		self.validate = False
		self.time = time
		self.data = string.split('|')
		self.shares, self.price, self.name, self.reply = "n/a","n/a","n/a",Bid.e
		if len(self.data) == 2:
			if self.data == ["C","TERMINATE\r\n"]:
			        self.dataset.close(time)
				Bid.close = True
				self.reply = Bid.a
			elif self.data == ["S","SUMMARY\r\n"]:
			        print self.dataset.summary()
				self.reply = Bid.a
		elif dataset.closep(time) == True:
			self.reply = Bid.c
		else:
			if self.data[0] == "B" and len(self.data) == 4:
				if Bid.num.match(self.data[1]) and Bid.num.match(self.data[2]) and Bid.name.match(self.data[3]) and int(self.data[1]) <= Bid.shares  and int(self.data[2]) >= Bid.pmin and int(self.data[2]) <= Bid.pmax:
					self.shares = int(self.data[1])
					self.price = int(self.data[2])
					self.name = Bid.name2.search(self.data[3]).group()
					self.reply = Bid.a
					self.validate = True
	def inspect(self):
		return "time: {0}\nname: {1}\nprice: {2}\nshares: {3}\nreply: {4}".format(self.time, self.name, self.price, self.shares, self.reply)
	def store(self):
		if self.validate:
			self.dataset.add(self.time,self.name,self.price,self.shares)
