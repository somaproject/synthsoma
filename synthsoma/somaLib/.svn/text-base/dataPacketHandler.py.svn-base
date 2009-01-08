#!/usr/bin/python
import struct

def decodePacket(dataIn):

	# id = struct.unpack(fmt, val) returns a tupple
	# id = ( someValue, ).  The [0] at the end of the
	# lines extacts someValue as a number from the tupple

	sequence = struct.unpack('>I', dataIn[0:4])[0]

	# Technically we only need to unpack the first 4 bytes and ensure
	# that we are receiving the packets in the correct order. However
	# for uses in FakeSoma we will also grab the type and src information
	# although these two attributes will be also passed on to the TSPike
	# decodeder

	# the len field doesn't need to be parsed now. We can let the
	# individual coders/decoders use those
	
	# the data that follows the header needs to be interpretted by 
	# depending on what type of packet this is. If it is a TSPike
	# then it needs to be decoded by tspikePacketHandler and so on
	# so although this data will be process later we need to know
	# how to process it so we grab that data now. 
	# But we leave it on the packet

	data = dataIn[4:len(dataIn)]

	return sequence, data		

def getPacketSeq(dataIn):
	return struct.unpack('>I', dataIn[0:4])[0]

def getPacketSrc(dataIn):
	return struct.unpack('>H', dataIn[5:6])[0]

def encodePacket(sequence, data):
	
	# Again as stated above this module is only concerend with general
	# data packets. the 

	dataOut =  struct.pack('>I', sequence)	 
	dataOut = dataOut + data
 
	return dataOut

