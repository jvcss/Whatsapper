import hashlib
import socket
import secrets
import requests

def get_access(client):
  client = ''.join(str(x) for x in client)
  print(client)
  headers = {'client-key': client}
  response = requests.get('http://localhost:5000/key', headers=headers)
  if response.status_code == 401:
    return 'Unauthorized'
  else:
    salted_key = response.json()['key']
    return salted_key

def get_machine_identifier():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return hostname, host_ip

identifier = get_machine_identifier()

key = get_access(identifier)
print(key)