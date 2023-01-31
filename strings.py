import requests
import uuid
import subprocess
def get_machine_id():
		mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
		return mac_address
def get_access():
	response = requests.get('http://localhost:5000/key', headers= {'client-key': ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1]).replace(':','')})
	if response.status_code == 401:
		return 'Unauthorized'
	else:
		salted_key = response.json()['key']
		return salted_key
supersafe = get_machine_id()
try:
	ONE_CLIENT = get_access()

	if supersafe is not None :
		print('autenticando usuario no servidor')
		if ONE_CLIENT == 'Unauthorized' :
			print('ESSE COMPUTADOR NÃO ESTÁ AUTORIZADO A USAR ESSA APLICAÇÃO, COMPRE A LINCESA entrando em contato com github.com/jvcss')
			exit()
		else:
			print(f'usuario : {ONE_CLIENT}')
			subprocess.call(["Whatsapper.bat"])
	else:
		print('ESSE COMPUTADOR NÃO ESTÁ AUTORIZADO A USAR ESSA APLICAÇÃO, COMPRE A LINCESA entrando em contato com github.com/jvcss')
		exit()
except Exception as e:
	print('SERVIDOR FORA DO AR ENTRE EM CONTATO COM github.com/JVCSS')