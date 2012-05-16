'''
	Created on May 15, 2012
	@author: mattd
'''
import zmq, uuid
from Queue import Queue
from com.trendrr.zmq.client.zmq_client_poller import ZMQClientPoller

class ZMQClient():

	def __init__(self, connection, handler):
		self.connection = connection
		self.handler = handler
		self.id = uuid.uuid4()
		self.socket = None
		#used by the poller thread
		self.poller_index
		self.outqueue = Queue()
#		LazyInit connectLock = new LazyInit()


	def get_connection(self):
		return self.connection

	def send(self,message):
		if self.connectLock.start():
			try:
				self.connect()
			except:
				pass
			else:
				self.connectLock.end()
		
		try:
			self.outqueue.put(message)
			ZMQClientPoller.instance().wakeup()
		except Exception, e:
			print e.message

	'''
	called lazily
	'''
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