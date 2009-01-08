#!/usr/bin/python
import sys
import struct
from tSpike import TSpike

class TTReader():

	def __init__(self,path):
		self.file = open(path,'r')
		print "Opened:",path, ' successfully'
		self.tholds =[0,0,0,0,0,0,0,0]
		self.gains = [0,0,0,0,0,0,0,0]
		self.headerParsed = False	

#------------------------ read Header ---------------------------------
	def readHeader(self):
		self.headerParsed = True
		probe = 0
		line = ''
#		print "START HEADER"
		while line!="%%ENDHEADER":	
		
			line = self.file.readline()
			line = line[0:(len(line)-1)] #remove end line char		

			# for the EXACT slicing indexs see below. I have a diagram
			# that shows how I got the EXACT slicing indecies		
			if line[0:1]=='%' and line[2:8]=="Probe:":
				probe = int(line[8:len(line)])
#				print "Probe set to:", probe
			
			if line[0:1]=='%' and line[2:9]=="channel":
				chanNum = int(line[10:11])		

				if line[12:20] == 'ampgain:':
					self.gains[chanNum] = int(line[20:len(line)])
				if line[12:22] == 'threshold:': # Thresholds follow gains, so we can do this
					self.tholds[chanNum] = int(line[22:len(line)])
#					print "Channel:", chanNum, " gain:",self.gains[chanNum], " thold:", self.tholds[chanNum]		

#		print "END HEADER", 
	
		if probe:
#			print "Probe = 1, taking chans 4:7"
			self.tholds = self.tholds[4:8]
			self.gains = self.gains[4:8]
		else:
#			print "Probe = 0, taking chans 0:3"
			self.tholds = self.tholds[0:4]	
			self.gains = self.gains[0:4]	
#		print "THOLDS ---:" + str(self.tholds)


# method reads a tspike from a TT file and returns a TSpike objectSomaObj.SPIKE
#-------------------------getSpike()------------------------------
	def getSpike(self):
		#Has the header been read? If not read it!
		if not self.headerParsed: self.readHeader()

		line = self.file.read(260) #read 262 bytes as there are 262 bytes per spike
		if len(line)<260:
			return "%ENDFILE"

		#TS in tt file is in AD units, to convert to soma units multiply by 5
		timeStamp = struct.unpack('I', line[0:4])[0]*5 
		spike = TSpike(timeStamp)

		line = line[4:len(line)] #cut off first 6 bytes of fluff
		chans = [ [], [], [], [] ]

		for i in range(0,32):  
			offset = i * 4 * 2
			for chanNum in range(0,8,2):
				if self.gains[chanNum/2] == 0:
					sample = 0
				else:
					sample = struct.unpack('h', line[ offset+chanNum : offset+chanNum+2 ])[0]
					sample = sample/4096.0 * 10.0 / self.gains[int(chanNum/2)] * 1e9
				chans[int(chanNum/2)].append(int(sample))

		VALID, FILID = 1, 0
		chanNum=0
		for chanNum in range(0,4):
			spike.addChannel(chanNum, VALID, FILID, self.tholds[chanNum], chans[chanNum])
		
		return spike
#----------------------- END getSpike -----------------------


	# |%| |C|h|a|n|n|e|l| |#| |a|m|p|g|a|i|n|:| | | | | |
	# |%| |P|r|o|b|e|:| |1| | | | | | | | | | | | | | | |
	# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 
	# 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2


if __name__=="__main__":
	
	c = TTReader("/home/slayton/data/t16.tt")
	s = c.getSpike()
	print s
	bin = s.toBinary()
	print len(bin)
