ZeroMQClientServer-Python
=========================

This is a wrapper around the hot-mess that is zeromq async sockets. This provides a threadsafe and latency free way to handle message passing in zeromq. This is a port of the Java version created by @dustismo

Usage:

```python
'''
create a client
you only need a client and a class to handle incoming messages
'''

from com.trendrr.zmq.client.zmq_client_message_handler import ZMQClientMessageHandler

ClientHandler(ZMQClientMessageHandler):

	def incoming(client,message):
		try:
			print message
		except Exception,e:
			print e.message

		def error(x):
			print x.message
 
client = ZMQClient("tcp://localhost:8988", ClientHandler())

#client is threadsafe
client.send("this is a message")

```

Server

```python
 '''
 this creates a simple echo server
 '''
	ZMQServerMessageHandler handler = new ZMQServerMessageHandler() {
			
			@Override
			public void incoming(ZMQChannel channel, byte[] message) {
				//just send the message back to the originating user.
				//you could also start a new thread here to handle more intense processing.
				//the channel is threadsafe
				channel.send(message);
			}
			
			@Override
			public void error(Exception x) {
				x.printStackTrace();
			}
		};
		ZMQServer server = new ZMQServer();
		server.listen(8988, handler, true);

```
