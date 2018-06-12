import fcntl
from bitarray import bitarray
from sys import getsizeof
import os


IN = "1"
OUT = "2"


def checkForEndPointNodes(dev, VID, PID, interface, endPoint):
	for INn in range(1, 16):
		if os.path.exists(dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + IN + "{0:02}".format(INn)) == False:
			break
		print("IN"+str(INn))

	for OUTn in range(1, 16):
		if os.path.exists(dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUT + "{0:02}".format(OUTn)) == False:
			break
		print("OUT"+str(OUTn))



def availableEndpoints(dev, VID, PID, interface, endPoint):
	if endPoint == "00":
		print("control :")
		checkForEndPointNodes(dev, VID, PID, interface, endPoint)
	
	elif endPoint == "01":
		print("bulk :")
		checkForEndPointNodes(dev, VID, PID, interface, endPoint)
	
	elif endPoint == "02":
		print("interrupt :")
		checkForEndPointNodes(dev, VID, PID, interface, endPoint)
	
	elif endPoint == "03":
		print("isochronous:")
		checkForEndPointNodes(dev, VID, PID, interface, endPoint)



class communication:
	def __init__(self):
		self.dev = "/home/samir/Documents/dev"

	def recive(self, VID, PID, interface, endPoint, INn):
		if os.path.exists(self.dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + INn):
			file = open(self.dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + INn, "r")
			data = bitarray()
			data.frombytes(file.read())
			file.close()
			return data
		
		else:
		    	print("no such endpoint ,printing available nodes :")
			availableEndpoints(self.dev, VID, PID, interface, endPoint)
			

	def sendWord(self, VID, PID, interface, endPoint, OUTn, request, requestType, value, index, size):
		if os.path.exists(self.dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn):
			messege = bitarray("{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:016b}".format(value) + "{0:016b}".format(index) + "{0:016b}".format(size))
			file = open(self.dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn, "a")
			file.write(messege.tobytes())
			print(messege.tobytes())
			file.close()
		
		else:
		    	print("no such endpoint ,printing available nodes :")
			availableEndpoints(self.dev, VID, PID, interface, endPoint)


	def sendData(self, VID, PID, interface, endPoint, OUTn, size, data):
		if os.path.exists(self.dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn):
			messege = bitarray("{0:0{width}b}".format(data, width=size))
			file = open(self.dev + "/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn, "a")
			file.write(messege.tobytes())
			print(messege.tobytes())
			file.close()
		
		else:
		    	print("no such endpoint ,printing available nodes :")
			availableEndpoints(self.dev, VID, PID, interface, endPoint)



	def ioctl(self, VID, PID, interface, operation):
		file = open(self.dev + "/" + VID + "/" + PID + "/" + interface + "/" + "/00/00", "r+")
		buffer = 0
		fcntl.fcntl(file, operation, buffer)
		return buffer
		file.close()
