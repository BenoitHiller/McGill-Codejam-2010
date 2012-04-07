import MySQLdb
import time
import bid
from threading import Thread, Lock
class Dataset(Thread):
	table = """CREATE TABLE BIDS (TIME DECIMAL(12,2) NOT NULL, NAME CHAR(32), PRICE INT, SHARES INT)"""
	def __init__(self, user, password, db, host="localhost"):
		Thread.__init__(self)
		self.exit = True
		self.closed = 0
		self.running = False
		self.user = user
		self.password = password
		self.db = db
		self.host = host
		self.lock = Lock()
	
	def connect(self):
		self.con = MySQLdb.connect(self.host,self.user,self.password,self.db)

	def add(self,time,name,price,shares):
		self.lock.acquire()
		if self.running:
			entry = "INSERT INTO BIDS(TIME, NAME, PRICE, SHARES) VALUES ('%f', '%s', '%d', '%d')" % (time,name,price,shares)
			while True:
				try:
					self.cursor.execute(entry)
					self.con.commit()
				except (AttributeError, MySQLdb.OperationalError):
					self.connect
					self.cursor = self.con.cursor()
					continue
				except:
					self.con.rollback()
					print "error could not store '%s'" % (entry)
				break
		else:
			print "Database not initialised"
		self.lock.release()

	def closep(self,time):
		if self.closed != 0:
			if self.closed >= time:
				return False
			else:
				return True
		else:
			return False

	def close(self,time):
		if self.closed == 0:
			self.closed = time

	def done(self):
		self.lock.acquire()
		self.con.close()
		self.running = False
		self.exit = False

	def getPrices(self, price):
		self.lock.acquire()
		if self.running:
			while True:
				try:
					self.cursor.execute("SELECT * FROM BIDS WHERE PRICE=%d" % (price))
					bids = self.cursor.fetchall()
				except (AttributeError, MySQLdb.OperationalError):
					self.connect
					self.cursor = self.con.cursor()
					continue
				break
		self.lock.release()
		return bids
		
	def sumPrices(self):
		sharelist = []
		prices = []
		self.lock.acquire()
		if self.running:
			while True:
				try:
					self.cursor.execute("SELECT DISTINCT PRICE FROM BIDS ORDER BY PRICE")
					pricesl = self.cursor.fetchall()
					for price in pricesl:
						prices.append(price[0])
					for price in prices:
						total = 0
						self.cursor.execute("SELECT PRICE,SHARES FROM BIDS WHERE PRICE=%d" % (price))
						shares = self.cursor.fetchall()
						for share in shares:
							total += share[1]
						sharelist.append(total)
				except (AttributeError, MySQLdb.OperationalError):
					self.connect
					self.cursor = self.con.cursor()
					continue
				break
		self.lock.release()
		return(prices, sharelist)
		
	def clearingPrice(self):
		total = 0
		clearingPrice = 0
		i = 0
		(prices, shares) = self.sumPrices()
		prices.reverse()
		shares.reverse()
		while i < len(prices):
			clearingPrice = prices[i]
			total += shares[i]
			if total >= bid.Bid.shares:
				break
			i = i + 1
		return clearingPrice

	def summary(self):
		(prices, shares) = self.sumPrices()
		prices.reverse()
		shares.reverse()
		i = 0
		summary = "Auction Status "
		if self.closed != 0:
			summary += "CLOSED"
		else:
			summary += "OPEN"
		summary += "\nClearing Price " + str(self.clearingPrice()) + "\n"
		while i < len(prices):
			summary += "${0} {1}\n".format(int(prices[i]), int(shares[i]))
			i += 1
		return summary

	def fiveNewest(self):
		returnstring = ""
		self.lock.acquire()
		if self.running:
			while True:
				try:
					self.cursor.execute("SELECT TIME,NAME,SHARES,PRICE FROM BIDS ORDER BY TIME DESC LIMIT 0,5")
					newest = self.cursor.fetchall()
					for new in newest:
						returnstring += "%s bought %d shares at $%d each at %s\n" % (new[1], new[2], new[3], (time.asctime(time.localtime(new[0]))))
				except (AttributeError, MySQLdb.OperationalError):
					self.connect
					self.cursor = self.con.cursor()
					continue
				break
		self.lock.release()
		return returnstring

	def run(self):
		self.running = True
		self.lock.acquire()
		self.connect()
		self.cursor = self.con.cursor()
		try:
			self.cursor.execute("DROP TABLE IF EXISTS BIDS")
			self.cursor.execute(Dataset.table)
			self.con.commit()
		except:
			self.con.rollback()
			print "Something horribly wrong with database"
			self.con.close()
			self.exit = False
		self.lock.release()
		print "Database Up"
		while self.exit:
			time.sleep(1)
