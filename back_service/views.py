from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

import requests

def get_sender_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
