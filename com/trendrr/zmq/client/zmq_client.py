'''
	Created on May 15, 2012
	@author: mattd
'''
import uuid
from Queue import Queue
from com.trendrr.zmq.client.zmq_client_poller import ZMQClientPoller
from __future__ import with_statement
from threading import Lock

class ZMQClient():

	def __init__(self, connection, handler):
		self.connection = connection
		self.handler = handler
		self.id = uuid.uuid4()
		self.socket = None
		self.poller_index
		self.outqueue = Queue(25)
		self.connectLock = Lock()
		self.connected = False
		
	def get_connection(self):
		return self.connection

	def send(self,message):
		with self.connectLock:
			if not self.connected:
				self.connect()
				self.connected = True
		
		try:
			self.outqueue.put(message)
			ZMQClientPoller.instance().wakeup()
		except Exception, e:
			print e.message

	def connect(self):
		ZMQClientPoller.instance().connect.add(self)
		ZMQClientPoller.instance().wakeup()

	def close(self):
		print 'Client CLOSE!'
		ZMQClientPoller.instance().disconnect.add(self)
		ZMQClientPoller.instance().wakeup()

	def _connected(self):
		print "CONNECTED!"
	
	def _closed(self):
		self.socket = None
		self.handler = None