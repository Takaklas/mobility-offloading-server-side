from django.core.management.base import BaseCommand, CommandError

from back_service.models import Client_ip_mac
import time
import os

def find_lease_file():
    file_path_1 = '/var/lib/misc/dnsmasq.leases'
    file_path_2 = '/var/log/dnsmasq.leases'
    if os.path.isfile(file_path_1):
        return file_path_1
    elif os.path.isfile(file_path_2):
        return file_path_2
    else:
        raise CommandError('Hell, I cant find the dhcp lease file!')

class Command(BaseCommand):
    def handle(self, *args, **options):
        #client = Client_ip_mac(client_mac = '3', client_ip = '4', is_local = False)
        #client.save()
        for entry in Client_ip_mac.objects.values():
            print(entry)
        file_path = find_lease_file()
        # now do the things that you want with your models here
        while True:
            start = time.time()
            with open(file_path,"r") as f:
                lines = f.readline().split()
                # [Time of lease expiry, MAC, IP, Computer Name, Client-ID]
                for line in lines:
                    start2 = time.time()
                    client = Client_ip_mac(client_mac = '3', client_ip = '4', is_local = False)
                    client.save()
                    print("Time taken for this save: {} sec".format(time.time()-start2))
            print("Time taken for saves: {} sec".format(time.time()-start))
            time.sleep(1)
            print("Total time taken: {} sec".format(time.time()-start))

