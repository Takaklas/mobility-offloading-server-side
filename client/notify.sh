#! /bin/bash
# just for testing
Log=/var/log/dnsmasqscript.log
date > $Log
echo "Param1 = $1" >> $Log
echo "Param2 = $2" >> $Log
echo "Param3 = $3" >> $Log
echo "Param4 = $4" >> $Log
#

ACTION=$1
MAC=$2
IP=$3
HOSTNAME=$4

if [ "$ACTION" = 'add' ] || [ "$ACTION" = 'old' ]; then
	#curl -d "mac=$2&ip=$3" http://0.0.0.0:8000/back/notify
	curl "http://0.0.0.0:8000/back/notify?mac=$2&ip=$3"
	notify-send $HOSTNAME $IP
fi
