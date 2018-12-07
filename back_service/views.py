from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from back_service.models import Client_ip_mac

from multiprocessing.dummy import Pool as ThreadPool 
import threading
import requests
import subprocess
import socket

def get_sender_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_server_ip():
    return socket.gethostbyname(socket.gethostname())
    return subprocess.check_output(['hostname','-I']).split()

def get_ip_from_mac(mac):
    with open('/proc/net/arp') as arpt:
        # first line is junk
        # [IP address, HW type, Flags, HW address, Mask, Device]
        lines = arpt.readlines()[1:]
        for line in lines:
            line = line.split()
            if line[3]==mac:
                return line[0]

def request_server(request):
    if request.method == 'GET':
        mac = request.GET['mac']
        result = request.GET['result']
    if request.method == 'POST':
        mac = request.POST['mac']
        result = request.POST['result']
    sender_ip = get_sender_ip(request)
    client_ip = get_ip_from_mac(mac)
    if client_ip == None: 
        print("Client is not connected to this server")
        return HttpResponse(status=404)
    url = "http://" + client_ip + ":8088"
    mul = result
    try:
        print("Responding to ip {} who came from {}".format(client_ip, sender_ip))
        # r = requests.get(url, params = {'result':mul}, timeout=1)
        r = requests.post(url, data = {'result':mul}, timeout=1)
        print("Response successful!")
        return HttpResponse(status=200)
    except requests.exceptions.ConnectionError:
        print("Client is not connected to this server")
        return HttpResponse(status=404)

class requests_wrapper:
    def __init__(self, params={}, timeout=1):
        self.params = params
        self.data = params
        self.timeout = timeout
    def get(self,url):  
        try:
            r = requests.get(url, params = self.params, timeout = self.timeout) 
        except requests.exceptions.ConnectionError:
            return 404
        return r.status_code
    def post(self,url):
        try:
            r = requests.post(url, data = self.data, timeout = self.timeout)  
        except requests.exceptions.ConnectionError:
            return 404
        return r.status_code

def notify_other_servers(mac,ip):
    server_ips = ['10.0.0.1','10.0.0.2']
    this_server_ip = get_server_ip()
    urls = ["http://" + ip + ":8000/back/notify" for ip in server_ips if ip!=this_server_ip]
    specific_request = requests_wrapper(params = {'mac':mac, 'ip':ip}, timeout=10)
    with ThreadPool(processes=len(urls)) as pool: 
        # open the urls in their own threads
        # and return the results
        results = pool.map(specific_request.get, urls)
    for server,result in zip(server_ips,results):
        if result!=200:
            print("Server with ip %s did not get notified!" % server)

def notify_connection(request):
    if request.method == 'GET':
        client_mac = request.GET['mac']
        client_ip = request.GET['ip']
    if request.method == 'POST':
        client_mac = request.POST['mac']
        client_ip = request.POST['ip']
    sender_ip = get_sender_ip(request)
    print("New client connected, coming from ip %s" % sender_ip)
    if sender_ip == "127.0.0.1":
        is_local=True
        notify_other_servers(client_mac,client_ip)
        #t = threading.Thread(target=notify_other_servers, args=(client_mac,client_ip,))
        # We want the program to wait on this thread before shutting down.
        #t.deamon = False
        #t.start()
    else:
        is_local=False
        client_ip = sender_ip
    print("Mac: {}, IP: {}, Local: {}\n".format(client_mac,client_ip,is_local))
    client = Client_ip_mac(client_mac = client_mac, client_ip = client_ip, is_local = is_local)
    client.save()
    #current_client = Client_ip_mac.objects.get(client_mac = client_mac)
    #print("Mac: {}, IP: {}".format(current_client.client_mac,current_client.client_ip))
  
    return HttpResponse(status=200)  
