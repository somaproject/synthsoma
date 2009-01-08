from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from socket import SOL_SOCKET, SO_BROADCAST
import socket, sys, time, errno, copy
from event import EventTxParser, EventTxResp, Event
from device import Device

class EventTxReceiver(DatagramProtocol):
	def __init__(self, reactor, devices):
		self.devices = devices
#		print "EventTx Receiver started"
	
	def datagramReceived(self, data, (host, port)):
		if port != 5100:
			return
		eParser = EventTxParser(data)
		nonce = eParser.getNonce()		
#print nonce, " received ", len(data), ': len'

		success = self.applyEvents(eParser.getEventList())
		resp = EventTxResp(nonce, success).toBinary()
#		print len(resp), ": response len (should be 4)"
		self.transport.write(resp, (host, port))

#this method simply parses the event, then passes them to the devices
	def applyEvents(self, eList):
		for event in eList:
			deviceAddrList = event.getAddrList()
			for dNum in deviceAddrList:
				self.devices[dNum].receiveEvent(event) 
				#devices.apply (takes 3 arguments, cmd,src,data	
		return 1
	# when the EventTxRx object receives a list of events it sends it. It 
	# doesn't care when the last eventPacket was sent or how many events
	# are in the packet. Whoever is invoking the method bcastEvent() is
	# responsible that the protocols outlined are being followed

