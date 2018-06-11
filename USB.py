import Communication

# os lib
# print(os.path.isdir("/home/el"))
# print(os.path.exists("/home/el/myfile.txt"))

# 00 -> control endpoint
# 01 -> bulk endpoint
# 02 -> interrupt endpoint
# 03 -> ISOCHRONOUS endpoint

CONTROL = "00"
BULK = "01"
INTERRUPT = "03"
ISOCHRONOUS = "04"

# 00 -> control (SETUP) endpoint
# 01 -> IN endpoint
# 02 -> OUT endpoint

SETUP = "00"
IN = "01"
OUT = "02"


class USB:
	def __init__(self, VID, PID, interface):
		self.VID = VID
		self.PID = PID
		self.interface = interface
		self.comm = Communication.communication()


	def writeInterrupt(self, data):
	    	self.comm.sendData(self.VID, self.PID, self.interface, INTERRUPT, OUT, 16, data)


	def readInterrupt(self):
	    	data = self.comm.recive(self.VID, self.PID, self.interface, INTERRUPT, IN)
	    	return data


	def writeBulk(self, data):
	    	self.comm.sendData(self.VID, self.PID, self.interface, BULK, OUT, 16, data)


	def readBulk(self):
	    	data = self.comm.recive(self.VID, self.PID, self.interface, BULK, IN)
	    	return data


	def writeControl(self, request, requestType, value, index, size, data):
		self.comm.sendWord(self.VID, self.PID, self.interface, SETUP, request, requestType, value, index, size)
		self.comm.sendData(self.VID, self.PID, self.interface, size, data)


if __name__ == "__main__":
	usb = USB("10", "10", "15")
	usb.writeBulk(65)
	print(usb.readBulk())
