#region IMPORTS
from base64 import b64decode
import pandas as pd
import streamlit as st
from streamlit_quill import st_quill as text_editor
import os
if os.name == 'nt':
	import win32clipboard
	from PIL import Image
	from io import BytesIO
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
import strings as literais
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

#endregion

PATH_PROFILE = "--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2"
st.set_page_config(
	 page_title='Unidades',
	 layout='centered',
	 initial_sidebar_state='expanded',
	 page_icon=literais.apple_dragon_icon, #"favicon.png" #expanded / collapsed
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)

if "contatos_salvos" not in st.session_state: st.session_state["contatos_salvos"] = pd.DataFrame([], columns=['contatos'])

if "contatos_list" not in st.session_state: st.session_state["contatos_list"] = []

if "ultima_conversa" not in st.session_state: st.session_state["ultima_conversa"] = []

if "black_list" not in st.session_state: st.session_state["black_list"] =  []

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

def listar_nomes_desc(content):
	desc_ = re.findall(r'_1qB8f"><span dir="auto" title="(.*?)" class="fd365im1', content)
	return desc_

def listar_nomes(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.findall(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)

def nome_localizado(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.search(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.search(r'<span dir="auto" title="(.*?)" class="gg', texto)

def extrair_info_ultima_conversa(texto):
	try:
		info_last_talk = re.search(r'<div class="_1i_wG">(.*?)</div>',texto)
	except Exception as e:
		print(f'Não achou nenhuma ultima conversa: {e}')
		return ""
	finally:
		if info_last_talk:
			return info_last_talk
		else: return ""


def desistir_localizado(contato, texto):
	#fr'{contato}: "><div class="_1Gy50"><span dir="ltr" class="i0jNr selectable-text copyable-text"><span>(.*?)<'
	ctt = contato.replace('+', '\+')
	frases = re.findall(fr'{ctt}: "><div class="_1Gy50"><span dir="ltr" class="i0jNr selectable-text copyable-text"><span>(.*?)<', texto)
	#
	for cada in frases:
		print(f'CADA UNIDADE {cada}')
	str_match = [s for s in frases if 'Desistir' in s]
	#print(f'PESSOA {contato} ENCONTRADO--> {str_match}\n\n')
	#print(f'FRASES VISTA--> {frases}\n\n')
	if str_match != []:
	#	print(f'AQUI--> {frases}')
		return contato
	else:
		return False



def ui_login():
	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 999)

	palavra_beta = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="side"]/header/div[1]/div[2]/b')))

	if palavra_beta:
		return palavra_beta.text
	else:
		return 'error'



def ui_lista_chat():
	chat_ctts = []

	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 999)

	btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
	btn_search.send_keys("")
	
	btn_search.send_keys(Keys.ARROW_DOWN)
	time.sleep(1)
	#
	#chat_bloco.send_keys(Keys.ARROW_DOWN) //*[@id="pane-side"]/div[2]
	#try:
	#chat_bloco = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[1]')))
	#except:
	chat_bloco = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[2]')))
	
	ctt_anterior = ''
	
	is_chat_not_end = True
	while is_chat_not_end:

		ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
		selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))

		chat_ctts.append(selected_name.group(1))

		if selected_name.group(1) != ctt_anterior:
			ctt_anterior = selected_name.group(1)
		else:
			is_chat_not_end = False
		print(f'\n\n\n\nNOME: {selected_name.group(1)}\n\n\n')
		time.sleep(.1)
		
		chat_bloco.send_keys(Keys.ARROW_DOWN)
		
	return chat_ctts


def ui_lista_contatos():
	contatos = []
	
	contato_anterior = ''
	descricao_anterior = ''
	fim_da_lista_contatos = True

	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 999)

	icone_ctts = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')))
	icone_ctts.click()

	ctt_blc = wait.until(EC.presence_of_element_located((By.XPATH , '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]')))
	ctt_blc.send_keys(Keys.ARROW_DOWN)
	ctt_blc.send_keys(Keys.ARROW_UP)
	while fim_da_lista_contatos:
		time.sleep(.1)
		
		ctt_selecionado = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))

		nome_selecionado = nome_localizado(str(ctt_selecionado.get_attribute('innerHTML')))

		descricao_nome_selecionado = listar_nomes_desc(str(ctt_selecionado.get_attribute('innerHTML')))

		contatos.append(str(nome_selecionado.group(1)))
		#lista_inter += nome_selecionado

		if descricao_nome_selecionado:
			print(f'\n\n >{nome_selecionado[0]} tem descrição>  {descricao_nome_selecionado[0]}')
		else:
			descricao_nome_selecionado.append(str(f'descrição ausente-{str(nome_selecionado.group(1))[:2]}'))
			print(f"\n\n >{nome_selecionado[0]} SEM descricao> {str(f'descrição ausente-{str(nome_selecionado.group(1))}')}")
		
		if nome_selecionado.group(1) != contato_anterior or descricao_nome_selecionado[0] != descricao_anterior:
			contato_anterior = nome_selecionado.group(1)
			descricao_anterior = descricao_nome_selecionado[0]
		else:
			fim_da_lista_contatos = False
		ctt_blc.send_keys(Keys.ARROW_DOWN)

	back_to_main = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/header/div/div[1]/button')))
	back_to_main.click()
	contatos = list(dict.fromkeys(contatos))
	
	return contatos







def ui_buscar(contatos_):
	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 60)
	contagem = 0
	ate_o_fim = True
	while ate_o_fim:
		if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
		try:
			driver.get('https://web.whatsapp.com/')
			btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
			btn_search.click()
			btn_search.send_keys(contatos_['contatos'][contagem])
			time.sleep(0.51)
			btn_search.send_keys(Keys.ARROW_DOWN)
			ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
			ctt_selected.click()
		except Exception as e:
			st.error(f'{e}')
		finally:
			time.sleep(0.51)
			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
			btn_clear.click()
			contagem +=1
			time.sleep(.21)
	driver.quit()










def ui_enviar_imagem(contatos_,mensagem):
	ate_o_fim = True
	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{mensagem}')
	texto_p_enviar = html_to_wppedit(mensagem)
	wait = WebDriverWait(driver, 60)
	contagem = 0
	lista_contatos_visto = []

	while ate_o_fim:
		if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
		try:
			driver.get('https://web.whatsapp.com/')
			btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
			btn_search.click()
			btn_search.send_keys(contatos_['contatos'][contagem])
			time.sleep(0.51)
			btn_search.send_keys(Keys.ARROW_DOWN)
			ctt_selecionado = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
			time.sleep(.51)
			ctt_selecionado.click()
			info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selecionado.get_attribute('innerHTML')))

			lista_contatos_visto.append(info_ultimo_contato.group(1))

			tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]')))
			

			se_desistente_ = desistir_localizado(contatos_['contatos'][contagem],tela_atual.get_attribute('innerHTML'))

			if bool(listar_imgs):
				espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
				espaco_enviar.send_keys('')
				actions = ActionChains(driver)
				actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
				time.sleep(3)
				espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')))
				espaco_enviar.send_keys(texto_p_enviar) #texto para enviar
				time.sleep(5)
				botao_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')))
				botao_enviar.click()
			else:
				espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
				espaco_enviar.send_keys('')
				espaco_enviar.send_keys(texto_p_enviar)
				botao_enviar_menor = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')))
				botao_enviar_menor.click()

		except Exception as e:
			print(f'envia_msg -- ERROR {e}')
		finally:
			time.sleep(1)

			

			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))

			btn_clear.click()

			contagem +=1

			time.sleep(.5)

	time.sleep(1)
	driver.quit()









def ui_ultima_conversa( contatos_):#dataframe['contatos'], text-img.txt
	ate_o_fim = True
	lista_contatos_info = []
	lista_contatos_ = []

	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	
	wait = WebDriverWait(driver, 60)
	contagem = 0

	while ate_o_fim:
		if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
		try:#abrir janela clicar em pesquisa. esperar item carregado
			driver.get('https://web.whatsapp.com/')

			btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
			btn_search.click()
			btn_search.send_keys(contatos_['contatos'][contagem])
			time.sleep(.81)
			btn_search.send_keys(Keys.ARROW_DOWN)
			
		except Exception as e:
			print(f'envia_msg -- ERROR {e}')
		finally:
			ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
			ctt_selected.click()
			selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
			info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
			
			lista_contatos_info.append(str(info_ultimo_contato.group(1)))
			lista_contatos_.append(selected_name.group(1))

			

			print(f'{selected_name.group(1)} < ULTIMA CONVERSA > {str(info_ultimo_contato.group(1))}')
			time.sleep(.51)

			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
			btn_clear.click()
			contagem +=1
			time.sleep(1)
	driver.quit()
	return lista_contatos_, lista_contatos_info


ESSA_FUNCAO_TEM_PROBLEMA_DE_RUN_TIME = """
def ui_ultima_conversa_chat( contatos_):
	ate_o_fim = True
	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 60)
	contagem = 0
	lista_conta_contatos = list(contatos_['contatos'])
	lista_contatos_info = []
	lista_contatos_ = []
	btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
	btn_search.click()
	chat_bloco = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[2]')))
	btn_search.send_keys(Keys.ARROW_DOWN)
	while ate_o_fim:
		if contagem >= len(lista_conta_contatos) - 1: ate_o_fim = False
		ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
		ctt_selected.click()
		selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
		info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
		print(f'\n\n\n{selected_name.group(1)} - {info_ultimo_contato.group(1)}\n\n')

		if any(selected_name.group(1) in s for s in contatos_['contatos']):
			lista_contatos_info.append(str(info_ultimo_contato.group(1)))
			lista_contatos_.append(selected_name.group(1))
		else:
			#caso contato do chat nao esteja na lista de todos os contatos anteriores
			lista_contatos_info.append('')
			lista_contatos_.append(selected_name.group(1))

			lista_conta_contatos.append(selected_name.group(1))

		contagem +=1
		chat_bloco.send_keys(Keys.ARROW_DOWN)
		#time.sleep(.51)
	dataframe = pd.DataFrame()#st.session_state["contatos_salvos"])
	dataframe['contatos'] = lista_contatos_
	dataframe['ultima conversa'] = lista_contatos_info
	
	#st.session_state["contatos_salvos"] = pd.DataFrame(dataframe)
	driver.quit()
	return pd.DataFrame(dataframe)"""




def ui_ultima_conversa_rapida( contatos_):#dataframe
	ate_o_fim = True
	opts = Options()
	opts.add_argument(PATH_PROFILE)
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	
	wait = WebDriverWait(driver, 60)
	contagem = 0
	lista_contatos_info = []

	while ate_o_fim:
		try:
			if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False

			btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
			btn_search.click()
			btn_search.send_keys(contatos_['contatos'][contagem])
			time.sleep(1)
			btn_search.send_keys(Keys.ARROW_DOWN)
			ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
			time.sleep(.81)
			ctt_selected.click()
			try:
				info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
			except:
				print('Falha Na Ultima Conversa {e}')

			#print(f'\n\n\n{contatos_["contatos"][contagem]} - {info_ultimo_contato.group(1)}\n\n')
			if type(info_ultimo_contato)!=str:
				lista_contatos_info.append(info_ultimo_contato.group(1))
			else:
				lista_contatos_info.append(info_ultimo_contato)
			
			tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]')))
			se_desistente_ = desistir_localizado(contatos_['contatos'][contagem],tela_atual.get_attribute('innerHTML'))

			print(f'DESISTENTE {se_desistente_}\n\n')
			
			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
			time.sleep(2)
			btn_clear.click()
			contagem +=1
		except Exception as e:
			print('Falha Na Ultima Conversa {e}')
			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
			btn_clear.click()
		finally:
			print('................')
	#st.session_state["contatos_salvos"]['ultima conversa'] = lista_contatos_info
	driver.quit()
	return lista_contatos_info












with st.container():
	caixa = st.container()
	caixa.subheader("Mensagem")
	content = text_editor(placeholder="Escreva seu Newsletter Personalizado",html=caixa.checkbox("Entregar como HTML", True),readonly=caixa.checkbox("Apenas leitura", False),key="quill",)
	listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{content}')
	st.subheader('contato dos pandas')

	st.write(st.session_state.contatos_salvos)
	st.write(st.session_state.contatos_list)
	st.write(st.session_state.ultima_conversa)


	if st.sidebar.button('LOGIN', ):
		#on_click=send_to_clipboard('imagem-0.png')
		
		st.sidebar.info(f'Login : {ui_login()}')

	if st.sidebar.button('LISTA CHAT',):
		st.sidebar.info('Executando Chrome')
		
		st.session_state["contatos_list"]  += ui_lista_chat()

		st.session_state["contatos_list"] = list(dict.fromkeys(st.session_state["contatos_list"]))

		st.session_state.contatos_salvos = pd.DataFrame(st.session_state.contatos_list, columns=['contatos'])

		st.experimental_rerun()

	if st.sidebar.button('LISTA CONTATOS',):
		st.sidebar.info('Executando Chrome')

		st.session_state["contatos_list"] += ui_lista_contatos()

		st.session_state["contatos_list"] = list(dict.fromkeys(st.session_state["contatos_list"]))
		
		st.session_state.contatos_salvos = pd.DataFrame(st.session_state.contatos_list, columns=['contatos'])

		st.experimental_rerun()
	
	if st.sidebar.button('CHAT E CONTATOS'):
		st.sidebar.info('Executando Chrome CHAT')
		st.session_state["contatos_list"]  += ui_lista_chat()
		st.session_state["contatos_list"] = list(dict.fromkeys(st.session_state["contatos_list"]))

		st.sidebar.warning('Executando Chrome CONTATOS')
		st.session_state["contatos_list"] += ui_lista_contatos()
		st.session_state["contatos_list"] = list(dict.fromkeys(st.session_state["contatos_list"]))

		st.session_state.contatos_salvos = pd.DataFrame(st.session_state.contatos_list, columns=['contatos'])
		st.experimental_rerun()



	if st.sidebar.button('BUSCA INDIVIDUAL',):
		st.sidebar.info('Executando Chrome')
		ui_buscar(st.session_state.contatos_salvos)

	enviar = st.sidebar.button('ENVIAR IMAGEM',)
	if enviar:
		st.sidebar.info('Executando Chrome')
		st.session_state["contatos_salvos"] = ui_enviar_imagem(st.session_state.contatos_salvos,content)

	if len(listar_imgs) > 0  and not enviar:
		with open(f"imagem-{0}.{listar_imgs[0][0]}", 'wb') as wrb:
			wrb.write(b64decode(listar_imgs[0][1]))
		send_to_clipboard(f"imagem-0.{listar_imgs[0][0]}")

	if st.sidebar.button('ULTIMA CONVERSA BUSCA',):
		st.sidebar.info('Executando Chrome')

		st.session_state["contatos_salvos"]['ultima conversa'] = ui_ultima_conversa_rapida(st.session_state.contatos_salvos)
		st.experimental_rerun()





def remove_repeted():
	remove_reapter = """
						try:
							tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[4]/div/div[3]/div/div[2]/div[3]')))
							
							clean_tela_atual = re.sub(CLEANR, '', tela_atual.get_attribute('innerHTML'))
							
							print(f'EU SEI clean_tela_atual? {clean_tela_atual}') #
							
							already_sending_call_back_no_texts = already_sent(clean_tela_atual, clean_mensagem)
							time.sleep(20)
							
							#print(f'EU SEI Q VEM ATÉ AQUI? {already_sending_call_back_no_texts}') #
							#time.sleep(100)
							#already_sending_call_back_no_texts = already_sent(tela_atual, mensagem_strip)
							
							#mensagem_strip = mensagem_strip.replace("/n", '')
							#print('fine, we found? '+ already_sent(clean_tela_atual, clean_mensagem))
						except:
							#//*[@id="main"]/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/span/div/span
							#print(f'fine EU SEI Q VEM ATÉ AQUI? {already_sending_call_back_no_texts}') #
							#time.sleep(100)
							exiting_no_content = wait_short.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/span/div/span')))
							#print(f"\n{exiting_no_content.get_attribute('innerHTML')}\n")
							if strings.svg_lock == exiting_no_content.get_attribute('innerHTML'):
								#print ("\nthey are equals, found\n")	
								already_sending_call_back_no_texts = False#					CONVERSA LIMPA
							else: #
								print('erro reading lock')
							#already_sending_call_back_no_texts = content_localizado(str(exiting_no_content.get_attribute('innerHTML')))
							#already_sending = False
							#mensagem_strip = mensagem
							#mensagem_strip = mensagem_strip.replace("/n", '')
								tela_atual = '!mensagem_strip'
								#print ("\nnot found first as msg they are not equal found\n")
							time.sleep(500)
							print('EXCESSAO')
						
						if already_sending_call_back_no_texts:
							#//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[1]/div[1]
							botao_fechar_img = wait.until(EC.presence_of_element_located(GetLocator.BOTAO_CANCELAR_IMG))
							botao_fechar_img.click()
							print(f"already sent to {contatos_['contatos'][contagem]}")
							time.sleep(1)
						else:
							pass"""