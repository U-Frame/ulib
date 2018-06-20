import os
import sys


VID = sys.argv[1]
PID = sys.argv[2]

file = open('uframe.h', 'r')
data = file.readlines()
file.close()
data[5] = '#define VID 0x' + VID + '\n'
data[6] = '#define PID 0x' + PID + '\n'
file = open('uframe.h', 'w')
file.write("".join(data))
file.close()

os.system("make")
os.system("sudo rmmod udriver.ko")
os.system("sudo insmod udriver.ko")

interface = 0
os.system("lsusb > lsusb.txt")
file = open('lsusb.txt', 'r')
data = file.readlines()
file.close()
os.system("rm lsusb.txt")
target = "ID " + VID + ":" + PID

deviceDetails = ""
for line in data:
	if target in line:
		deviceDetails = line
		break

if deviceDetails != "":
	bus = deviceDetails[4:7]
	device = deviceDetails[15:18]

	print("bus: " + bus)
	print("device: " + device)
	
	os.system("lsusb -D /dev/bus/usb/" + bus + "/" + device + " > deviceDiscriptor.txt")
	
	file = open("deviceDiscriptor.txt", "r")
	data = file.readlines()
	file.close()
	#os.system("rm deviceDiscriptor.txt")

	target = "Endpoint Descriptor:"
	ep = open("endpoints.txt", "w")
	ep.write(target + "\n")
	deviceDetails = ""
	counter = 0
	for line in data:
		if target in line:
			
			for i in range(counter + 1, len(data)-1) :
				ep.write(data[i])
			ep.close()
			break
		counter += 1

	
	endpointCounter = 0 
	type = ""
	direction = ""
	#creating control endpoint
	os.system("bash create_node.sh " + " " + VID + " " + PID + " " + str(interface) + " " + "Control" + " " + "{0:03}".format(0) + " " + str(endpointCounter))

	target = "Endpoint Descriptor"
	ep = open("endpoints.txt", "r")
	data = ep.readlines()
	counter = 0
	interruptOUTCounter = 0
	interruptINCounter = 0
	bulkOUTCounter = 0
	bulkINCounter = 0
	isochronousOUTCounter = 0
	isochronousINCounter = 0
	for line in data:
		if target in line:
			type = ""
			direction = ""
			for i in range(counter + 1, len(data)-1) :
				if "bEndpointAddress" in data[i]:
					#endpointCounter += 1
					if "IN" in data[i]:
						dir = 1
					else:
						dir = 0
				if "Transfer Type" in data[i]:
					if "Interrupt" in data[i]:
						type = "Interrupt"
						if dir == "OUT":
							interruptOUTCounter += 1
							endpointCounter = interruptOUTCounter
						else:
							interruptINCounter += 1
							endpointCounter = interruptINCounter
							print("IN")
					elif "Bulk" in data[i]:
						type = "Bulk"
						if dir == "OUT":
							bulkOUTCounter += 1
							endpointCounter = bulkOUTCounter
						else:
							bulkINCounter += 1
							endpointCounter = bulkINCounter
					elif "Isochronous" in data[i]:
						type = "Isochronous"
						if dir == "OUT":
							iscochronousOUTCounter += 1
							endpointCounter = iscochronousOUTCounter
						else:
							iscochronousINCounter += 1
							endpointCounter = iscochronousINCounter

					direction = "{0:03}".format(dir + endpointCounter*10)

				
				if type != "" and direction != "":
					os.system("bash create_node.sh " + " " + VID + " " + PID + " " + str(interface) + " " + type + " " + direction + " " + str(endpointCounter))
					break
		counter += 1


else :
	print ("device is not connected")




