#!/bin/bash

python3 manage.py migrate

#python3 manage.py lease_read &

#iperf3 -s -p 5202 -J --logfile ./log1.txt &
#python3 -u ./manage.py runserver 0.0.0.0:8000
python3 manage.py runserver 0.0.0.0:8000  

pkill -9 python3


