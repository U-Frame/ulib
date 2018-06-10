import fcntl
from bitarray import bitarray
from sys import getsizeof


class communication :

    def recive(self, VID, PID, interface, IN):
        file = open(VID + PID + "/" + interface + "/" + IN, "r")
	data = bitarray()
	data.frombytes( file.read())
	file.close()
        return data

    def send(self, VID, PID, interface, OUT, request, requestType, value, index, size, data):
	messege = bitarray( "{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:016b}".format(value) + "{0:016b}".format(index) + "{0:016b}".format(size) + "{0:0{width}b}".format(data, width = size))
        file = open(VID + PID + "/" + interface + "/" + OUT, "a")
        file.write(messege.tobytes())
	print(messege.tobytes())
	file.close()

    def ioctl(self, VID, PID, interface, IN, operation):
        file = open(VID+PID+"/"+interface+"/"+IN, "r+")
        fcntl.ioctl(file, operation)
	file.close()
