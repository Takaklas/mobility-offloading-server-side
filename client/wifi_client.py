import requests
import subprocess
import threading
import client_server3
import net

def send_request(ip):
    split_ip = ip.split('.')
    server_ip = split_ip[0] + '.' + split_ip[1] + '.' + split_ip[2] + '.1'
    url = "http://" + server_ip +":8000/front/request"
    r = requests.get(url, params = {'num1':'5', 'num2':'7'}, timeout=1)
    #subprocess.check_call(["curl", url+"?num1=5&num2=7"])

    #r = requests.post(url, data = {'num1':'5', 'num2':'7'}, timeout=1)
    #subprocess.check_call(["curl", "-d", '"?num1=5&num2=7"', url])

    print(r.status_code)
    print(r.text)
    r.raise_for_status()

if __name__ == "__main__":
    ids = find_network_id2()
    # pprint.pprint(ids)
    client_server_thread = threading.Thread()
    while True:
        cells = parse_scan(ids)
        select = show_only_found(ids,cells)
        pprint.pprint(select)
        # pprint.pprint(cells[0])
        taken_ip = connect_to_strongest(cells,ids)

        # if client_server_thread is alive,
        # client is waiting for a response
        # else client is ready to send new request
        waiting_for_response = client_server_thread.is_alive()       
        if not waiting_for_response:
            send_request(taken_ip)            
            client_server_thread = threading.Thread(target=client_server3.run, args=[])
            client_server_thread.start()

