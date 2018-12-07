import requests
import subprocess
import client_server3
import socket
import threading
import time
import random
import os
import datetime
from sys import version as python_version

if python_version.startswith('3'):
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def get_ip():
    return socket.gethostbyname(socket.gethostname())
    return subprocess.check_output(['hostname','-I']).split()

def ping_server(ip):
    #output = subprocess.check_output('ping -c %s -W %s -t %s 8.8.8.8' % (self.numPings, (self.pingTimeout * 1000), self.maxWaitTime), shell=True)
    output = subprocess.check_output(['ping', '-c', '1', ip]).decode('utf-8')

    output = output.split('\n')[-3:]
    # -1 is a blank line, -3 & -2 contain the actual results

    xmit_stats = output[0].split(",")
    timing_stats = output[1].split("=")[1].split("/")

    packet_loss = float(xmit_stats[2].split("%")[0])

    ping_min = float(timing_stats[0])
    ping_avg = float(timing_stats[1])
    ping_max = float(timing_stats[2])
    print(packet_loss,ping_min,ping_avg,ping_max)

def start_threaded_server():
    t = threading.Thread(target=client_server3.run_forever)
    # We want the program to wait on this thread before shutting down.
    t.deamon = False
    t.start()

def threaded_server():
    server_class=HTTPServer 
    handler_class=client_server3.GP
    port=8088
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server running at localhost:8088...')
    t = threading.Thread(target=httpd.serve_forever)
    t.deamon = False
    t.start()
    return httpd

def send_multiply_request(server_ip,num1,num2):
    url = "http://" + server_ip +":8000/front/request"
    #r = requests.get(url, params = {'num1':str(i), 'num2':'7'}, timeout=1)
    #subprocess.check_call(["curl", url+"?num1=5&num2=7"])

    r = requests.post(url, data = {'num1':str(num1), 'num2':str(num2)}, timeout=1)
    #subprocess.check_call(["curl", "-d", '"?num1=5&num2=7"', url])
    return r

def send_image_request(server_ip,image):
    img = image + ".jpg"
    post_url = "http://" + server_ip +":8000/front/imageUpload"
    size = os.path.getsize("../images/" + img)
    pts = datetime.datetime.now().strftime('%s')
    json = {"size": size, "start_time": pts}
    files = {"file": open("../images/" + img, "rb")}
    try:
        r = requests.post(post_url, files=files, data=json,timeout=10)
    except requests.exceptions.ConnectionError:
        print("Could not upload image {} to server {}".format(image,server_ip))
        return
    return r

images = ['n','n1','n2','n3','y1','y2','y3','y4','y5','y6','y7','y8','y9']
if __name__ == "__main__":
    #client_server3.run_forever()
    #start_threaded_server()
    httpd = threaded_server()
    for i in range(6):
        start = time.time()
        ip = get_ip()
        split_ip = ip.split('.')
        server_ip = split_ip[0] + '.' + split_ip[1] + '.' + split_ip[2] + '.1'
        server_ip = '192.168.1.1' # '11.0.0.1' 
        # r = send_multiply_request(server_ip,i,7)
        r = send_image_request(server_ip,random.choice(images))
        # r.raise_for_status()

        #client_server3.run()
        print("Request sent to server, took {} seconds".format(time.time()-start) )
    try:
        wait = input("All activities done.Press any key...")
    except KeyboardInterrupt:
        pass
    httpd.shutdown()
