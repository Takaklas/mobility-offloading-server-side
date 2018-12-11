#!/bin/bash

sudo cp notify.sh /bin
sudo echo "dhcp-script = /bin/notify.sh" >> /etc/dnsmasq.more.conf
