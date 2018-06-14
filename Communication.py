import fcntl
from bitarray import bitarray
import os
import struct
import array


OUT = 0
IN = 1



class communication:
	def __init__(self, vid, pid, interface):
		self.vid = vid
		self.pid = pid
		self.interface = interface
		self.root = "/home/samir/Documents/dev/uframe" + "/" + str(self.vid) + "/" + str(self.pid) + "/" + str(self.interface) + "/"

	def checkForEndPointNodes(self, endPoint):
		for OUTn in range(1, 16):
			if os.path.exists(self.getPath(endPoint, OUTn)) == False:
				break
			print("OUT"+str(OUTn))
		for INn in range(101, 116):
			if os.path.exists(self.getPath(endPoint, INn)) == False:
				break
			print("IN"+str(INn%100))

	def availableEndpoints(self, endPoint):
		if endPoint == 0:
			print("control :")
			self.checkForEndPointNodes(endPoint)
		elif endPoint == 1:
			print("bulk :")
			self.checkForEndPointNodes(endPoint)
		elif endPoint == 2:
			print("interrupt :")
			self.checkForEndPointNodes(endPoint)
		elif endPoint == 3:
			print("isochronous:")
			self.checkForEndPointNodes(endPoint)

	def recive(self, endPoint, INn, request = None, requestType = None, value = None, index = None, size = None, data = None, operation = 1):
		if request == None:
			fd = self.getPath(endPoint, INn)
			if os.path.exists(fd):
				file = open(fd, "r+")
				data = file.read()
				file.close()
				return data
			
			else:
				print("no such endpoint ,printing available nodes :")
				self.availableEndpoints(endPoint)
		else :
			fd = self.getPath(endPoint, INn)
			file = open(fd, "r+")
			byteBuffer = bytearray(self.formRequestPacket(request, requestType, value, index, size))
			for d in data :
				byteBuffer.append(d)
			tempBuffer = array.array("B", byteBuffer)
			buffer = array.array("c", tempBuffer.tostring())
			#print (buffer)
			fcntl.ioctl(file, operation, buffer, 1)
			file.close()
			#print (buffer)
			return buffer[8:].tostring()
				
				
	def send(self, endPoint, OUTn, request = None, requestType = None, value = None, index = None, size = None, data = None):
		fd = self.getPath(endPoint, OUTn)
		messege = ""
		if os.path.exists(fd):
			if request != None:
				messege = messege + self.formRequestPacket(request, requestType, value, index, size) 
			if data != None:
				messege = messege + data
			file = open(fd, "w")
			file.write(messege)
			file.close()
		
		else:
		    	print("no such endpoint ,printing available nodes :")
			self.availableEndpoints(endPoint)
			
		
	def getPath(self, endPoint, IOn):
		return self.root + "{0:02}".format(endPoint) + "/" + "{0:03}".format(IOn)
		
	def formRequestPacket(self, request, requestType, value, index, size):
		return bitarray("{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:<016b}".format(value) + "{0:<016b}".format(index) + "{0:<016b}".format(size)).tobytes()
	
