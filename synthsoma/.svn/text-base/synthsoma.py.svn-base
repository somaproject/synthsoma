#/usr/bin/python
from twisted.internet import reactor

from somaLib.device import Device, Timer
from somaLib.eventBroadcaster import EventBroadcaster
from somaLib.eventTxReceiver import EventTxReceiver

from somaLib.ttImport import TTReader
from somaLib.dataPacketSender import DataPacketSender, DataReTxListener
from somaLib.spikeLoader import loadSpikes, genFakeSpikes
from somaLib.eegLoader import loadWave, genFakeWave

class SyntheticSoma(object):
	
	def __init__(self, ip):
		self.r = reactor		
		self.reactorRunning = False

		self.tspikeSenders = []
		self.numSpikeSources = 0

		self.waveSenders = []
		self.numWaveSources = 0
			
		self.devices = []
		self.ip = ip
		
		self.ReTxListener = DataReTxListener(reactor)
		self.reTxPort = 400

		self.spikes = False
		self.waves = False
		self.events = False


	def addSpikeSource(self, file, numSpikes, rate):
			
		if self.reactorRunning:
			print "Sources cannot be changed once the reactor has started"
			return

		seq = 1000 * self.numSpikeSources
		chan = self.numSpikeSources


		if file == "genSpikes":
			newSource = genFakeSpikes(numSpikes,seq,chan)
		else:
			newSource = loadSpikes(file,seq,numSpikes,chan)

		dataPacketSender = DataPacketSender(self.ip, 4000+chan, float(1)/rate, self.r, newSource)
		self.tspikeSenders.append(dataPacketSender)
		self.numSpikeSources += 1
		self.spikes = True
	
	def addWaveSource(self,file,numSamples,waveChan):

		if self.reactorRunning:
			print "Sources cannot be changed once the reactor has started"
			return

		seq = 10000 + 1000 * self.numWaveSources
		chan = self.numWaveSources

		if file == "genWaves":
			newSource = genFakeWave(numSamples, seq, chan)
		else:
			newSource = loadWave(file, numSamples, seq, chan, waveChan)

		dataPacketSender = DataPacketSender(self.ip, 4064+chan, float(1)/4000, self.r, newSource)
		self.waveSenders.append(dataPacketSender)
		self.numWaveSources += 1
		self.waves = True	

	def enableEvents(self):
		self.devices.append(Timer(0))
		for i in range(79):
			self.devices.append(Device(i+1))
		self.events = True

 	def start(self):
		
		print "\n\n"

		if self.spikes:
			print "Enabling .tt file transmission for:", len(self.tspikeSenders), ' sources'
			for sender in self.tspikeSenders:
				reactor.listenUDP(0, sender)

		if self.waves:
			print "Enabling .eeg file transmission for: ", len(self.waveSenders), ' sources'
			for sender in self.waveSenders:
				reactor.listenUDP(0,sender)

		if self.events:
			print "Enabling events"
			eventBCast = EventBroadcaster(20e-5, self.ip, 5000, self.devices, reactor)
			eventTxRx = EventTxReceiver(reactor,self.devices)
			reactor.listenUDP(0,eventBCast)
			reactor.listenUDP(5100, eventTxRx)
		
		print "Sythetic Soma is running..."
		print "\t\t (Press Ctrl+C to quit)"

		reactor.run()

	def stop(self):
		reactor.stop()

