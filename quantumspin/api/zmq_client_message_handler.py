'''
    Created on May 15, 2012
    @author: mattd
'''

import abc

class ZMQClientMessageHandler():
	
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod	
	def incoming(self,client,message):
		'''you must implement this'''
		return
	
	@abc.abstractmethod
	def error(self,x):
		'''you must implement this'''
		return