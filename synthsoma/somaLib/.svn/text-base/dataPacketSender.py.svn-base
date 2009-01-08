#!/usr/bin/python

#this program will do a couple of things:
#	1- have an infinite list of data packets (looped packets)
#	2- send those packets sequentially to 192.168.255.255 
#	3- listen to for dataPacketReTx requests 
#		-if the request comes & packet is still stored then send the requested packet
#	4- Keep a cache of recently sent packest (to answer requests, see above)
#	5- ignore any requests for packets that are not in the cache
#	6- continue looping until the user kills the program
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from socket import SOL_SOCKET, SO_BROADCAST
import socket, sys, time, errno
import dataPacketHandler, dataPacketGen

#each class needs access to these variables
#----------------------------------------------------------------------
# Sends datagram packets over the network on given port
class DataPacketSender(DatagramProtocol):
	def __init__(self,ip, port,sleep, reactor, pList):
		self.port = port
		self.reactor = reactor
		self.sleep = sleep
		self.bcast = ip

		self.packetList = pList
		self.packetCache = {} 
# I have a cache and a list of the cache for fast access, and easy removal of 
#old packets
		self.packetCacheList = []
		self.cacheMaxSize = 250


	def startProtocol(self):
		self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
		self.sendPackets()
		
	def sendPackets(self):
		data = self.packetList.pop(0)
		seq = dataPacketHandler.getPacketSeq(data)
#		print "Writing:" #, data
		self.transport.write(data,(self.bcast,self.port))
		self.cachePacket(data)  # save if packet is needed in a ReTx
		
#		print "Getting old seq"
		seqNew = self.getSequence()+1  # as the packet list goes 1 -> 2 -> ... -> n ->1  but we can't do this we seq numbers so we need to update them to a new number everytime we paste the packet back into the list
		seqOld, pData = dataPacketHandler.decodePacket(data)
		newData = dataPacketHandler.encodePacket(seqNew, pData)

		self.packetList.append(newData) #adds spike to end of list
#		print "sleeping"
		self.reactor.callLater(self.sleep, self.sendPackets)

	def cachePacket(self, data):
		#add current packet to cache, check cache size, if too big remove a packet
		seq = dataPacketHandler.getPacketSeq(data)
		self.packetCache[seq] = data
		self.packetCacheList.append(seq)		
		if len(self.packetCacheList)>self.cacheMaxSize:
			del self.packetCache[self.packetCacheList.pop(0)] # remove oldest entry from packetCache, which should be at index 0 or packetCacheList
	
	def requestReTx(self, seq):
		if seq in self.packetCache:
			print seq, ": in cache, resending packet"
			dataResend = self.packetCache[seq]
			self.packetList.insert(0, dataResend)
		else: print "\t\tI don't have it"

	def getSequence(self):
		packet = self.packetList.pop()
		lastSeq, data = dataPacketHandler.decodePacket(packet)
		self.packetList.append(packet)
#		print lastSeq, " <---------- Last Seq"
		return lastSeq

#--------------------------------------------------------------------
# Listens for ReTx packets, if one is received it searches for the 
# appropriate packet in the cache and appends it to the front of the
# packetList.

class DataReTxListener(DatagramProtocol):
	def __init__(self,reactor):
		self.reactor = reactor
		self.senderList = []

	#when datagram received, check the seq number, if seq is in cache
	#resend the packet
	def datagramReceived(self, data, (host,port)):
		seq = dataPacketHandler.getPacketSeq(data)
		print "ReTx request received: ", seq
		for sender in senderList:
			sender.requestReTx(seq)
	
	def appendSenderList(self, senderList):
		for member in senderList:
			self.senderList.append(member)


#--------------End Data Packet Sender (Re Tx)  Classes----------------



#--------------start() generic packets sending------------------------
	# start the whole process
def start():
	
	print "Getting packets"
	pList = dataPacketGen.genPackets(10000)
	pCache = {}
	pCacheList = []
	bcast = "192.168.255.255"
	cacheMaxSize = 10000	
	bcastPort = 4000	
	reTxPort  = 4100
	print "setting up port:", bcastPort
	reactor.listenUDP(0, DataPacketSender(bcastPort, reactor, pList, pCache, pCacheList, cacheMaxSize))
	print "setting up ReTxPort:", reTxPort
	reactor.listenUDP(reTxPort, DataReTxListener(reactor, pList, pCache))
	reactor.run()

#--------------------------------------------------------------------
if __name__=="__main__":
	start()
