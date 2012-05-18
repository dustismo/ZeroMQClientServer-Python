'''
	Created on May 15, 2012
	@author: mattd
'''

import zmq, threading
from zmq.core.poll import Poller
from com.trendrr.zmq.client.zmq_client_wakeup import ZMQClientWakeup
from Queue import Queue

class ZMQClientPoller(threading.Thread):
	
	poller = None

	@staticmethod
	def instance():
		if not ZMQClientPoller.poller:
			ZMQClientPoller.poller = ZMQClientPoller()
			ZMQClientPoller.poller.init()
			ZMQClientPoller.poller.deamon = True
			ZMQClientPoller.poller.start()
		return ZMQClientPoller.poller

	def __init__(self):
		self.clients = {}
		self.context = zmq.Context()
		self.backend = None
		self.outgoing = None

		#queue of clients waiting to connect.
		self.connect = Queue(10)

		#queue of clients waiting to disconnect.
		self.disconnect = Queue(10)
		
	''' 
	wakes up the poller, checks for disconnects, connects, outgoing messages, ect.
	'''
	def wakeup(self):
		self.outgoing.send("")
		
	'''
	do the initialization outside of the main thread execution.
	'''
	def init(self):
		self.backend = self.context.socket(zmq.DEALER)
		self.backend.bind("inproc://clientbackend")
		self.outgoing = ZMQClientWakeup(self.context, "inproc://clientbackend")
		self.outgoing.start()

	def run(self):
		poller = Poller()
		alert = poller.register(self.backend, zmq.POLLIN)
		more = False
		
		while True:
			poller.poll()
			
			#process the wake up alerts
			if poller.pollin(alert):
				while more:
					#ingest and discard the message.
					id = self.backend.recv(0) #@ReservedAssignment
					more = self.backend.hasReceiveMore()

			''' 
			handle disconnections
			'''
			try :
				while True:
					
					disconnection = self.disconnect.get(block=False)
					self.clients.pop(disconnection.pollerIndex)
					poller.unregister(disconnection.socket)
					disconnection.socket.setLinger(0l)
					disconnection.socket.close()
					disconnection._closed()
			except:
				pass #TODO only want to pass on Empty exceptions
				
			'''
			handle new connections
			''' 
			try :
				while True:
					newConnection = self.connect.get(block=False)
					newConnection.socket = self.context.socket(zmq.DEALER)
					newConnection.socket.setsockopt(zmq.IDENTITY,newConnection.id)
					print "CONNECTING: %s" % newConnection.getConnection()
					newConnection.socket.connect(newConnection.getConnection())
					newConnection.pollerIndex = poller.register(newConnection.socket, zmq.POLLIN)
					self.clients.put(newConnection.pollerIndex, newConnection)
					newConnection._connected()
			except:
				pass #TODO only want to pass on Empty exceptions

			for index in self.clients.keys():
				c = self.clients.get(index)
				# now handle any real incoming messages
				if poller.pollin(index):
					# there is message ! 
					while more:
						message = c.socket.recv(0)
						more = c.socket.hasReceiveMore()
						c.handler.incoming(c, message)

				#check for error?
#				zmq.POLLERR
#				if poller.pollerr(index):
#					pass

				#check for outgoing..
				while not c.outqueue.empty():
					message = c.outqueue.poll()
					c.socket.send(message, 0)		
