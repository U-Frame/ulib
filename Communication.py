import fcntl
from bitarray import bitarray
import os
import struct
import array

def non_block_read(output):
	fd = output.fileno()
	fl = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
	try:
		return output.read()
	except:
		return ""

OUT = 0
IN = 1



class communication:
	def __init__(self, vid, pid, interface):
		self.vid = vid
		self.pid = pid
		self.interface = interface
		self.root = "/home/samir/Documents/dev/uframe" + "/" + self.vid + "/" + self.pid + "/" + self.interface + "/"
		structure = struct.pack("i", 0)
		control = open(self.getPath("Interrupt", 11), "r")
		buffer = array.array("i", structure)
		operation = 0
		fcntl.ioctl(control, operation, buffer, 1)
		control.close()
		self.WordLength = buffer[0]
		print (self.WordLength)

	def checkForEndPointNodes(self, endPoint):
		for OUTn in range(0, 150, 10):
			if os.path.exists(self.getPath(endPoint, OUTn)) == False:
				break
			print( "OUT" + str( (int)(OUTn/10) ) ) 
		for INn in range(1, 151, 10):
			if os.path.exists(self.getPath(endPoint, INn)) == False:
				break
			print( "IN" + str( (int)(OUTn/10) ) ) 

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

		path = self.getPath(endPoint, INn)
		if request == None:
			if os.path.exists(path): 
				#file = open(path, "r")
				try:
					f = os.open(path, os.O_RDONLY)
					#data = file.read(self.WordLength)
					data = os.read(f, 18)
					#data = f.read()
				except Exception as e:
					print(e)
					data = None
					pass
				#file.close()
				return data
			
			else:
				print("no such endpoint ,printing available nodes :")
				self.availableEndpoints(endPoint)
		else :
			file = open(path, "r+")
			byteBuffer = bytearray(self.formRequestPacket(request, requestType, value, index, size))
			for d in data :
				byteBuffer.append(d)
			tempBuffer = array.array("B", byteBuffer)
			buffer = array.array("c", tempBuffer.tostring())
			fcntl.ioctl(file, operation, buffer, 1)
			file.close()
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
		return self.root + endPoint + "/" + "{0:03}".format(IOn)
		
	def formRequestPacket(self, request, requestType, value, index, size):
		return bitarray("{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:<016b}".format(value) + "{0:<016b}".format(index) + "{0:<016b}".format(size)).tobytes()

