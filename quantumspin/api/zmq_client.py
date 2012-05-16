'''
	Created on May 15, 2012
	@author: mattd
'''
import zmq, uuid
from quantumspin.api.zmq_client_poller import ZMQClientPoller

class ZMQClient():

	def __init__(self, connection, handler):
		self.connection = connection
		self.handler = handler
		self.id = uuid.uuid4()
		
		#used by the poller thread
		self.poller_index

#		ZMQ.Socket socket;
#		ArrayBlockingQueue<byte[]> outqueue = new ArrayBlockingQueue<byte[]>(25);
#		LazyInit connectLock = new LazyInit();


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
		client_poller.instance().disconnect.add(self)
		ZMQClientPoller.instance().wakeup()

	def _connected(self):
		print "CONNECTED!"
	
	def _closed(self):
		self.socket = None
		self.handler = None