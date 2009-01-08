#!/usr/bin/python
import sys
from eegImport import EEGReader
from eeg import EEGSample
import dataPacketHandler

def loadWave(wavePath, numSamples, seqStart, srcChan, selChan):
	type = 1
	print "Loading  EEG "
	waveList, seq = [], seqStart
	waveFile = EEGReader(wavePath, selChan)
	
	for i in range(numSamples):
		sample = waveFile.getRecord(100)
		if sample == "%ENDFILE": break
		wavePacket = dataPacketHandler.encodePacket(seq, sample.toBinary(srcChan, type))
		waveList.append(wavePacket)
		seq += 1
	return waveList

def genFakeWave(numSamples, seqStart, srcChn):
	print "Generating fake EEG wave data"
	import time, math
	seq = seqStart
	waveList = []
	type = 1
	gain = 10000
	selChan, rateNumer, rateDenom, filid = 0, 4000, 1, 1

	for packet in range(numSamples):
		wave = EEGSample(selChan, rateNumer, rateDenom, filid, time.clock())
		samples = []

		for sample in range(100):
			samples.append(int(math.sin(2*math.pi*sample/100)*gain))
		wave.addChannel(samples)
		wave = dataPacketHandler.encodePacket(seq, wave.toBinary(srcChn,type))
		waveList.append(wave)
		seq += 1
	return waveList
