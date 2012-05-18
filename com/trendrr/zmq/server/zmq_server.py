'''
Created on May 17, 2012
@author: mattd
'''

import zmq, threading
from com.trendrr.zmq.server.zmq_channel import ZMQChannel

class ZMQServer(threading.Thread):
	def __init__(self):
		self.port = 8653
		self.handler
		private AtomicBoolean stopped = new AtomicBoolean(True)
		self.context
		self.pollingTimeout = 1000*1000

	'''
	starts the listener.
	@param threaded should this be started in a new thread? if true, will return immediately, if false will never return.
	'''
	def listen(self,port,handler,threaded):
		self.port = port
		self.handler = handler
		if threaded:
			self.start()
		else:
			self.run()


	def run(self):
		
		context = zmq.Context(1)
		frontend = context.socket(zmq.ROUTER)
		frontend.bind ("tcp://*:%d" % self.port)

		backend = context.socket(zmq.DEALER)
		backend.bind("inproc://serverbackend")

		#set up the outgoing
		outgoing = ZMQServerOutgoing(context, "inproc://serverbackend")
		outgoing.start()

		self.stopped.set(False)

		poller = context.poller(2)
		frontIndex = poller.register(frontend, zmq.POLLIN)
		backIndex = poller.register(backend, zmq.POLLIN)

		more = False
		
		print("Server Listening on : %d" % self.port)
		
		while True:
			poller.poll(self.pollingTimeout)
			if self.stopped.get():
				poller.unregister(frontend)
				poller.unregister(backend)
				frontend.setLinger(0l)
				frontend.close()
				backend.setLinger(0l)
				backend.close()
				context.term()
				return

			if (poller.pollin(frontIndex)):
				#incoming messages.
				while more:
					id = frontend.recv(0)
					message = frontend.recv(0)
					more = frontend.hasReceiveMore()
					self.handleIncoming(ZMQChannel(id, outgoing), message)

			if (poller.pollin(backIndex)):
				#theres a message needs to be written.
				while more:
					id = backend.recv(0)
					message = backend.recv(0)
					more = backend.hasReceiveMore()
					# Broker it
					frontend.send(id, zmq.SNDMORE)
					frontend.send(message,0)

	'''
	closes and cleans up this server
	
	Currently this is an asynch call, it returns immediately, but it may take a 
	second or three to actually clean up.  
	
	TODO: block until the operation completes.
	'''
	def close(self):
		self.stopped.set(True)

	def handleIncoming(self,channel,message):
		self.handler.incoming(channel, message)