#!/usr/bin/python
import sys,time
from ttImport import TTReader
import dataPacketHandler
from tSpike import TSpike

def loadSpikes(ttPath, seqStart, numSpikes, srcChan):
	type = 0
	print "Loading real spikes"
	sList, seq = [], seqStart
	ttFile = TTReader(ttPath)
	ttFile.readHeader()
	print "LOADING SPIKES, depending spikeNum this may take some time...."
	for i in range(numSpikes):
		spike = ttFile.getSpike()
		if spike == "%ENDFILE": break
		s = dataPacketHandler.encodePacket(seq, spike.toBinary(srcChan, type))
		sList.append(s)
		seq += 1
	print "tSpikes loaded!"
	return sList

def genFakeSpikes(numSpikes, seqStart, srcChn):
	print "Generating fake spikes"
	seq = seqStart
	sList = []
	type = 0
	for i in range(numSpikes):
		spike = TSpike(time.clock())
		chan1 = [30000 * (((i+0)%4)+4) -100000] * 32;
		chan2 = [30000 * (((i+2)%4)+4) -100000] * 32;
		chan3 = [30000 * (((i+3)%4)+4) -100000] * 32;
		chan4 = [30000 * (((i+4)%4)+4) -100000] * 32;
		spike.addChannel(0, 1, 0, 250, chan1)
		spike.addChannel(1, 1, 0, 250, chan2)
		spike.addChannel(2, 1, 0, 250, chan3)
		spike.addChannel(3, 1, 0, 250, chan4)
		s = dataPacketHandler.encodePacket(seq, spike.toBinary(srcChn, type))
		sList.append(s)
		seq += 1
	print "Fake Spike data GENERATED!"
	return sList

