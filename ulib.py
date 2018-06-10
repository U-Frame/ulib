import fcntl
from bitarray import bitarray
from sys import getsizeof


class communication :

    def recive(self, interface, IN):
        file = open(interface+"/"+IN, "r")
	data = bitarray()
	data.frombytes( file.read())
	file.close()
        return data

    def send(self, interface, IN,request, requestType, value, index, size, data):
	#print(len("{0:0{width}b}".format(data, width = size)))
	messege = bitarray( "{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:016b}".format(value) + "{0:016b}".format(index) + "{0:016b}".format(size) + "{0:0{width}b}".format(data, width = size))
        file = open(interface+"/" + IN, "a")
        file.write(messege.tobytes())
	print(messege.tobytes())
	file.close()

    def ioctl(self, interface, IN, operation):
        file = open(interface+"/"+IN, "r+")
        fcntl.ioctl(file, operation)
	file.close()

if __name__ == "__main__":
	como = communication()
	como.send("new", "5ra.txt",65, 66, 17219, 17476, 16, 70)
	print(como.recive("new", "5ra.txt"))
