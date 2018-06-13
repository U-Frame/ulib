import Communication
import StoppableThread
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
IN1 = Communication.IN + "01"
IN2 = Communication.IN + "02"
IN3 = Communication.IN + "03"
IN4 = Communication.IN + "04"
IN5 = Communication.IN + "05"
IN6 = Communication.IN + "06"
IN7 = Communication.IN + "07"
IN8 = Communication.IN + "08"
IN9 = Communication.IN + "09"
IN10 = Communication.IN + "10"
IN11 = Communication.IN + "11"
IN12 = Communication.IN + "12"
IN13 = Communication.IN + "13"
IN14 = Communication.IN + "14"
IN15 = Communication.IN + "15"
IN16 = Communication.IN +"16"

OUT1 = Communication.OUT + "01"
OUT2 = Communication.OUT + "02"
OUT3 = Communication.OUT + "03"
OUT4 = Communication.OUT + "04"
OUT5 = Communication.OUT + "05"
OUT6 = Communication.OUT + "06"
OUT7 = Communication.OUT + "07"
OUT8 = Communication.OUT + "08"
OUT9 = Communication.OUT + "09"
OUT10 = Communication.OUT + "10"
OUT11 = Communication.OUT + "11"
OUT12 = Communication.OUT + "12"
OUT13 = Communication.OUT + "13"
OUT14 = Communication.OUT + "14"
OUT15 = Communication.OUT + "15"
OUT16 = Communication.OUT + "16"


IOCTL_INTERRUPT_INTERVAL = 0


class USB:
	def __init__(self, VID, PID, interface):
		self.VID = VID
		self.PID = PID
		self.interface = interface
		self.comm = Communication.communication()
		self.interruptInterval = self.comm.ioctl(self.VID, self.PID, self.interface, 0, 0, 0, 0, 0, 0, 0, IOCTL_INTERRUPT_INTERVAL)

	def writeInterrupt(self, data, OUTn):
	    	self.comm.sendData(self.VID, self.PID, self.interface, INTERRUPT, OUTn, 16, data)


	def writeInterruptHandler(self, OUTn, interval = None, callBackFunction = None):
		if interval == None:
			interval = self.interruptInterval

		thread = threading.Thread(target = self.readInterruptCaller, args = (INn, interval, callBackFunction,))
		thread.start()
		return thread


	def writeInterruptCaller(self, OUTn, interval, callBackFunction = None):
		while True :
			data = self.readInterrupt(OUTn)
			callBackFunction(data)
			time.sleep(interval/1000)


	def readInterrupt(self, INn):
	    	data = self.comm.recive(self.VID, self.PID, self.interface, INTERRUPT, INn)
	    	return data

	
	def readInterruptHandler(self, INn, interval = None, callBackFunction = None):
		if interval == None:
			interval = self.interruptInterval
		thread = threading.Thread(target = self.readInterruptCaller, args = (INn, interval, callBackFunction,))
		thread.start()
		return thread


	def readInterruptCaller(self, INn, interval, callBackFunction = None):
		while True :
			data = self.readInterrupt(INn)
			callBackFunction(data)
			time.sleep(interval/1000)


	def writeBulk(self, OUTn, data):
	    	self.comm.sendData(self.VID, self.PID, self.interface, BULK, OUTn, 16, data)


	def readBulk(self, INn):
	    	data = self.comm.recive(self.VID, self.PID, self.interface, BULK, INn)
	    	return data


	def writeControl(self, request, requestType, value, index, size, data):
		self.comm.sendWord(self.VID, self.PID, self.interface, SETUP, request, requestType, value, index, size)
		self.comm.sendData(self.VID, self.PID, self.interface, size, data)


def callback1(data):
	print("2")


def callback2(data):
	print("1")


if __name__ == "__main__":
	usb = USB("10", "10", "15")
	usb.writeBulk(OUT15, 65)
	print(usb.readBulk(IN1))
	thread1 = usb.readInterruptHandler(IN1, 10000, callback1)
	thread2 = usb.readInterruptHandler(IN1, 10000, callback2)

	time.sleep(2)
