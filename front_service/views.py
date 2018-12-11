from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from back_service.models import Client_ip_mac
import configuration

import threading
from multiprocessing.dummy import Pool as ThreadPool 
import requests
import time
import os
from front_service.tasks import classify

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

def gen_password( temp=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"):
        random_bytes = os.urandom(8)
        len_charset = len(charset)
        indices = [int(len_charset * (byte / 256.0)) for byte in random_bytes]
        return "".join([charset[index] for index in indices])

def handle_uploaded_file(src_img):
    dirr = os.getcwd()
    filename = os.path.join(dirr, '')
    dest_img = filename + gen_password() + src_img.name

    with open(dest_img, 'wb+') as dest:
        for c in src_img.chunks():
            dest.write(c)
    return dest_img

def delete_uploaded_file(image):
    if os.path.isfile(image):
        os.remove(image)
    else:
        print("Error: temp file not found")

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
        print("Responding to {}".format(mac))
        # r = requests.get(url, params = {'result':mul}, timeout=1)
        # raise requests.exceptions.ConnectionError
        r = requests.post(url, data = {'result':mul}, timeout=1)
        print("Response to {} successful!".format(mac))
    except requests.exceptions.ConnectionError:
        print("Client moved to another server!Searching...")
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
                        print('Client found at {}!'.format(ip))
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
                        print('Client found at {}!'.format(server_ip))
                        Found = True
                        break

def send_response_read_from_db(data,mac):
    if mac==None: return requests.post("http://127.0.0.1:8088", data=data, timeout=1)
    current_client = Client_ip_mac.objects.get(client_mac = mac)
    client_ip = current_client.client_ip
    is_local = current_client.is_local
    print("Responding to  IP: {}, Mac: {}".format(client_ip,mac))
    if is_local:
        url = "http://" + client_ip + ":8088"    
        try:
            print("Client {} is local,responding from this server".format(mac))
            # data['random']=1
            # r = requests.get(url, params = data, timeout=1)
            # raise requests.exceptions.ConnectionError
            r = requests.post(url, data=data, timeout=1)
            print("Response to {} successful!".format(mac))
        except requests.exceptions.ConnectionError:
            print("Client moved to another server!Searching...")
    else:
        print("Client {} is not local, forwarding response to server {} ...".format(mac,client_ip))
        url = "http://" + client_ip + ":8000/front/forward"
        data['mac'] = mac 
        r = requests.get(url, params=data, timeout=1) 
        # r = requests.post(url, data=data, timeout=1)
        if r.status_code==200:
            print("Forwarding response to server {} successful!".format(client_ip))

def multiply_task(params,ip,mac):
    #time.sleep(5)
    num1 = params['num1']
    num2 = params['num2']
    mul = int(num1)*int(num2)
    #send_response_concurrent_search(mul,ip,mac)
    data = {'result':mul}
    send_response_read_from_db(data,mac)

def image_process_task(params,img,img_name,ip,mac):
    #time.sleep(5)
    size = params['size']
    start_time = params['start_time']
    if configuration.local_classify:
        preds = classify.local_classify(img)
    else:
        preds = classify.remote_classify(size,start_time,img,img_name)
    delete_uploaded_file(img)
    data = preds
    send_response_read_from_db(data,mac)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def forward_response(request):
    server_ip = get_client_ip(request)
    if request.method == 'GET':
        data = request.GET.dict()
    if request.method == 'POST':
        data = request.POST.dict()
    mac = data.pop("mac")
    current_client = Client_ip_mac.objects.get(client_mac = mac)
    client_ip = current_client.client_ip
    is_local = current_client.is_local
    print("Forwardind response from {} to  IP: {}, Mac: {}".format(server_ip,client_ip,mac))
    if is_local:
        url = "http://" + client_ip + ":8088"    
        try:
            print("Responding to {}".format(mac))
            # r = requests.get(url, params = {'result':mul}, timeout=1)
            # raise requests.exceptions.ConnectionError
            r = requests.post(url, data=data, timeout=1)
            print("Response to {} successful!".format(mac))
            return HttpResponse(status=200)
        except requests.exceptions.ConnectionError:
            print("Client moved to another server!Searching...")
    else:
        url = "http://" + client_ip + ":8000/front/forward"
        data['mac'] = mac
        r = requests.post(url, data=data, timeout=1)

@csrf_exempt
def request_server(request):
    ip = get_client_ip(request)
    mac = get_mac_from_ip(ip)
    print("Request from IP: {}, MAC: {}".format(ip,mac))
    if request.method == 'GET':
        print(dict(request.GET))
        print(request.GET.dict())
        data = request.GET.dict()
    if request.method == 'POST':
        data = request.POST.dict()
        print(request.FILES)
    t = threading.Thread(target=multiply_task, args=(data,ip,mac,))
    # We want the program to wait on this thread before shutting down.
    t.deamon = False
    t.start()
    #time.sleep(5)
    return HttpResponse(status=202)

@csrf_exempt
def image_upload(request):
    ip = get_client_ip(request)
    mac = get_mac_from_ip(ip)
    print("Request from IP: {}, MAC: {}".format(ip,mac))
    if request.method == 'GET':
        data = request.GET.dict()
    if request.method == 'POST':
        data = request.POST.dict()
        image = request.FILES['file']
        print(request.FILES)
        #if image.multiple_chunks(): print(image.temporary_file_path())
        img = handle_uploaded_file(image)
        img_name = image.name
    t = threading.Thread(target=image_process_task, args=(data,img,img_name,ip,mac,))
    # We want the program to wait on this thread before shutting down.
    t.deamon = False
    t.start()
    #time.sleep(5)
    print("END")
    return HttpResponse(status=202)

