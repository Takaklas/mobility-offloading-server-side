#!/bin/bash

# sudo mn --mac --arp -x --topo single,3 # --nat --test pingall
# sudo mn --mac -x --custom triangle.py --topo really_last_hope # --nat --test pingall
# sudo mn --mac -x --custom triangle.py --topo last_hope # --arp --nat --test pingall
sudo mn --mac --arp --custom triangle.py --topo proper_triangle # -x --nat --test pingall
# sudo mn --mac --arp -x --custom triangle.py --topo square # --nat --test pingall
# sudo mn --mac --arp -x --custom triangle.py --topo triangle --nat --test pingall
