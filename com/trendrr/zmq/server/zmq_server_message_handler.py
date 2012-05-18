'''
Created on May 17, 2012
@author: mattd
'''
import abc

class ZMQServerMessageHandler():
	
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod		
	def incoming(self,channel,message):
		#you must impliment this
		return

	@abc.abstractmethod
	def error(self,x):
		#you must impliment this
		return