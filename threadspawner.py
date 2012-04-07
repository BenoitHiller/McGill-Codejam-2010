"""
     This program runs in its own thread and waits for connections.
     When a thread is opened, it spawns a processthread.py
     It is created with (port, total shares, minimum price, maximum price)
     Run it by calling .start()
"""
cont = True

import processthread
import bid
import socket
from threading import Thread
import Dataset

#This is our thingy that accepts sockets
class threadspawner(Thread):
    def __init__(self, port,user="dutch",password="godm0d3",data="dutchipo"):
        Thread.__init__(self)
        self.port = port
        self.dataset = Dataset.Dataset(user, password, data)
	self.dataset.start()

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('', self.port))
        serversocket.listen(30000)
        while cont:
            (clientsocket, address) = serversocket.accept()
            worker = processthread.processthread(clientsocket, self.dataset)
            worker.start()
            




        
