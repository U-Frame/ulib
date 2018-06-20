import USB

import USB
import sys
import time
from bitarray import bitarray


def callback(Data):
	if Data == None :
		print("None")
	else:
		data = bytearray(Data)
		print(Data)
		for record in data:
			print("data: " + str(record))
		print("eof")


#usb = USB.USB("0e8f", "00fb", "0")
usb = USB.USB("16c0", "03e8", "0")
temp = bytearray("                ")
#control test

#turn on led
usb.writeControl(1,0xc0,0,0,16,temp)
time.sleep(2)

#turn off led
usb.writeControl(0,0xc0,0,0,16,temp)
time.sleep(1)


#write data in value and index
usb.writeControl(3, 0xc0, ord("e") + (ord("t")<<8), ord("t") + (ord("s")<<8), 16)

#read data
print(usb.readControl(2,0xC0,0,0,16,temp))

#write new data
data = bytearray("wla wla         ")
#data = "wlaaaa   "
#usb.writeControl(4,0x40,0,0,16,data)
usb.writeControl(4,0xc0,0,0,16,data)
		
#read data
print(usb.readControl(2,0xC0,0,0,16,temp))


#thread = usb.readInterruptHandler(11, None,callback)
#thread = usb.readInterruptHandler(21, None,callback)
#usb.writeBulk(11, 8, "walaaaaa")
#print(usb.readBulk(11))


