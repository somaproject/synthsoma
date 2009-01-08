#!/usr/bin/python
from event import Event
import struct, time
from math import sin, pi

class Device(object):

	def __init__(self, numDevice):
		self.num = numDevice
		self.cNum = 0

	#each devices needs to know when a event cycle has occured
	#each event cycle this method will be called. It is up to the
	#individual devices to handle the cycling of the event cycle
	#however is the most appropriate for that individual device
	def setCycleLength(self, len):
		self.cyclelen = len


	def setOutputQueue(self, eventQueue):
		self.eventQueue = eventQueue

	def cycle(self):
		self.cNum +=1
		
	def receiveEvent(self, event):
#		print event.getCmd(), " from", event.getSrc(), ' applied to:', self.num
#		self.bcastEvent()
		x = 1 #empty method
			
	def bcastEvent(self):
		addr = 0
		cmd = 0
		src = self.num
		eventOut = Event(addr, cmd, src, 'I\'mtheDr')
		self.eventQueue.enqueueEvent(eventOut)

class Timer(object):
	def __init__(self, numDevice):
		self.num = numDevice
		self.somaTime = 0

	def setOutputQueue(self, eventQueue):
		self.eventQueue = eventQueue

	def setCycleLength(self, len):
		self.cyclelen = len

	def cycle(self):
		self.__broadcastTime()

	def __broadcastTime(self):
		addr = range(80)
		cmd = 0x10
		src = 0
		eventOut = Event(addr, cmd,src, struct.pack(self.TIME(), self.somaTime) ) 
		self.eventQueue.enqueueEvent(eventOut)
		self.somaTime += 1

	def receiveEvent(self, event):
#		print event.getCmd(), " from", event.getSrc(), ' applied to:', self.num
		x = 1 #empty method
			
	def TIME(self): return '>Q'
