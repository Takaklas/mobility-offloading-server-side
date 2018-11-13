from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

import threading
from multiprocessing.dummy import Pool as ThreadPool 
import requests
import time

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_mac_from_ip(ip):
    with open('/proc/net/arp') as arpt:
        # first line is junk
        # [IP address, HW type, Flags, HW address, Mask, Device]
        lines = arpt.readlines()[1:]
        for line in lines:
            line = line.split()
            if line[0]==ip:
                return line[3]

class requests_wrapper:
    def __init__(self, params={}, timeout=1):
        self.params = params
        self.data = params
        self.timeout = timeout
    def get(self,url):  
        r = requests.get(url, params = self.params, timeout = self.timeout) 
        return r.status_code
    def post(self,url):
        r = requests.post(url, data = self.data, timeout = self.timeout)  
        return r.status_code    

def send_response_concurrent_search(mul,ip,mac):
    url = "http://" + ip + ":8088"
    try:
        print("Responding:")
        # r = requests.get(url, params = {'result':mul}, timeout=1)
        # raise requests.exceptions.ConnectionError
        r = requests.post(url, data = {'result':mul}, timeout=1)
        print("Response sucessful!")
    except requests.exceptions.ConnectionError:
        print("Oh shit...must find that mofo")
        Found = False
        server_ips = ['10.0.0.1','10.0.0.2']
        urls = ["http://" + ip + ":8000/back/request" for ip in server_ips]
        client_sequential_search = False
        specific_request = requests_wrapper(params = {'result':mul, 'mac':mac}, timeout=100)
        while not Found:
            if client_sequential_search:
                for ip, url in zip(server_ips, urls): 
                    result = specific_request.get(url)                     
                    # r = specific_request.post(url)
                    if result == 200:
                        print('mofo found at {}!'.format(ip))
                        Found = True
                        break
            else:
                # make the Pool of workers
                with ThreadPool(processes=len(urls)) as pool: 
                    # open the urls in their own threads
                    # and return the results
                    results = pool.map(specific_request.get, urls)
                for server_ip, result in zip(server_ips,results):
                    if result == 200:
                        print('mofo found at {}!'.format(server_ip))
                        Found = True
                        break

def task(num1,num2,ip,mac):
    time.sleep(5)
    mul = int(num1)*int(num2)
    send_response_concurrent_search(mul,ip,mac)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def request_server(request):
    ip = get_client_ip(request)
    mac = get_mac_from_ip(ip)
    print("IP: {}, MAC: {}".format(ip,mac))
    if request.method == 'GET':
        number1 = request.GET['num1']
        number2 = request.GET['num2']
    if request.method == 'POST':
        number1 = request.POST['num1']
        number2 = request.POST['num2']
    t = threading.Thread(target=task, args=(number1,number2,ip,mac,))
    # We want the program to wait on this thread before shutting down.
    t.deamon = False
    t.start()
    #time.sleep(5)
    return HttpResponse(status=202)

