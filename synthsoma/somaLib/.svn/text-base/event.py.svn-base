#!/usr/bin/python
import struct

class EventTxResp(object):
	
	def __init__(self, nonce, success):
		self.nonce = nonce
		self.success = success
	
	def toBinary(self):
		bin = struct.pack(self.NONCE(), self.nonce)
		bin += struct.pack(self.SUCCESS(), self.success)
		return bin 
	
	def NONCE(self): 	return '>H'
	def SUCCESS(self):	return '>H'

#----------------------------------------------------------------------
class EventTxParser(object):

	def NONCE(self):    return '>H'
	def ECNT(self):     return '>H'
	def EADDR(self):    return '>H'
	def CMD(self): 		return 'B'
	def SRC(self):		return 'B'
    #NEED TO FINISH THE EventTx object packers

	def __init__(self, data):
		self.data = data
		self.nonce = struct.unpack(self.NONCE(), self.data[0:2])[0]
		self.numEvents = struct.unpack(self.ECNT(), self.data[2:4])[0]
		self.data = self.data[4:]
		self.events = []

	def getNonce(self):
		return self.nonce

	def getEcnt(self):
		return self.numEvent

	def getEventList(self):
		for i in range(self.numEvents):
			self.events.append(self.__getNextEvent())
		return self.events

	def __getNextEvent(self):
		e = self.data[0:22]
		self.data = self.data[32:]  
		addrList = self.__getAddresses(e[0:10])
		cmd = struct.unpack(self.CMD(), e[10:11])[0]
		src = struct.unpack(self.SRC(), e[11:12])[0]
		dataOut = e[12:]
		return Event(addrList,cmd,src,dataOut)
	
	def __getAddresses(self, data):
		byte2Addr = [0,0,0,0,0]
		byte2Addr[0] = struct.unpack(self.EADDR(), data[0:2])[0]
		byte2Addr[1] = struct.unpack(self.EADDR(), data[2:4])[0]
		byte2Addr[2] = struct.unpack(self.EADDR(), data[4:6])[0]
		byte2Addr[3] = struct.unpack(self.EADDR(), data[6:8])[0]
		byte2Addr[4] = struct.unpack(self.EADDR(), data[8:10])[0]
		targets= [] #A list of the devices targeted by the event addr
		for i in range(5): # for each of the 5 2byte addresses
			for j in range(16): # each bit in the 2byte addresses
				if (byte2Addr[i] & j ): targets.append( (i*16+j))

		return  targets
	
#-----------------------------------------------------------------
class Event(object):
	def __init__(self,addr, cmd, src, data):
		self.addr = addr
		self.cmd = cmd
		self.src = src
		self.data = data #5 bytes of data
	
	def getAddrList(self): return self.addr
	def getCmd(self): return self.cmd
	def getSrc(self): return self.src
	def getData(self): return self.data

	def apply(self): #its unclear if the application of the event includes applying the binary of the cmd,src,data or if it is made up of giving the device the cmd src and data and letting the device figure the rest out
		return self.cmd, self.src, self.data
	
	def toBinary(self):
		bin = ''
		bin += struct.pack(self.CMD(), self.cmd)
		bin += struct.pack(self.SRC(), self.src)
		bin += self.data
		return bin

	def CMD(self): return 'B'
	def SRC(self): return 'B'
	def ADDR(self): return '>H'
	
	
