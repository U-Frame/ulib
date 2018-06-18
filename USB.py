import Communication
import StoppableThread
import threading
import time


# 00 -> control endpoint
# 01 -> bulk endpoint
# 02 -> interrupt endpoint
# 03 -> ISOCHRONOUS endpoint


CONTROL = 0
BULK = 1
INTERRUPT = 2
ISOCHRONOUS = 3


# 00 -> control (SETUP) endpoint
# 01 -> IN endpoint
# 02 -> OUT endpoint


IN0 = 001
IN1 = 101
IN2 = 102
IN3 = 103
IN4 = 104
IN5 = 105
IN6 = 106
IN7 = 107
IN8 = 108
IN9 = 109
IN10 = 110
IN11 = 111
IN12 = 112
IN13 = 113
IN14 = 114
IN15 = 115
IN16 = 116

OUT0 = 0
OUT1 = 1
OUT2 = 2
OUT3 = 3
OUT4 = 4
OUT5 = 5
OUT6 = 6
OUT7 = 7
OUT8 = 8
OUT9 = 9
OUT10 = 10
OUT11 = 11
OUT12 = 12
OUT13 = 13
OUT14 = 14
OUT15 = 15
OUT16 = 16


IOCTL_INTERRUPT_INTERVAL = 0


class USB:
	def __init__(self, vid, pid, interface):
		self.vid = vid
		self.pid = pid
		self.interface = interface
		self.comm = Communication.communication(vid, pid, interface)
		#self.interruptInterval = self.comm.ioctl(vid, pid, interface, 0, 0, 0, 0, 0, 0, IN0, IOCTL_INTERRUPT_INTERVAL)
		self.interruptInterval = 1000

	def writeInterruptHandler(self, OUTn, interval = None, callBackFunction = None):
		if interval == None:
			interval = self.interruptInterval
		thread = threading.Thread(target = self.writeInterruptCaller, args = (INn, interval, callBackFunction,))
		thread.start()
		return thread
		
		
	def writeInterruptCaller(self, OUTn, interval, callBackFunction = None):
		while True :
			data = self.writeInterrupt(OUTn)
			callBackFunction(data)
			time.sleep(interval/1000)


	def writeInterrupt(self, size, data, OUTn):
	    	self.comm.sendData(INTERRUPT, OUTn, size, data)


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
			time.sleep(interval/1000.0)


	def readInterrupt(self, INn):
	    	#data = self.comm.recive(INTERRUPT, INn)
	    	data = self.comm.recive(1, 0)
	    	return data

	
	def writeBulk(self, OUTn, size, data):
	    	self.comm.sendData(BULK, OUTn, size, data)


	def readBulk(self, INn):
	    	data = self.comm.recive(BULK, INn)
	    	return data


	def writeControl(self, request, requestType, value, index, size, data = None):
		self.comm.send(CONTROL, 1, request, requestType, value, index, size, data)
		
	def readControl(self, request, requestType, value, index, size, data):
		return self.comm.recive(CONTROL, 0, request, requestType, value, index, size, data)
	
	
def callback1(data):
	print("2")


def callback2(data):
	print("1")


if __name__ == "__main__":
	usb = USB(10, 10, 15)
	usb.writeBulk(OUT15, 8, 65)
	print(usb.readBulk(IN1))
	thread1 = usb.readInterruptHandler(IN1, callBackFunction = callback1)
	thread2 = usb.readInterruptHandler(IN1, callBackFunction = callback2)

	time.sleep(2)
