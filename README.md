# mobility-offloading-server-side

A Django implemetation of an image recognition server at the edge interconnected with other servers, with the ability to detect mobility of users to other sevrers on the same network of edge servers. Used for experiments in mobility computational offloading.

Back service keeps track of users, detecting new users and informing the other servers about newcomers.

Front service serves as the image recognition server, accepting images and returning detection results to the user.

Tested using scripts in client folder in mininet and on the lab infrastructure. Requires access points with dnsmasq as the dhcp server and accessible arp table.
