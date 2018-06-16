#!/bin/bash

if [ $1 == "help" ]
then
	echo "usage: manage.sh make driver"
	echo "Runs make command on the driver files."
	echo ""
	echo "usage: manage.sh load driver"
	echo "usage: manage.sh create directory #pid #vid #interface"
	echo ""
	echo "Creates a directory to a specific interface."
	echo ""
	echo "usage: manage.sh default #vid #pid #interface"
	echo "Runs make on driver files then loads the driver and creates a directory for the given vid, pid and interface an finally creates an interface by a default of 1 endpoint of each type."
	echo "" 
	echo "usage: manage.sh create node #vid #pid #interface #nodetype #direction"
	echo "00 -> control"
	echo "01 -> bulk"
	echo "02 -> interrupt"
	echo "03 -> isochronous"
	echo "000-> OUT"
	echo "001-> IN"
	echo "To create a node, the two most significant digits denote to the number and the least significant digit denotes to the direction."
	echo "ex: 010 means node number 2 and its direction is OUT."
	echo ""
elif [ $1 == "make" ] && [ $2 == "driver" ]
then
	make

elif [ $1 == "load" ] && [ $2 == "driver" ]
then
	echo "inserting the driver..."
	sudo insmod udriver.ko

elif [ $1 == "create" ] && [ $2 == "directory" ]
then
	if (( $# < 5 ))
	then
		echo "Error: Arguments missing."
	else
		#specifying the vid,pid and interface
		vid=$3
		pid=$4
		interface=$5
		dir="/home/samir/Documents/dev/fframe/"$vid"/"$pid"/"$interface"/"
		echo "creating directory: ""/home/samir/Documents/dev/fframe/"$vid"/"$pid"/"$interface"/"
		#making a directory for the interface
		mkdir -p $dir
	fi
elif [ $1 == "default" ]
then 
	if (( $# < 4 ))
	then
		echo "Error: Arguments missing."
	else
		make
		vid=$2
		pid=$3
		interface=$4

		mode="666"
		module="uframe"
		
		dir="/home/samir/Documents/dev/fframe/"$vid"/"$pid"/"$interface"/"

		echo "inserting the driver..."
		sudo insmod udriver.ko
		#/sbin/insmod ./udriver.ko $* || exit 1
		
		echo "creating directory: ""/home/samir/Documents/dev/fframe/"$vid"/"$pid"/"$interface"/"
		mkdir -p $dir

		echo "creating nodes (endpoints)..."
		echo "00 -> control"
		echo "01 -> bulk"
		echo "02 -> interrupt"
		echo "03 -> isochronous"
		echo "000-> OUT"
		echo "001-> IN"
		echo ""

		major=`awk "\\$2==\"$module\" {print \\$1}" /proc/devices`

		group="staff"
		grep -q '^staff:' /etc/group || group="wheel"

		for type in {0..3}
		do
			mkdir -p "$dir"0"$type"
			for direction in {0..1}
			do
				echo "$dir""0$type""/""00$direction" c $major $type 
				sudo mknod "$dir""0$type""/""00$direction" c $major $type
				sudo chgrp $group "$dir""0$type""/""00$direction"
				sudo chmod $mode "$dir""0$type""/""00$direction"
			done
		done
	fi

elif [ $1 == "create" ] && [ $2 == "node" ]
then
	if (( $# < 7 ))
	then
		echo "Error: Arguments missing."
	else
		#specifying the vid,pid and interface
		vid=$3
		pid=$4
		interface=$5
		type=$6
		direction=$7

		mode="666"
		module="uframe"
		
		dir="/home/samir/Documents/dev/fframe/"$vid"/"$pid"/"$interface"/"$type"/"

		major=`awk "\\$2==\"$module\" {print \\$1}" /proc/devices`

		group="staff"
		grep -q '^staff:' /etc/group || group="wheel"

		nodeDir="$dir""$direction"

		mkdir -p "$dir"

		if [ $type == "00" ]
		then 
			minor="0"
		elif [ $type == "01" ]
		then
			minor="1"
		elif [ $type == "02" ]
		then
			minor="2"
		elif [ $type == "03" ]
		then
			minor="3"
		fi

		echo "$nodeDir c $major $minor"
		sudo mknod $nodeDir c $major $minor
		sudo chgrp $group $nodeDir
		sudo chmod $mode $nodeDir
	fi

fi
