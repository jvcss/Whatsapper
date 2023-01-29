import re
import urllib.parse
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command
import time

def html_to_url_wppedit(raw_html):
	negrito = re.compile('(<strong>|</strong>)')
	clean_negrito_text = negrito.sub('*', raw_html)
	italico = re.compile('(<em>|</em>)')
	clean_negrito_text = italico.sub('_', clean_negrito_text)
	cutted = re.compile('(<s>|</s>)')
	clean_negrito_text = cutted.sub('~', clean_negrito_text)
	monoletter = re.compile(r'(<span class="ql-font-monospace">|</span>)')
	clean_negrito_text = monoletter.sub('```', clean_negrito_text)
	new_line = re.compile(r'(<br>)')
	clean_negrito_text = new_line.sub('\n', clean_negrito_text)
	CLEANR = re.compile('<.*?>')
	cleantext = re.sub(CLEANR, '', clean_negrito_text)
	cleantext = urllib.parse.quote(cleantext)
	return cleantext

def listar_nomes_desc(content):
	#desc_ = re.findall(r'_1qB8f"><span dir="auto" title="(.*?)" class="', content)
	desc_ = re.search(r'_1qB8f"><span dir="auto" title="(.*?)" class="', content)
	return desc_

def nome_localizado(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` _3vPI2
	try:
		title_name = re.findall(r'"><span dir="auto" title="(.*?)" class="g', texto)
		if title_name is not None:
			return title_name[0]
		else:
			title_alt = re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)
			return title_alt[1]
	except Exception as e: 
		print(f"FALHA NO REGULAR EXPRESSION {e}")

class Cliente:
	"""
		Faz login no whats
		param driver: The selenium driver
		type driver: object
	"""
	google = None
	URL = 'https://web.whatsapp.com/'

	def __init__(self, google=None):
		"""
		param driver The selenium driver
		type driver object
		"""
		self.google = google

	def consultar(self): #
		self.google.get(self.URL)
		self.google.maximize_window()
		try:
			while self.google.title:
				try:
					self.google.execute(Command.STATUS)
				except Exception as e:
					self.google.quit()
		except Exception as e:
			print(f"Could not login {e}")

	def login(self):
		self.google.get(self.URL)
		self.google.maximize_window()
		wait = WebDriverWait(self.google, 999)
		try:
			wnd = wait.until(EC.visibility_of_element_located(GetLocator.ALPHA))
		except TimeoutException:
			self.google.quit()
			return "você precisa ler o QR CODE. Tente denovo"
		if wnd:
			return ''# wnd.text
		else:
			return "algo diferente de nao ter lido BETA no tempo certo."

	def contatos(self):
		cttss = []
		ctt_nome_anterior = ''
		desc_nome_anterior = ''
		is_ctt_not_end = True
		wait = WebDriverWait(self.google, 999)
		try:
			btn_ctt = wait.until(EC.presence_of_element_located(GetLocator.BTN_CHAT))
			btn_ctt.click()
			
			time.sleep(.51)
			ctt_blc1 = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div[2]')))
			ctt_blc1.send_keys(Keys.ARROW_DOWN)
			ctt_blc = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div[2]/div/div')))
			while is_ctt_not_end:
				time.sleep(.1)

				ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))#OK
				
				#print(f"\n\nULTIMO COMANDO {ctt_selected.get_attribute('innerHTML')}??????\n\n")
				
				nome_selecionado = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))#RETORNA UMA OBJETO MATCH COM A PROPRIEDADE GROUP
				#***CASO DESCRIÇÃO NAO EXISTA
				selec_desc_name = listar_nomes_desc(str(ctt_selected.get_attribute('innerHTML')))
				
				
				time.sleep(.1)
				#print(f"\n\nULTIMO COMANDO {nome_selecionado}   ??????\n\n")
				cttss.append(str(nome_selecionado).replace(',', ''))
				#cttss.append(str(nome_selecionado[0]).replace(',', ''))

				if selec_desc_name:
					print(f'{nome_selecionado} :descrição: {selec_desc_name}')
				else:
					selec_desc_name = nome_selecionado#.append(str(f'descrição ausente-{str(nome_selecionado.group(1))[:2]}'))
					print(f'NAO TEM descrição tem conteudo {str(nome_selecionado)}')


				if nome_selecionado != ctt_nome_anterior or selec_desc_name != desc_nome_anterior:
					ctt_nome_anterior = nome_selecionado
					if selec_desc_name:
						desc_nome_anterior = selec_desc_name
				else:
					is_ctt_not_end = False
				print('here?')
				ctt_blc1.send_keys(Keys.ARROW_DOWN)

			back_to_main = wait.until(EC.presence_of_element_located(GetLocator.BACK_BTN))
			back_to_main.click()
			cttss = list(dict.fromkeys(cttss))
			return cttss

		except Exception as e:
			print(f">ERRO:  {e}")
			time.sleep(99)
			return cttss

	def chats_ctt(self):
		chat_ctts = []
		wait = WebDriverWait(self.google, 90)
		fast = WebDriverWait(self.google, 1)
		try:
			btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
			btn_search.send_keys('')
			time.sleep(1)
			ctt_nome_anterior = ''
			btn_search.send_keys(Keys.ARROW_DOWN)
			try:
				chat_bloco = fast.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]')))#//*[@id="pane-side"] #(By.XPATH, '//*[@id="pane-side"]')
			except:
				chat_bloco = fast.until(EC.presence_of_element_located(GetLocator.CHAT_BLOC))#(By.XPATH, '//*[@id="pane-side"]/div[2]')))#
			is_chat_not_end = True
			while is_chat_not_end:
				time.sleep(0.1)
				chat_ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
				selected_name = nome_localizado(str(chat_ctt_selected.get_attribute('innerHTML')))
				
				chat_ctts.append(str(selected_name).replace(',', ''))
				
				if selected_name != ctt_nome_anterior:
					ctt_nome_anterior = selected_name
				else:
					is_chat_not_end = False
				chat_bloco.send_keys(Keys.ARROW_DOWN)
			chat_ctts = list(dict.fromkeys(chat_ctts))
			return chat_ctts
		except Exception as e:
			print(f'\n\n\n\n\n\n\nFALHA {e}')
			time.sleep(99)
			return chat_ctts

	def envia_msg(self, contatos_, mensagem):
		ate_o_fim = True
		self.google.get(self.URL)
		self.google.maximize_window()
		lista_contatos_info = []
		lista_contatos_ = []
		lista_negra = []
		listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{mensagem}')
		
		try:
			image_tag = re.compile(r'<img.*?>').search(mensagem).group()
			mensagem = mensagem.replace(image_tag, '')
		except AttributeError:
			print("No image tag found in message.")

		texto_p_enviar = html_to_url_wppedit(mensagem)
		if os.name == 'nt':

			if bool(listar_imgs):
				
				wait = WebDriverWait(self.google, 999)
				contagem = 0

				while ate_o_fim:
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					try:
						url_to_send = f'https://web.whatsapp.com/send/?text={texto_p_enviar}'
						self.google.get(url_to_send)
						btn_busca = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_BUSCA_CARD)))
						btn_busca.click()
						btn_busca.send_keys(contatos_['contatos'][contagem])
						ActionChains(self.google).send_keys(Keys.TAB).perform()
						time.sleep(2)
						card_contato = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_CONTATO_CARD)))
						card_contato.click()
						time.sleep(1)
						btn_envia_card = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_ENVIA_CARD)))
						btn_envia_card.click()
						time.sleep(1)
						#read the conversation with this selected contact
						tela_atual = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'_2gzeB')))
						elements = tela_atual.find_elements(By.CLASS_NAME,'_11JPr')
						filtered_elements = [e for e in elements if "selectable-text" in e.get_attribute("class") and "copyable-text" in e.get_attribute("class")]
						conteudo_conversa = ""
						for element in filtered_elements:
							conteudo_conversa += element.text+' '
						conteudo_conversa = re.sub('\n', ' ', conteudo_conversa)
						conteudo_conversa = re.sub(r'\s+', '', conteudo_conversa)
						conteudo_conversa = re.sub(r'[^\x00-\x7F]+', '', conteudo_conversa)

						mensagem  = re.sub('<.*?>', ' ', mensagem)
						mensagem = re.sub(r'\s+', '', mensagem)#tira espaços e emoji
						mensagem = re.sub(r'[^\x00-\x7F]+', '', mensagem)

						pedido_sair = re.search("!sair", conteudo_conversa.lower())
						if pedido_sair is not None:
							print(f'\n\n\n...add to BLACK LIST: {contatos_["contatos"][contagem]}')
							lista_negra.insert(0, contatos_['contatos'][contagem])
						if mensagem in conteudo_conversa or pedido_sair is not None:
							print(f'\n\n\n...do not send again to {contatos_["contatos"][contagem]}')
						else:
							ActionChains(self.google).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
							btn_envia = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_ENVIA_IMAGE)))
							btn_envia.click()
							time.sleep(5)
						lista_contatos_.insert(0, contatos_['contatos'][contagem])
					except Exception as e:
						print(f"::ERRO:: contato {contatos_['contatos'][contagem]} ::ERRO::")
					contagem +=1
					time.sleep(1)
				self.google.quit()
				return lista_contatos_, lista_negra
			else:#SE NAO TIVER IMAGEM NOVA ROTINA DE ENVIO DE MSG
				wait = WebDriverWait(self.google, 999)
				contagem = 0

				while ate_o_fim:
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					try:
						#time.sleep(999)
						# https://web.whatsapp.com/send/?text=O
						url_to_send = f'https://web.whatsapp.com/send/?text={texto_p_enviar}'
						self.google.get(url_to_send)
						time.sleep(3)
						#busca contato
						btn_busca = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_BUSCA_CARD)))
						btn_busca.click()
						btn_busca.send_keys(contatos_['contatos'][contagem])
						ActionChains(self.google).send_keys(Keys.TAB).perform()
						time.sleep(2)
						card_contato = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_CONTATO_CARD)))
						card_contato.click()
						time.sleep(1)
						btn_envia_card = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_ENVIA_CARD)))
						btn_envia_card.click()
						time.sleep(1)
						#read the conversation with this selected contact
						tela_atual = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'_2gzeB')))
						elements = tela_atual.find_elements(By.CLASS_NAME,'_11JPr')
						filtered_elements = [e for e in elements if "selectable-text" in e.get_attribute("class") and "copyable-text" in e.get_attribute("class")]
						conteudo_conversa = ""
						for element in filtered_elements:
							conteudo_conversa += element.text+' '
						
						conteudo_conversa = re.sub('\n', ' ', conteudo_conversa)
						conteudo_conversa = re.sub(r'\s+', '', conteudo_conversa)
						conteudo_conversa = re.sub(r'[^\x00-\x7F]+', '', conteudo_conversa)

						mensagem  = re.sub('<.*?>', ' ', mensagem)
						mensagem = re.sub(r'\s+', '', mensagem)#tira espaços e emoji
						mensagem = re.sub(r'[^\x00-\x7F]+', '', mensagem)

						pedido_sair = re.search("!sair", conteudo_conversa.lower())
						if pedido_sair is not None:
							print(f'\n\n\n...add to BLACK LIST: {contatos_["contatos"][contagem]}')
							lista_negra.insert(0, contatos_['contatos'][contagem])
						if mensagem in conteudo_conversa or pedido_sair is not None:
							print(f'\n\n\n...do not send again to {contatos_["contatos"][contagem]}')
						else:
							btn_envia = wait.until(EC.presence_of_element_located((GetLocator.BOTAO_ENVIA_TXT)))
							btn_envia.click()
						#ENVIA SEM IMAGEM
						lista_contatos_.insert(0, contatos_['contatos'][contagem])
					except Exception as e:
						print(f"::ERRO:: contato {contatos_['contatos'][contagem]} ::ERRO::")
					contagem +=1
					time.sleep(1)
				self.google.quit()
				return lista_contatos_, lista_negra
		elif os.name == 'posix':
			wait = WebDriverWait(self.google, 5)
			contagem = 0

			while ate_o_fim:
				if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
				try:#abrir janela clicar em pesquisa. esperar item carregado
					pass
				except Exception as e:
					print(f'FALHA  App Whats. Não achei algum elemento {e}')
				finally:
					time.sleep(2)

				contagem +=1
				time.sleep(1)
			self.google.quit()
			return lista_contatos_info, lista_contatos_, lista_negra

class GetLocator(object):
	ALPHA = (By.XPATH, '/html/body/div[1]/div/div/div[3]/header/div[1]/div')

	BTN_CHAT = (By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')

	SEARCH_INPUT = (By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')

	CHAT_BLOC = (By.XPATH, '//*[@id="pane-side"]/div[2]')

	BACK_BTN = (By.XPATH, '//*[@id="side"]/div[1]/div/div/button')

	BOTAO_BUSCA_CARD = (By.XPATH, '/html/body/div[1]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[2]')

	BOTAO_CONTATO_CARD = (By.XPATH,'/html/body/div[1]/div/span[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/button')

	BOTAO_ENVIA_CARD = (By.XPATH, '/html/body/div[1]/div/span[2]/div/div/div/div/div/div/div/span/div/div/div')

	BOTAO_ENVIA_TXT = (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')

	BOTAO_ENVIA_IMAGE = (By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div')