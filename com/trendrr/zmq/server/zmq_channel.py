'''
Created on May 17, 2012
@author: mattd
'''

class ZMQChannel():
	
	def __init__(self, _id, out):
		self.id = _id
		self.outgoing = out

	def send(self, message):
		self.outgoing.send(id, message)