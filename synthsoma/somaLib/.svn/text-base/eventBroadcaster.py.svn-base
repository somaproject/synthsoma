#!/usr/bin/python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from socket import SOL_SOCKET, SO_BROADCAST
import socket, sys, time, copy, struct
from device import Device

class EventBroadcaster(DatagramProtocol):
	def __init__(self, cycleLen, bCastIP, port, devices, reactor ):
		self.bcast = bCastIP
		self.port = port
		self.devices = devices
		self.reactor = reactor
	
		self.eventQueue = []
		self.cycleLen = float(cycleLen)
		self.setCount = 0
		self.eventSets = [ [],[],[],[],[] ]
		self.totalEvents = 0
		self.currentSeq = 0	
	
		for d in devices: 
			d.setOutputQueue(self)
			d.setCycleLength(self.cycleLen)

		self.cycle()		

	def startProtocol(self):
		self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
#		print "Event BCast Protocol Started"

	def enqueueEvent(self, event):
#		print "receiving command to enqueue a new event"
		self.eventQueue.append(event)

	def cycle(self):
# copy all current events from the cue and add them to the event set
# if the event Queue is empty then create and empty event set
		if len(self.eventQueue) != 0: 
			self.eventSets[self.setCount] = copy.deepcopy(self.eventQueue)
		else: 
			self.eventSets.append(self.__emptySet())
		self.totalEvents += len(self.eventQueue)
		self.eventQueue = []
		self.setCount += 1
		self.setCount = self.setCount%5
				
#check the total events ready to send and the number of eSets 
#send if necessary
		if self.totalEvents>=20 or self.setCount>=10:
#			print "trigger!", self.totalEvents, ':', self.setCount
			self.writeEventSets()
			self.totalEvents, self.setCount  = 0, 0

#cycle each devices in the device lise
		for d in self.devices: 	d.cycle()

		self.reactor.callLater(self.cycleLen, self.cycle)
	
	def __emptySet(self):
		return struct.pack('>H', 0) #chan len is 0 for empty set	

	def writeEventSets(self):
		bin = struct.pack(self.SEQ(), self.currentSeq)
		for set in self.eventSets:
			if set == self.__emptySet(): 
				bin += set
			else:
				bin += struct.pack(self.EVLEN(), len(set))
				for event in set:
			#		for d in event.getAddrList(): self.devices[d].receiveEvent(event)
			#	The above line is not needed as synthsoma will not have devices applying
			# 	events to other devices, they will only broadcast over the network
					bin += event.toBinary()
		self.currentSeq += 1	

		self.transport.write(bin, (self.bcast, self.port))
#		print "event Packets Written"

	def SEQ(self): return '>I'
	def EVLEN(self): return '>H'
