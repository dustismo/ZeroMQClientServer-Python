'''
	Created on May 15, 2012
	@author: mattd
'''
import zmq, threading, uuid, Queue

class ZMQClientWakeup(threading.Thread):

	def __init__(self,context,connection):
		threading.Thread.__init__(self)
		self.context = context
		self.connection = connection
		self.messages = Queue()
		self.daemon = True

	def run(self):
		socket = self.context.socket(zmq.DEALER)
		socket.setIdentity(uuid.uuid4())
		socket.connect(self.connection);
		while True:
			try:
				message = self.messages.get()
				socket.send(message, 0)
			except Exception,e:
				print e.message

	def send(self,message):
		try:
			self.messages.put(message)
		except Exception,e:
			print e.message