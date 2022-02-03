import re
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import win32clipboard
from PIL import Image
from base64 import b64decode
from io import BytesIO
from selenium.common.exceptions import TimeoutException
import time

def html_to_wppedit(raw_html):
	negrito = re.compile('(<strong>|</strong>)')
	clean_negrito_text = negrito.sub('*', raw_html)

	italico = re.compile('(<em>|</em>)')
	clean_negrito_text = italico.sub('_', clean_negrito_text)

	cutted = re.compile('(<s>|</s>)')
	clean_negrito_text = cutted.sub('~', clean_negrito_text)

	monoletter = re.compile(r'(<span class="ql-font-monospace">|</span>)')
	clean_negrito_text = monoletter.sub('```', clean_negrito_text)

	CLEANR = re.compile('<.*?>')
	cleantext = re.sub(CLEANR, '', clean_negrito_text)
	return cleantext

def send_to_clipboard(img_path):
	image = Image.open(img_path)#path
	output = BytesIO()
	image.convert("RGB").save(output, "BMP")
	data = output.getvalue()[14:]
	#print(data)
	output.close()
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)

def listar_nomes(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.findall(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)

def listar_nomes_desc(content):
	desc_ = re.findall(r'_1qB8f"><span dir="auto" title="(.*?)" class="fd365im1', content)
	return desc_

#options = Options()
#options.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
class Cliente:
	"""
		Faz login no whats
		:param driver: The selenium driver
		:type driver: object
	"""
	google = None
	URL = 'https://web.whatsapp.com/'

	def __init__(self, google=None):
		"""
		:param driver: The selenium driver
		:type driver: object
		"""
		self.google = google

	def img_para_ctrl_c(self, img_path):
		image = Image.open(img_path)#path
		output = BytesIO()
		image.convert("RGB").save(output, "BMP")
		data = output.getvalue()[14:]
		output.close()
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
		time.sleep(1)
		print('COPIO COM SUCESSO?')

	def login(self):
		#primeiro vc entra no site
		self.google.get(self.URL)
		self.google.maximize_window()

		wait = WebDriverWait(self.google, 999)
		try:
			wnd = wait.until(EC.visibility_of_element_located(GetLocator.O_BETA))
		except TimeoutException:
			self.google.quit()
			return "você precisa ler o QR CODE. Tente denovo"
		#self.google.
		if wnd:
			return wnd.text
		else:
			return "algo diferente de nao ter lido BETA no tempo certo."

	def contatos(self):
		cttss = []
		wait = WebDriverWait(self.google, 5)
		try:
			btn_ctt = wait.until(EC.presence_of_element_located(GetLocator.BTN_CHAT))
			btn_ctt.click()
			time.sleep(1)
			
			ctt_nome_anterior = ''
			desc_nome_anterior = ''
			is_ctt_not_end = True
			
			box_list_ctt = wait.until(EC.presence_of_element_located(GetLocator.CTT_LIST_BOX))
			conteudo_list_ctt = str(box_list_ctt.get_attribute('innerHTML'))
			cttss = listar_nomes(conteudo_list_ctt)
			
			ctt_blc = wait.until(EC.presence_of_element_located(GetLocator.CTT_BLOC))

			#descer enquanto o elemento selecionado for diferente do anteriormente selecionado
			lista_inter = cttss
			while is_ctt_not_end:
				ctt_blc.send_keys(Keys.ARROW_DOWN)
				#SELECTED CSS class = _2nY6U vq6sj _2_TVt
				ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
				#lista com 1 nome, na ordem
				selec_nomes = listar_nomes(str(ctt_selected.get_attribute('innerHTML')))
				#lista com 1 descricao, na ordem. 
				selec_desc_name = listar_nomes_desc(str(ctt_selected.get_attribute('innerHTML')))
				lista_inter += selec_nomes
				if selec_desc_name:
					print(f'\n\n descrição tem conteudo {selec_desc_name[0]}')
				else:
					selec_desc_name.append(str(selec_nomes[0]))
					print(f'\n\n NAO TEM descrição tem conteudo {selec_nomes[0]}')

				#se contato atual diferente do anterior, desce na lista
				if selec_nomes[0] != ctt_nome_anterior or selec_desc_name[0] != desc_nome_anterior:
					ctt_nome_anterior = selec_nomes[0]
					desc_nome_anterior = selec_desc_name[0]
				else:
					is_ctt_not_end = False
				#ctt_selected.click()
				time.sleep(1)
			back_to_main = wait.until(EC.presence_of_element_located(GetLocator.BACK_BTN))
			back_to_main.click()
			cttss = list(dict.fromkeys(lista_inter))
			return cttss#se deu tudo certo é essa variavel que retorna láaa pro nosso app.py

		except Exception as e:
			print(f">>>:::  {e}")
			return []

	def chats_ctt(self):
		chat_ctts = []
		wait = WebDriverWait(self.google, 30)
		try:
			btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
			btn_search.click()
			time.sleep(1)
			chat_bloco = wait.until(EC.presence_of_element_located(GetLocator.CHAT_BLOC))
			ctt_nome_anterior = ''
			#mini_chat_anterior = ''
			is_chat_not_end = True
			while is_chat_not_end:
				chat_bloco.send_keys(Keys.ARROW_DOWN)
				chat_ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
				selected_name = listar_nomes(str(chat_ctt_selected.get_attribute('innerHTML')))
				chat_ctts += selected_name
				if selected_name[0] != ctt_nome_anterior:
					ctt_nome_anterior = selected_name[0]
				else:
					is_chat_not_end = False
				time.sleep(1)
			chat_ctts = list(dict.fromkeys(chat_ctts))
			return chat_ctts


		except Exception as e:
			print(f'hmm questões na busca chat {e}')

	def envia_msg(self, contatos_, mensagem):#dataframe['contatos'], text-img.txt
		ate_o_fim = True
		self.google.get(self.URL)
		self.google.maximize_window()

		listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{mensagem}')
		texto_p_enviar = html_to_wppedit(mensagem)
		#lista_imgs_ext = []

		if bool(listar_imgs):
			
			wait = WebDriverWait(self.google, 5)
			contagem = 0

			while ate_o_fim:
				if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
				
				btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
				btn_search.click()

				btn_search.send_keys(contatos_['contatos'][contagem])
				time.sleep(1)

				btn_search.send_keys(Keys.ARROW_DOWN)

				time.sleep(1)
				ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
				ctt_selected.click()
				time.sleep(1)

				btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
				btn_clear.click()
				time.sleep(1)

				try:
					espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
					espaco_enviar.click()
					time.sleep(2)

					pos = 0# CTRL + C
					for _ in listar_imgs:
						img_name = f"imagem-{pos}.{listar_imgs[pos][0]}"#posição da extensao da img POS
						print(f'NOME DAS IMAGENS: {img_name} ')
						#self.img_para_ctrl_c(img_name)
						time.sleep(2)
						actions = ActionChains(self.google)
						#espaco_enviar.send_keys(Keys.CONTROL, 'v')
						actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
						time.sleep(10)
						print(f'CRTL V já foi 1º: {img_name} ')
						#actions.key_down(Keys.CONTROL).send_keys('z').key_up(Keys.CONTROL).perform()
						#actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
				except:
					print(f'FALHA AO ANEXAR UMA IMAGEM {e}')
				finally:
					pass
				try:
					espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')))
					espaco_enviar.send_keys(texto_p_enviar) #texto para enviar
					
					botao_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
					botao_enviar.click()
					#BOTAO enviar
				except Exception as e:
					print(f'FALHA AO DIGITAR MENSAGEM {e}')
				finally:
					pass

				contagem += 1

			self.google.quit()
				
			

		else:
			wait = WebDriverWait(self.google, 5)
			contagem = 0

			while ate_o_fim:
				if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
				try:#abrir janela clicar em pesquisa. esperar item carregado
					
					#click em pesquisar
					btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
					btn_search.click()

					btn_search.send_keys(contatos_['contatos'][contagem])
					# insere nome do contato

					time.sleep(1)
					btn_search.send_keys(Keys.ARROW_DOWN)
					ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
					ctt_selected.click()
					time.sleep(1)
					#abre contato selecionado

					btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
					btn_clear.click()
					
					time.sleep(1)
					#apaga busca anterior
					try:
						espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
						espaco_enviar.send_keys(texto_p_enviar) #texto para enviar
						#BOTAO enviar
						box_buscador = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
						box_buscador.click()
					except Exception as e:
						print(f'FALHA AO ABRIR CHAT {e}')
					finally:
						pass
				except Exception as e:
					print(f'FALHA  App Whats. Não achei algum elemento {e}')
				finally:
					time.sleep(2)

				contagem +=1
				time.sleep(1)
			self.google.quit()
		#self.google.maximize_window()

	def ultima_conversa(self, contatos_):#dataframe['contatos'], text-img.txt
		ate_o_fim = True
		self.google.get(self.URL)
		self.google.maximize_window()

		lista_imgs_ext =0
		contatos_['contatos']#contato1,contato2 LIST
		for cada in contatos_['contatos']:
			pass



		wait = WebDriverWait(self.google, 60)
		contagem = 0

		while ate_o_fim:
			if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
			try:#abrir janela clicar em pesquisa. esperar item carregado
				self.google.get(self.URL)
				#click em pesquisar
				
				btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
				btn_search.click()
				btn_search.send_keys(contatos_['contatos'][contagem])
			except Exception as e:
				print(f'envia_msg -- ERROR {e}')
			finally:
				time.sleep(5)
				#aparentemente 11 meses de range
				#encontra a data 1/1/2022 da ultima conversa, se for diferente de horas e nome dos dias conta como data.
				box_buscador = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_1i_wG')))
				#print(box_buscador.get_attribute('innerHTML'))
				#valor  = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-selected="false"]')))
				#valor.click()

				#espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
				#espaco_enviar.send_keys(texto_p_enviar)


			btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
			btn_clear.click()
			contagem +=1
			time.sleep(3)
		self.google.quit()
		#self.google.maximize_window()


class GetLocator(object):

	"""
		:Getter: 'Web Element'
	"""
	
	O_BETA = (By.XPATH, '//*[@id="side"]/header/div[1]/div[2]/b')
	"""
		:span: TEXTO 'beta'
	"""
	
	BTN_CHAT = (By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')
	"""
		:div: BOTAO 'contatos'
	"""
	#tab_index_contact_key     //*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]
	CTT_LIST_BOX = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]/div/div')
	"""
		:div: BLOCO 'CONTATO-BLOCO'
	"""

	CTT_IDX = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[1]/div/div/div[12]/div/div/div[2]/div[1]/div/span/span')
	"""
		:span: TITLE 'CONTATO_NOME'
	"""

	CTT_BLOC = (By.XPATH , '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]')
	"""
		:div: BLOCO 'CONTATOS'
	"""

	SEARCH_INPUT = (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')
	"""
		:div: INPUT
	"""
	CHAT_BLOC = (By.XPATH, '//*[@id="pane-side"]/div[2]')
	"""
		::
	"""
	BACK_BTN = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/header/div/div[1]/button')
	
	"""
		:button: BUTTON
	"""
	CLEAR_BUTTON = (By.XPATH, '//*[@id="side"]/div[1]/div/button')
	"""
		:div: IN //*[@id="pane-side"]/div[1]/div/div
	"""
								 #//*[@id="pane-side"]/div[1]/div/div/div[6]/div/div
								 #//*[@id="pane-side"]/div[1]/div/div
	SELECT_CHAT_BOX = (By.XPATH, '//*[@id="pane-side"]/div[1]/div/div')
	"""
		:div: TEXTBOX
	"""
	TEXT_BOX_CHAT = (By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
	
	"""
		:chat: CLASS
	"""
	CHAT_CLASS_ = (By.CSS_SELECTOR,'#pane-side > div:nth-child(1) > div > div > div:nth-child(9) > div > div > div > div._2EU3r')
	"""
	<div tabindex="-1" aria-selected="false" role="row">
	"""
