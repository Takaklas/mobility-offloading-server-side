import time
import random
import subprocess
import datetime
import sys
import requests
import os
import pprint
import client_server3

img = 'y5.jpg'
#img = 'capture.jpg'
#post_url = "http://0.0.0.0:8002/ca_tf/imageUpload/" + img
post_url = "http://11.0.0.1:8000/front/imageUpload"
#post_url = "http://0.0.0.0:8000/front/imageUpload"
#post_url = "http://10.0.0.4:8002/ca_tf/imageUpload/" + img
post_url = "http://0.0.0.0:8000/ca_tf/imageUpload/" + img
size = os.path.getsize("../images/" + img)
pts = datetime.datetime.now().strftime('%s')
json = {"size": size, "start_time": pts}
files = {"file": open("../images/" + img, "rb")}
r = requests.post(post_url, files=files, data=json,timeout=10)
pprint.pprint(r.headers)
print r
print r.text
print r.url
print r.status_code
print r.history
print r.cookies
r.raise_for_status()
client_server3.run()
#print r.json()
