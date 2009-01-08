import struct
from channel import Channel		
class TSpike(object):
# Struct Codes: (http://docs.python.org/lib/module-struct.html)
		def TYPE(self): 	return 'B' 	# B - unsigned char 1 Byte
		def SRC(self):		return 'B'
		def CHANLEN(self): 	return '>H'	# H - unsigned short 2 Bytes
		def TIME(self): 	return '>Q'	# Q - unsigned longlong  8 Bytes
		def FILID(self): 	return '>I'	
		def VALID(self): 	return 'B'
		def SRCCHN(self): 	return 'B'
		def THOLD(self): 	return '>i'	# i - signed int  4 Bytes
		def SAMPLE(self): 	return '>i'		

		def __init__(self, timeStamp):
			self.type = 0
			self.src  = -1
			self.chanLen = 32
			self.time = timeStamp
			self.chans = [ Channel(), Channel(), Channel(), Channel()]

		def toBinary(self, src, type):
			self.src, self.type = src, type
			if self.src == -1 or self.type == -1:
				print "Type or Source net yet set! Type:", self.type, ' source:', self.src
				return "null"
			
			dataOut = ''
			dataOut += struct.pack(self.TYPE(), self.type)
			dataOut += struct.pack(self.SRC(), self.src)
			dataOut += struct.pack(self.CHANLEN(), self.chanLen)
			dataOut += struct.pack(self.TIME(), self.time)
			for chan in range(0,4):
				dataOut += struct.pack(self.SRCCHN(), self.chans[chan].srcch)
				dataOut += struct.pack(self.VALID(), self.chans[chan].valid)
				dataOut += struct.pack(self.FILID(), self.chans[chan].filid)
				dataOut += struct.pack(self.THOLD(), self.chans[chan].thold)
				for sample in range(0,32):
					dataOut += struct.pack(self.SAMPLE(), self.chans[chan].samples[sample])

			return dataOut

		def addChannel(self, chanNum, valid, filid, thold, samples):
			self.chans[chanNum].srcch = chanNum
			self.chans[chanNum].valid = 1
			self.chans[chanNum].filid = 0
			self.chans[chanNum].thold = thold
			self.chans[chanNum].samples = samples
			
		def setType(self, type):
			self.type = type

		def setSrc(self, src):
			self.src = src

		def getType(self):
			return self.src

		def getSrc(self):
			return self.type

		def __str__(self):
			string = ''
			string += "Type, Src: " + str(self.type) + "\t" + str(self.src) + '\n'
			string += "ChanLen: " + str(self.chanLen) + '\n'
			string += "Tstamp:" + str(self.time) + '\n'
			for chan in range(0,4):
				string += "========= Start " + str(chan) + " ========\n"
				string += "\tSrcCh:" + str( self.chans[chan].srcch ) + '\t'
				string += "\tValid:" + str( self.chans[chan].valid ) + '\n'
				string += "\tFilID:" + str( self.chans[chan].filid ) + '\n'
				string += "\tTHold:" + str( self.chans[chan].thold ) + '\n'
				string += "Samples:" + str( self.chans[chan].samples ) + '\n'
		
			return string
			

