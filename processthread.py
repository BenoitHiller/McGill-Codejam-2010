"""
    This thread processes the client/server interaction
    It is called from threadspawner.py

    Usage: create by passing in a valid socket and then call .start()

"""

import bid
import time
from threading import Thread


class processthread(Thread):

    def __init__(self, socket, dataset):
        Thread.__init__(self)
        self.socket = socket
        self.dataset = dataset
    def run(self):   
    	#print "process thread started========="
        msocket = self.socket
        msocket.settimeout(0.1)
	total_data=[]
	data=''
	begin=time.time()
	while True:
		if total_data and time.time() - begin > 0.005:
			break
		elif time.time() - begin > 0.01:
			break
		try:
			data=msocket.recv(96)
			if data:
				total_data.append(data)
				begin=time.time()
			else:
				time.sleep(1)
		except:
			pass
	readin = ''.join(total_data)
      	#print repr(readin)
	test = time.time()
        ourbid = bid.Bid(readin, test, self.dataset) #changed
	#print str(test)
#check valid socket
        try:
            status = msocket.sendall(ourbid.reply)
        except:
            msocket.close()
            return
        if status is None:
#that is if sendAll worked
            ourbid.store()
        msocket.close()
