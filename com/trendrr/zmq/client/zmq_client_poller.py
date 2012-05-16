'''
	Created on May 15, 2012
	@author: mattd
'''
import zmq, uuid, threading

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
#            poller = ZMQClientPoller();
#			poller.init();
#			Thread t = new Thread(poller);
#			t.setDaemon(true);
#			t.start();
#			return poller;
#		}
#	};
    
#    @staticmethod
#	def instance():
#        return instance.get()

	#queue of clients waiting to connect.
	ArrayBlockingQueue < ZMQClient > connect = new ArrayBlockingQueue < ZMQClient > (10);

	#queue of clients waiting to disconnect.
	ArrayBlockingQueue < ZMQClient > disconnect = new ArrayBlockingQueue < ZMQClient > (10);
	
	ZMQClientWakeup outgoing;
	ZMQ.Socket backend;


	def __init__(self):
		self.clients = {}
		self.context = zmq.Context()
        self.backend = None
        
    ''' 
	wakes up the poller, checks for disconnects, connects, outgoing messages, ect.
	'''
    def wakeup(self):
        self.outgoing.send(new byte[1])
        
    '''
	do the initialization outside of the main thread execution.
	'''
    def init(self):
        self.backend = self.context.socket(zmq.dealer)
		self.backend.bind("inproc://clientbackend")
		self.outgoing = ZMQClientWakeup(self.context, "inproc://clientbackend")
		self.outgoing.start()

    def run():
		poller = self.context.poller()
		alert = poller.register(self.backend, zmq.Poller.POLLIN)
		more = False
		
        while True:
			poller.poll()
			#process the wakeup alerts
			if poller.pollin(alert)):
				while more:
					#ingest and discard the message.
					byte[] id = backend.recv(0);
                    more = backend.hasReceiveMore()

			''' 
            handle disconnections
            '''
            disconnection = self.disconnect.poll();
			while not disconnection:
				#connect to remote.
				self.clients.pop(self.disconnection.pollerIndex)
				poller.unregister(self.disconnection.socket)
				self.disconnection.socket.setLinger(0l)
				self.disconnection.socket.close()
				self.disconnection._closed()
				self.disconnection = disconnect.poll()
                
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
				newConnection.pollerIndex = poller.register(newConnection.socket, zmq.Poller.POLLIN)
				self.clients.put(newConnection.pollerIndex, newConnection)
				newConnection._connected()
				newConnection = connect.poll()

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
				if poller.pollerr(index)):
					#TODO
				}

				#check for outgoing..
				while not c.outqueue.isEmpty()):
                    message = c.outqueue.poll()
					c.socket.send(message, 0)		
