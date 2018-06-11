import Communication
import threading
import time


# 00 -> control endpoint
# 01 -> bulk endpoint
# 02 -> interrupt endpoint
# 03 -> ISOCHRONOUS endpoint


CONTROL = "00"
BULK = "01"
INTERRUPT = "02"
ISOCHRONOUS = "03"


# 00 -> control (SETUP) endpoint
# 01 -> IN endpoint
# 02 -> OUT endpoint


SETUP = "00"
IN1 = "101"
IN2 = "102"
IN3 = "103"
IN4 = "104"
IN5 = "105"
IN6 = "106"
IN7 = "107"
IN8 = "108"
IN9 = "109"
IN10 = "110"
IN11 = "111"
IN12 = "112"
IN13 = "113"
IN14 = "114"
IN15 = "115"
IN16 = "116"

OUT1 = "201"
OUT2 = "202"
OUT3 = "203"
OUT4 = "204"
OUT5 = "205"
OUT6 = "206"
OUT7 = "207"
OUT8 = "208"
OUT9 = "209"
OUT10 = "210"
OUT11 = "211"
OUT12 = "212"
OUT13 = "213"
OUT14 = "214"
OUT15 = "215"
OUT16 = "216"


IOCTL_INTERRUPT_INTERVAL = 0
IOCTL_INTERRUPT_STEP = 1


class USB:
	def __init__(self, VID, PID, interface):
		self.VID = VID
		self.PID = PID
		self.interface = interface
		self.comm = Communication.communication()
		self.interruptInterval = self.comm.ioctl(self.VID, self.PID, self.interface, IOCTL_INTERRUPT_INTERVAL)
		self.interruptStep = self.comm.ioctl(self.VID, self.PID, self.interface, IOCTL_INTERRUPT_STEP)


	def writeInterrupt(self, data, OUTn):
	    	self.comm.sendData(self.VID, self.PID, self.interface, INTERRUPT, OUTn, 16, data)


	def writeInterruptHandler(self, OUTn, interval = None, step = None, callBackFunction = None):
		if interval == None:
			interval = self.interruptInterval
		
		if step == None:
			step = self.interruptStep

		threading.Thread(target = self.readInterruptCaller, args = (OUTn, interval, step, callBackFunction,)).start()


	def writeInterruptCaller(self, OUTn, interval, step, callBackFunction = None):
		for i in range(1, interval, step):
			data = self.readInterrupt(OUTn)
			callBackFunction(data)
			time.sleep(step/1000)


	def readInterrupt(self, INn):
	    	data = self.comm.recive(self.VID, self.PID, self.interface, INTERRUPT, INn)
	    	return data

	
	def readInterruptHandler(self, INn, interval = None, step = None, callBackFunction = None):
		if interval == None:
			interval = self.interruptInterval
		
		if step == None:
			step = self.interruptStep

		threading.Thread(target = self.readInterruptCaller, args = (INn, interval, step, callBackFunction,)).start()


	def readInterruptCaller(self, INn, interval, step, callBackFunction = None):
		for i in range(1, interval, step):
			data = self.readInterrupt(INn)
			callBackFunction(data)
			time.sleep(step/1000)


	def writeBulk(self, OUTn, data):
	    	self.comm.sendData(self.VID, self.PID, self.interface, BULK, OUTn, 16, data)


	def readBulk(self, INn):
	    	data = self.comm.recive(self.VID, self.PID, self.interface, BULK, INn)
	    	return data


	def writeControl(self, request, requestType, value, index, size, data):
		self.comm.sendWord(self.VID, self.PID, self.interface, SETUP, request, requestType, value, index, size)
		self.comm.sendData(self.VID, self.PID, self.interface, size, data)


def callback1(data):
	print(data)


def callback2(data):
	print("1")


if __name__ == "__main__":
	usb = USB("10", "10", "15")
	usb.writeBulk(OUT1, 65)
	print(usb.readBulk(IN1))
	usb.readInterruptHandler(IN1, 2000, 1000, callback1)
	usb.readInterruptHandler(IN1, 3000, 1000, callback2)
