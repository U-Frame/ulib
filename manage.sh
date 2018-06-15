#!/bin/bash


echo $#
if (( $# < 3 ))
then
	echo "Error: parameter missing"
	echo "usage: manage.sh pid vid interface"

else
	#specifying the vid,pid and interface
	vid=$1
	pid=$2
	interface=$3

	mode="666"
	module="uframe"
	dir="/home/samir/Documents/dev/fframe/"$vid"/"$pid"/"$interface"/"

	#inserting the driver
	insmod udriver.ko
	#/sbin/insmod ./udriver.ko $* || exit 1

	#making a directory for the interface
	mkdir -p $dir

	#creating nodes (endpoints)
	major=`awk "\\$2==\"$module\" {print \\$1}" /proc/devices`

	group="staff"
	grep -q '^staff:' /etc/group || group="wheel"

	for number in {0..3}
	do
		mkdir -p "$dir"0"$number"
		for num in {0..1}
		do
			echo "$dir""0$number""/""00$num" c $major $number 
			mknod "$dir""0$number""/""00$num" c $major $number 
			chgrp $group "$dir""0$number""/""00$num"
			chmod $mode "$dir""0$number""/""00$num"
		done
	done
fi
