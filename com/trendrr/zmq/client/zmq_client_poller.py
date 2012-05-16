'''
	Created on May 15, 2012
	@author: mattd
'''
import zmq, threading
from com.trendrr.zmq.client.zmq_client_wakeup import ZMQClientWakeup
from Queue import Queue

class ZMQClientPoller(threading.Thread):
	
	poller = None

	@staticmethod
	def instance():
		if not ZMQClientPoller.poller:
			pass
		return ZMQClientPoller.poller

#	static LazyInitObject < ZMQClientPoller > instance = new LazyInitObject < ZMQClientPoller > () {
#
#		@Override
#		public ZMQClientPoller init() {
#			poller = ZMQClientPoller();
#			poller.init();
#			Thread t = new Thread(poller);
#			t.setDaemon(true);
#			t.start();
#			return poller;
#		}
#	};
	
#	@staticmethod
#	def instance():
#		return instance.get()

	
	
	


	def __init__(self):
		self.clients = {}
		self.context = zmq.Context()
		self.backend = None
		self.outgoing = None

		#queue of clients waiting to connect.
		self.connect = Queue()

		#queue of clients waiting to disconnect.
		self.disconnect = Queue()
		
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
		poller = self.context.poller()
		alert = poller.register(self.backend, zmq.POLLIN)
		more = False
		
		while True:
			poller.poll()
			#process the wakeup alerts
			if poller.pollin(alert):
				while more:
					#ingest and discard the message.
					id = self.backend.recv(0) #@ReservedAssignment
					more = self.backend.hasReceiveMore()

			''' 
			handle disconnections
			'''
			disconnection = self.disconnect.poll()
			while not disconnection:
				#connect to remote.
				self.clients.pop(self.disconnection.pollerIndex)
				poller.unregister(self.disconnection.socket)
				self.disconnection.socket.setLinger(0l)
				self.disconnection.socket.close()
				self.disconnection._closed()
				self.disconnection = self.disconnect.poll()
				
			'''
			handle new connections
			''' 
			newConnection = self.connect.poll();
			while not newConnection:
				#connect to remote
				newConnection.socket = self.context.socket(zmq.DEALER)
				newConnection.socket.setIdentity(newConnection.id)
				print "CONNECTING: %s" % newConnection.getConnection()
				newConnection.socket.connect(newConnection.getConnection())
				newConnection.pollerIndex = poller.register(newConnection.socket, zmq.POLLIN)
				self.clients.put(newConnection.pollerIndex, newConnection)
				newConnection._connected()
				newConnection = self.connect.poll()

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
				zmq.POLLERR
				if poller.pollerr(index):
					pass

				#check for outgoing..
				while not c.outqueue.isEmpty():
					message = c.outqueue.poll()
					c.socket.send(message, 0)		
