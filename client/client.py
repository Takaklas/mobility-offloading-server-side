import requests
import subprocess
import client_server3

server_ip = '11.0.0.1'
#split_ip = ip.split('.')
#server_ip = split_ip[0] + '.' + split_ip[1] + '.' + split_ip[2] + '.1'
url = "http://" + server_ip +":8000/front/request"
r = requests.get(url, params = {'num1':'5', 'num2':'7'}, timeout=1)
#subprocess.check_call(["curl", url+"?num1=5&num2=7"])

#r = requests.post(url, data = {'num1':'5', 'num2':'7'}, timeout=1)
#subprocess.check_call(["curl", "-d", '"?num1=5&num2=7"', url])

print(r.status_code)
print(r.text)
r.raise_for_status()

client_server3.run()
