import fcntl
from bitarray import bitarray
from sys import getsizeof


class communication :

    def __init__(self, vid, pid):
	self.vid = vid
	self.pid = pid

    def recive(self):
        file = open(self.vid+"/"+self.pid, "r")
	data = bitarray()
	data.frombytes( file.read())
	file.close()
        return data

    def send(self, request, requestType, value, index, size, data):
	#print ("{0:0b}".format(data))
	messege = bitarray( "{0:08b}".format(request) + "{0:08b}".format(requestType) + "{0:016b}".format(value) + "{0:016b}".format(index) + "{0:016b}".format(size) + "{0:0b}".format(data) )
	#8 request - 8 requesttype- 16 value - 16 index - 16 size+ Data
        file = open(self.vid+"/"+self.pid, "a")
        file.write(messege.tobytes())
	file.close()

    def ioctl(self, operation):
        file = open(self.vid+"/"+self.pid, "r+")
        fcntl.ioctl(file, operation)
	file.close()

if __name__ == "__main__":
	como = communication("new", "new.txt")
	a = bitarray('01000010')
	como.send(65, 66, 17219, 17476, 17733, 70)
	print(como.recive())
