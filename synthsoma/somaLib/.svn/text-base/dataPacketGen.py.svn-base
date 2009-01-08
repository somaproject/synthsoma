#!/usr/bin/python
import struct

#creates a predefined number of packets and returns them as a group
def genPackets(numPackets):
	sequence = 0
	data = "Oh me? I'm the doctor"
	packets=[]
	seq=0
	while seq<numPackets:
		packets.append(struct.pack('>I', seq) + data)
		seq = seq + 1
	return packets
