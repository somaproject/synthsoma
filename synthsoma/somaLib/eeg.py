#!/usr/bin/python
import struct

class EEGSample(object):

	def TYPE(self):		return 'B'
	def SRC(self):		return 'B'
	def LEN(self):		return '>H'
	def SELCHAN(self):	return '>H'
	def RATE_NUMER(self):	return '>H'
	def RATE_DENOM(self):	return '>H'
	def FILID(self):	return '>H'
	def TIME(self):		return '>Q'
	def SAMP(self):		return '>i'


	def __init__(self, selChan, numer, denom, filid, time):
		self.type = -1
		self.src  = -1
		self.selChan = selChan
		self.rate_numer = numer
		self.rate_denom = denom
		self.filid = filid
		self.time = time
		self.samples = []

	def addChannel(self, samples):
		self.samples = samples
	
	def toString(self):
		return self.samples

	def toBinary(self, src, type):
		self.src, self.type = src, type
		if self.src == -1 or self.type == -1:
			print "Type or Source net yet set! Type:", self.type, ' source:', self.src
			return "null"
		dataOut = ''
		dataOut += struct.pack(self.TYPE(), self.type)
		dataOut += struct.pack(self.SRC(), self.src)
		dataOut += struct.pack(self.LEN(), len(self.samples))
		dataOut += struct.pack(self.SELCHAN(), self.selChan)
		dataOut += struct.pack(self.RATE_NUMER(), self.rate_numer)
		dataOut += struct.pack(self.RATE_DENOM(), self.rate_denom)
		dataOut += struct.pack(self.FILID(), self.filid)
		dataOut += struct.pack(self.TIME(), self.time)
		#print len(self.samples)
		for sample in self.samples:
			dataOut += struct.pack(self.SAMP(), int(sample))

		return dataOut
