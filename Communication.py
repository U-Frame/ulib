import fcntl
from bitarray import bitarray
import os


OUT = 0
IN = 1



class communication:
	def __init__(self):
		self.dev = "/home/samir/Documents/dev"

	def checkForEndPointNodes(self, vid, pid, interface, endPoint):
		for OUTn in range(1, 16):
			if os.path.exists(self.getPath(self.dev, vid, pid, interface, endPoint, OUTn)) == False:
				break
			print("OUT"+str(OUTn))
		for INn in range(101, 116):
			if os.path.exists(self.getPath(self.dev, vid, pid, interface, endPoint, INn)) == False:
				break
			print("IN"+str(INn%100))

	def availableEndpoints(self, vid, pid, interface, endPoint):
		if endPoint == 0:
			print("control :")
			self.checkForEndPointNodes(vid, pid, interface, endPoint)
		elif endPoint == 1:
			print("bulk :")
			self.checkForEndPointNodes(vid, pid, interface, endPoint)
		elif endPoint == 2:
			print("interrupt :")
			self.checkForEndPointNodes(vid, pid, interface, endPoint)
		elif endPoint == 3:
			print("isochronous:")
			self.checkForEndPointNodes(vid, pid, interface, endPoint)

	def recive(self, vid, pid, interface, endPoint, INn):
		fd = self.getPath(self.dev, vid, pid, interface, endPoint, INn)
		if os.path.exists(fd):
			file = open(fd, "r")
			data = file.read()
			file.close()
			return data
		
		else:
		    	print("no such endpoint ,printing available nodes :")
			self.availableEndpoints(self.dev, VID, PID, interface, endPoint)
			

	def sendWord(self, vid, pid, interface, endPoint, OUTn, request, requestType, value, index, size):
		fd = self.getPath(self.dev, vid, pid, interface, endPoint, OUTn)
		if os.path.exists(fd):
			messege = self.formRequest(request, requestType, value, index, size)
			file = open(fd, "a")
			file.write(messege)
			print(messege)
			file.close()
		
		else:
			print("no such endpoint ,printing available nodes :")
			self.availableEndpoints(self.dev, vid, pid, interface, endPoint)


	def sendData(self, vid, pid, interface, endPoint, OUTn, size, data):
		fd = self.getPath(self.dev, vid, pid, interface, endPoint, OUTn)
		if os.path.exists(fd):
			messege = self.getByteRepresentation(data, size)
			file = open(fd, "a")
			file.write(messege)
			print(messege)
			file.close()
		
		else:
		    	print("no such endpoint ,printing available nodes :")
			self.availableEndpoints(vid, pid, interface, endPoint)


	def ioctl(self, vid, pid, interface, endPoint, INn, request, requestType, value, index, size, operation):
		fd = self.getPath(self.dev, vid, pid, interface, endPoint, INn)
		file = open(fd, "r+")
		buffer = self.formRequest(request, requestType, value, index, size)
		fcntl.ioctl(file, operation, buffer)
		file.close()
		return buffer
		
	def getPath(self, dev, vid, pid,interface, endPoint, IO):
		return dev + "/" + "{0:02}".format(vid) + "/" + "{0:02}".format(pid) + "/" + "{0:02}".format(interface) + "/" + "{0:02}".format(endPoint) + "/" + "{0:03}".format(IO)
		
	def getByteRepresentation(self, data, size):
		return bitarray("{0:0{width}b}".format(data, width=size)).tobytes()
		
	def formRequest(self, request, requestType, value, index, size):
		return bitarray("{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:016b}".format(value) + "{0:016b}".format(index) + "{0:016b}".format(size)).tobytes()
	
