'''
Created on May 17, 2012

@author: mattd
'''
import threading, zmq
from Queue import Queue

class ZMQOutMessage():
	def __init__(self, _id, message):
		self.id = _id
		self.message = message

class ZMQServerOutgoing(threading.Thread):

	def __init__(self, context, connection):
		self.message = Queue(10)
		self.context = context
		self.connection = connection

	def start(self):
		self.daemon = True
		self.start()

	def run(self):
		socket = self.context.Socket(zmq.DEALER)
		socket.connect(self.connection)
		while True:
			try:
				message = self.messages.get()
				socket.send(message.id, zmq.SNDMORE)
				socket.send(message.message, 0)
			except Exception,e:
				print "Caught %s" % e.message


	def send(self,_id,message):
		try:
			self.messages.put(ZMQOutMessage(_id, message))
		except Exception, e:
			print e.message