'''
	Created on May 15, 2012
	@author: mattd
'''
import zmq, threading, uuid

class ZMQClientWakeup(threading.Thread):

	def __init__(self,context,connection):
		self.context = context
		self.connection = connection
		self.messages = Queue()

	def start(self):
		t = Thread(self)
		t.setDaemon(True)
		t.start()
	
	def run(self):
		socket = self.context.socket(zmq.DEALER)
		socket.setIdentity(uuid.uuid4())
		socket.connect(self.connection);
		while True:
			try:
				message = self.messages.take()
				socket.send(message, 0)
			except Exception,e:
				print e.message

	def send(self,message):
		try:
			self.messages.append(message)
		except Exception,e:
			print e.message