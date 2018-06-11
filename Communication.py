import fcntl
from bitarray import bitarray
from sys import getsizeof
import os


class communication:
	def recive(self, VID, PID, interface, endPoint, INn):
		if os.path.exists("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + INn):
			file = open("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + INn, "r")
			data = bitarray()
			data.frombytes(file.read())
			file.close()
			return data
		
		else:
		    	print("no such endpoint ,printing device descriptor...")


	def sendWord(self, VID, PID, interface, endPoint, OUTn, request, requestType, value, index, size):
		if os.path.exists("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn):
			messege = bitarray("{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:016b}".format(value) + "{0:016b}".format(index) + "{0:016b}".format(size))
			file = open("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn, "a")
			file.write(messege.tobytes())
			print(messege.tobytes())
			file.close()
		
		else:
		    	print("no such endpoint ,printing device descriptor...")


	def sendData(self, VID, PID, interface, endPoint, OUTn, size, data):
		if os.path.exists("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn):
			messege = bitarray("{0:0{width}b}".format(data, width=size))
			file = open("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUTn, "a")
			file.write(messege.tobytes())
			print(messege.tobytes())
			file.close()
		
		else:
		    	print("no such endpoint ,printing device descriptor...")



	def ioctl(self, VID, PID, interface, operation):
		file = open("dev/" + VID + "/" + PID + "/" + interface + "/" + "/00/00", "r+")
		buffer = 0
		fcntl.fcntl(file, operation, buffer)
		return buffer
		file.close()
