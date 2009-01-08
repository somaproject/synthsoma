#!/usr/bin/python
import sys, struct
from eeg import EEGSample


class EEGReader(object):
	
	def __init__(self, path, chanNum):
		self.file = open(path,'r')
		print "Opened:", path, 'successfully'
		self.gains = [0,0,0,0,0,0,0,0]
		self.offset = [0,0,0,0,0,0,0,0]
		self.rate = 0
		self.bufferSize = 0
		self.readHeader()
		self.chanNum = chanNum
		self.buffer = []
		self.time = 0

	def SAMP(self): return 'h'
	def TIME(self): return 'I'

	def getRate(self): return self.rate	

	def readHeader(self):
		line = ''
		while line != '%%ENDHEADER':
			line = self.file.readline()
			line = line[0:len(line)-1] #remove  \n character
			
			if line[0:1]=='%' and line[2:6] == "rate":
				self.rate = float(line[7:])			

			if line[0:1]=='%' and line[2:14] == "dma_bufsize:":
				self.bufferSize = int(line[14:])

			if line[0:1]=='%' and line[2:9] == "channel":
				chanNum = int(line[10:11])
				
				if line[12:20] == "ampgain:":
					self.gains[chanNum] = int(line[20:])

#		print "EEG Sampling Rate:", self.rate
#		print "EEG gains:", self.gains
#		print "EEG Buffer:", self.bufferSize
#		print "----------------%%ENDHEADER"
		
	def getRecord(self, numSample):
		eegSamples = []
		rateNumer = int(self.rate)

		rateDenom = 1
		
		if len(self.buffer)<numSample: 
			if self.readFromFile()=='%ENDFILE': return "%ENDFILE"

		for i in range(numSample): 
			eegSamples.append(self.buffer.pop(0))

		eegOut = EEGSample(self.chanNum, 1, rateNumer, rateDenom, self.time)
		eegOut.addChannel(eegSamples)
		self.time += (500.0 / self.rate *1e4)
		return eegOut


	def readFromFile(self):

		line = self.file.read(4 + self.bufferSize*2)
		if len(line)<(4+self.bufferSize*2):
			return '%ENDFILE'

		timeStamp = struct.unpack(self.TIME(), line[0:4])[0]
		if self.time == 0 : 
			self.time=timeStamp*5
		line = line[4:]

		for samp in range(self.bufferSize/8): #8 channels per sample
			offset = samp * 8 * 2
#			print "----------------------------"
			for chan in range(0, 16, 2):
				if chan/2 == self.chanNum:
					if self.gains[chan/2] ==0:
						sample = 0
					else:
						sample = (struct.unpack(self.SAMP(), line[offset+chan:offset+chan+2])[0])
						sample = float(sample)/4096.0 * 10.0 / float(self.gains[chan/2]) * 1e9
						self.buffer.append(int(sample))
			
				
#		print timeStamp


#if __name__=="__main__":

#	r = EEGReader('/home/slayton/data/eeg1.eeg', 1)

#	for i in range(2500):
#		rec = r.getRecord(100)	
#		line = (rec.toBinary(1,1))
#		ts = line[12:20]
#		print struct.unpack('>Q', ts)[0]	
#	r.getRecord()
#	r.getRecord()

