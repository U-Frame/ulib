import fcntl
from bitarray import bitarray
from sys import getsizeof


class communication:

	def recive(self, VID, PID, interface, endPoint, IN):
		if os.path.isdir("dev/" + VID + "/" + VID + "/" + interface + "/" + endPoint + "/" + IN):
			file = open("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + IN, "r")
			data = bitarray()
			data.frombytes(file.read())
			file.close()
			return data
		
		else:
		    	print("no such endpoint ,printing device descriptor...")


	def send(self, VID, PID, interface, endPoint, OUT, request, requestType, value, index, size, data):
		if os.path.isdir("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUT):
			messege = bitarray("{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:016b}".format(value) + "{0:016b}".format(index) + "{0:016b}".format(size) + "{0:0{width}b}".format(data, width=size))
			file = open("dev/" + VID + "/" + PID + "/" + interface + "/" + endPoint + "/" + OUT, "a")
			file.write(messege.tobytes())
			print(messege.tobytes())
			file.close()
		
		else:
		    	print("no such endpoint ,printing device descriptor...")



	def ioctl(self, VID, PID, interface, IN, operation):
		file = open("dev/" + VID + "/" + PID + "/" + interface + "/" + "/00" + OUT, "r+")
		fcntl.ioctl(file, operation)
		file.close()
