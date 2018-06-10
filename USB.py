import Communication


#00 -> control (SETUP) endpoint
#01 -> IN endpoint
#02 -> OUT endpoint


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
		self.comm.send(self.VID, self.PID, self.interface, OUT, "", "", "", "", "", data)

	def readInterrupt(self):
		data = self.comm.recive(self.VID, self.PID, self.interface, IN);
		return data

	def writeBulk(self, data):
		self.comm.send(self.VID, self.PID, self.interface, OUT, 65, 66, 17219, 17476, 8, data)

	def readBulk(self):
		data = self.comm.recive(self.VID, self.PID, self.interface, IN);
		return data		

	def writeControl(self, request, requestType, value, index, size, data):
		self.comm.send(self.VID, self.PID, self.interface, SETUP, request, requestType, value, index, size, data)

if __name__ == "__main__":
	usb = USB("10", "10", "15")
	usb.writeBulk(65)
	print(usb.readBulk())
