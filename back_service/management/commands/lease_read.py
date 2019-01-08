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
        lease_database = [entry for entry in Client_ip_mac.objects.values()]
        file_path = find_lease_file()
        # Cached_stamp tells us the last time lease file was saved
        cached_stamp = os.stat(file_path).st_mtime
        with open(file_path,"r") as f:
            cached_lines = f.readlines()
        while True:
            start = time.time()
            # Read the modified time of file and save it
            stamp = os.stat(file_path).st_mtime
            # and then compare with the old one.If different, file is modified
            if stamp != cached_stamp:
                with open(file_path,"r") as f:
                    lines = f.readlines()
                    for line in lines:
                        # We compare with the old lease file.Changed lines are new leases
                        if line not in cached_lines:
                            line = line.split() # [Time of lease expiry, MAC, IP, Computer Name, Client-ID]
                            start2 = time.time()
                            current_client = Client_ip_mac.objects.get(client_mac = line[1])
                            client = Client_ip_mac(client_mac = line[1], client_ip = line[2], is_local = True)
                            client.save()
                            print("Time taken for this save: {} sec".format(time.time()-start2))
                print("Time taken for saves: {} sec".format(time.time()-start))
                cached_lines = lines
                cached_stamp = stamp
            time.sleep(1)
            print("Total time taken: {} sec".format(time.time()-start))

