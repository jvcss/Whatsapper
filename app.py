import streamlit as st
import os
if os.name == 'nt':
	import win32clipboard
	from PIL import Image
	from base64 import b64decode
	from io import BytesIO

	def send_to_clipboard(img_path):
		image = Image.open(img_path)
		output = BytesIO()
		image.convert("RGB").save(output, "BMP")
		data = output.getvalue()[14:]
		output.close()
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
import re
import pandas as pd

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options as opts_google
#from selenium.webdriver.firefox.options import Options

from streamlit_quill import st_quill as text_editor
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder


import urllib.parse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command
import time

#region LITERAL
apple_dragon_icon = "data:image/png;base64,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"

js_code_highlight_cell="""
function(e) {
    let api = e.api;
    let rowIndex = e.rowIndex;
    let col = e.column.colId;
    
    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
    api.flashCells({
      rowNodes: [rowNode],
      columns: [col],
      flashDelay: 10000000000
    });

};
"""
#endregion
#region CLIENTE

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
#endregion

class Cliente:
	google = None
	URL = 'https://web.whatsapp.com/'

	def __init__(self, google=None):
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
			return ''
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
			while is_ctt_not_end:
				time.sleep(.1)
				ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
				nome_selecionado = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
				selec_desc_name = listar_nomes_desc(str(ctt_selected.get_attribute('innerHTML')))
				time.sleep(.1)
				cttss.append(str(nome_selecionado).replace(',', ''))
				if selec_desc_name:
					print(f'{nome_selecionado} :descrição: {selec_desc_name}')
				else:
					selec_desc_name = nome_selecionado
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
				chat_bloco = fast.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]')))
			except:
				chat_bloco = fast.until(EC.presence_of_element_located(GetLocator.CHAT_BLOC))
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
						mensagem = re.sub(r'\s+', '', mensagem)
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
			else:
				wait = WebDriverWait(self.google, 999)
				contagem = 0

				while ate_o_fim:
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					try:
						url_to_send = f'https://web.whatsapp.com/send/?text={texto_p_enviar}'
						self.google.get(url_to_send)
						time.sleep(3)
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
						mensagem = re.sub(r'\s+', '', mensagem)
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
				try:
					pass
				except Exception as e:
					print(f'FALHA  App Whats. Não achei algum elemento {e}')
				finally:
					time.sleep(2)

				contagem +=1
				time.sleep(1)
			self.google.quit()
			return lista_contatos_info, lista_contatos_, lista_negra



st.set_page_config(
	page_title='Absolut',
	layout='wide',
	initial_sidebar_state='expanded',
	page_icon=apple_dragon_icon,
	menu_items={
		'Get help': 'https://github.com/jvcss',
		'Report a bug': "https://github.com/jvcss",
		'About': "App para automação whatsapp"
	}
)

if "contatos_salvos" not in st.session_state: st.session_state["contatos_salvos"] = pd.DataFrame([''], columns=['contatos'])#pd.DataFrame([''], columns=['contatos'])

if "beta_on" not in st.session_state: st.session_state["beta_on"] = "."

if "black_list" not in st.session_state: st.session_state["black_list"] =  []

if "contatos_list" not in st.session_state: st.session_state["contatos_list"] = []

if "ultima_conversa" not in st.session_state: st.session_state["ultima_conversa"] = []

if "escolhe_browser" not in st.session_state: st.session_state["swtich_browser"] = ""

if "driver_id" not in st.session_state: st.session_state["driver_id"] = ""

if "pc_user" not in st.session_state: st.session_state["pc_user"] = "vitim"

if "browser_path" not in st.session_state: st.session_state["browser_path"] = fr"C:\Users\{st.session_state['pc_user']}\AppData\Roaming\Mozilla\Firefox\Profiles\{st.session_state['driver_id']}"

#region
escolha_de_navegador = st.sidebar.radio('', ['Gecko', 'Chromium'], 0)
st.sidebar.markdown('____')
st.session_state["pc_user"] = st.sidebar.text_input('Nome Usuario', value='vitim')
st.session_state["driver_id"] = st.sidebar.text_input('Driver ID', value='eyhgqphi.default-release',help="Para Chrome o nome da pasta perfil de usuario 'Profile 1'\nPara Firefox o nome da pasta gerada 'r4nd0m.default-release'")
st.sidebar.markdown('____')

st.session_state["browser_path"] = fr"C:\Users\{st.session_state['pc_user']}\AppData\Roaming\Mozilla\Firefox\Profiles\{st.session_state['driver_id']}"

st.session_state["swtich_browser"] = st.sidebar.button("Login")#True#

if escolha_de_navegador == 'Gecko':
	from selenium.webdriver.firefox.options import Options
	from selenium.webdriver.firefox.service import Service
	opts = Options()
	opts.add_argument('-profile')
	opts.set_preference("dom.webnotifications.enabled", False);
	opts.add_argument(f'{st.session_state["browser_path"]}')
	srvc = Service(r'geckodriver.exe')
elif escolha_de_navegador == 'Chromium':
	from selenium.webdriver.chrome.options import Options
	opts = Options()
	opts.add_argument('Log-Level=3')
	opts.add_experimental_option('excludeSwitches', ['enable-logging'])
	opts.add_argument(fr'--user-data-dir=C:\Users\{st.session_state["pc_user"]}\AppData\Local\Google\Chrome\User Data\{st.session_state["driver_id"]}')

try:
	if st.session_state.contatos_salvos.empty:
		st.sidebar.info('Você não sincronizou a lista Online')
except Exception as e:
	st.info('A lista Online está denificada. Recarregue a página')
	st.sidebar.info(f"Versão {st.session_state['beta_on']}")

if st.sidebar.button('Consultar'):
	if escolha_de_navegador == 'Gecko':
		motorista = webdriver.Firefox(service=srvc,options=opts)
		cliente = Cliente(motorista)
		cliente.consultar()
	else:
		motorista = webdriver.Chrome(options=opts)
		cliente = Cliente(motorista)
		cliente.consultar()
st.sidebar.markdown('____')
st.sidebar.subheader('Lista Contatos Online')
st.sidebar.write(st.session_state.contatos_salvos)
st.sidebar.markdown('____')
st.sidebar.subheader('Lista Negra')
st.sidebar.write(st.session_state['black_list'])

enable_selection = st.sidebar.checkbox("Selecionar Contatos", value=True, help='Para poder deletar contatos é necessário permitir a seleção')
selection_mode = st.sidebar.radio("Modo de Seleça", ['single','multiple'], help='Selecione o primeiro contato e com CTRL pressionado selecione os demais')
use_checkbox = st.sidebar.checkbox("Marcador de Linha")
editavel = st.sidebar.radio("Modo Edição", [True, False], help='Para habilitar duplo click na linha e alterar o conteúdo')
available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material"]
selected_theme = st.sidebar.selectbox("Tema", available_themes)
if st.sidebar.button('Apagar Arquivos'):
	try:
		os.remove("contatos.csv")
		os.remove("contatos_e_status.csv")
		st.info('Contatos Apagados')
	except:
		st.info('não há mais arquivos para deletar')
#endregion

def grade():
	#region DECLARA GRADE
	gb = GridOptionsBuilder.from_dataframe(pd.read_csv('contatos.csv'))
	if enable_selection:
		gb.configure_selection(selection_mode)
		if use_checkbox:
			gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
		if ((selection_mode == 'multiple') & (not use_checkbox)):
			gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=True, suppressRowDeselection=False)
	gb.configure_grid_options(domLayout='normal',onCellValueChanged=js_code_highlight_cell,)
	gb.configure_default_column( editable=editavel, resizable=True)
	gridOptions = gb.build()
	return_mode = list(DataReturnMode.__members__)
	update_mode = list(GridUpdateMode.__members__)
	grid_response = AgGrid(pd.read_csv('contatos.csv'), gridOptions=gridOptions, reload_data=False, theme=selected_theme, height=400,fit_columns_on_grid_load=True,allow_unsafe_jscode=True,update_mode=update_mode[6], data_return_mode = return_mode[1], enable_enterprise_modules=False,)
	#endregion
	st.markdown("""
	<style>
	
	</style>
	""", unsafe_allow_html=True)
	with st.container():
		if st.button('➕',help='adiciona item'):
			try:
				with open('contatos.csv', "w", encoding="utf-8") as f4:
					for ctt in grid_response['data']:
						f4.write(ctt + '\n')
				
				with open('contatos.csv', "a", encoding="utf-8") as f6:
					for ctt in ['*_novo contato_*']:
						f6.write(ctt + '\n')
				
				with open('contatos.csv', "a", encoding="utf-8") as f5:
					contatos_permitidos = set(list(grid_response['data']['contatos'])) -  set (list(st.session_state.black_list))
					for ctt in contatos_permitidos:
						f5.write(ctt + '\n')
			except:
				st.info('falha ao adicionar contato. tente sincronizar novameente')
			
			finally:
				st.session_state.contatos_salvos = pd.read_csv("contatos.csv")
				st.experimental_rerun()
		
		if st.button('💾',help='salva itens modificados'):
			try:
				with open('contatos.csv', "w", encoding="utf-8") as f1:
					for ctt in grid_response['data']:
						f1.write(ctt + '\n')
				with open('contatos.csv', "a", encoding="utf-8") as f2:
					contatos_permitidos = set(list(grid_response['data']['contatos'])) -  set (list(st.session_state.black_list))
					for ctt in contatos_permitidos:
						f2.write(ctt + '\n')
			except:
				st.info('falha ao reescrever arquivo. verique a integridade')
			
			finally:
				st.session_state.contatos_salvos = pd.read_csv("contatos.csv")
				st.experimental_rerun()
		
		if st.button('🗑️',help='remove itens selecionados'):
			string_list_contato = []
			if len(grid_response['selected_rows']) > 0:
				with open('contatos.csv', "r", encoding="utf-8") as ctts_file:
					string_list_contato = ctts_file.readlines()
					string_list_contato = [lista_item[:-1] for lista_item in string_list_contato if lista_item.strip()]
				
				for cada in grid_response['selected_rows']:
					string_list_contato.remove(cada['contatos'])
			
				try:
					with open('contatos.csv', "w", encoding="utf-8") as f3:
						for ctt in string_list_contato:
							f3.write(ctt + '\n')
			
				except:
					st.info('falha ao reescrever arquivo. verique a integridade')
				
				finally:
					st.session_state.contatos_salvos = pd.read_csv("contatos.csv")
					st.experimental_rerun()
#region MENU

def main_call():
	if st.session_state["swtich_browser"] or st.session_state.beta_on == '':
		try:
			if st.session_state.beta_on == '':
				col1, col2 = st.columns(2)
				with col1:
					caixa = st.container()
					caixa.subheader("Mensagem")
					with caixa:
						
						content = text_editor(
							placeholder="Escreva seu Newsletter Personalizado",
							html=caixa.checkbox("Entregar como HTML", True),
							readonly=caixa.checkbox("Apenas leitura", False),
							key="quill",)
							
						if os.name == 'nt':
							listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{content}')
						enviar =  st.button('Enviar')

						if enviar:
							if escolha_de_navegador == 'Gecko':
								motorista = webdriver.Firefox(service=srvc,options=opts)
								cliente = Cliente(motorista)
							else:
								motorista = webdriver.Chrome(options=opts)
								cliente = Cliente(motorista)
							
							st.session_state["contatos_list"], st.session_state['black_list'] = cliente.envia_msg(st.session_state.contatos_salvos,content)

							dataframe = pd.DataFrame(st.session_state['contatos_salvos'], index=None)
							dataframe['contatos'] = st.session_state["contatos_list"]
							
							st.session_state.contatos_salvos = dataframe
							dataframe.to_csv('contatos_e_status.csv', index = False)
							with open('contatos.csv', "w", encoding="utf-8") as f1:
								for ctt in ['contatos']:
									f1.write(ctt + '\n')
							with open('contatos.csv', "a", encoding="utf-8") as f2:
								contatos_permitidos = set(list(st.session_state.contatos_salvos['contatos'])) -  set(list(st.session_state.black_list))
								for ctt in contatos_permitidos:
									f2.write(ctt + '\n')
							st.experimental_rerun()

						if content:
							if os.name == 'nt':
								if len(listar_imgs) > 0 and not enviar:
									po_si = 0
									for _ in listar_imgs:
										if os.path.exists(os.path.abspath(f"imagem-{0}.{listar_imgs[po_si][0]}")) is True:
											os.remove(os.path.abspath(f"imagem-{0}.{listar_imgs[po_si][0]}"))
											po_si += 1
											print('removi as IMAGENS anteriores primeiro')

									pos = 0
									for _ in listar_imgs:
										with open(f"imagem-{pos}.{listar_imgs[pos][0]}", 'wb') as wrb:
											wrb.write(b64decode(listar_imgs[pos][1]))
										send_to_clipboard(f"imagem-0.{listar_imgs[pos][0]}")
										pos += 1
								else:
									print('\n\n\n\n\n\n\n\n')
									pass

							elif os.name == 'posix':
									st.markdown('____')
									st.markdown(content, unsafe_allow_html=True)
									st.markdown('____')
				with col2:
					try:
						grade()
					except Exception as falha_grade:
						print(f'grade retornando erro {falha_grade}')
					try:
						with st.form('exibir_arquivo'):
							st.subheader('Arquivo Contatos')
							if st.form_submit_button('⇩', help='Mostrar arquivo'):
								st.write(pd.read_csv('contatos_e_status.csv'))
					except Exception as e:
						st.info('contatos_salvos ausente')
						print(f'FALHA AO EXIBIR ARQUIVO {e}')
					finally:
						st.download_button('contatos.csv', st.session_state.contatos_salvos.to_csv().encode('utf-8'),'contatos.csv', help='faça o download dos seus contatos do whatsapp')
						st.download_button('contatos_e_status.csv', st.session_state.contatos_salvos.to_csv().encode('utf-8'),'contatos_e_status.csv', help='faça o download dos seus contatos com status do whatsapp',key='err',)
			else:
				if st.session_state["swtich_browser"]:
					if escolha_de_navegador == 'Gecko':
						motorista = webdriver.Firefox(service=srvc,options=opts)
						cliente = Cliente(motorista)
					else:
						motorista = webdriver.Chrome(options=opts)
						cliente = Cliente(motorista)
					st.session_state.beta_on = cliente.login()
					try:
						st.session_state.contatos_salvos = pd.read_csv("contatos.csv")
					except Exception as e:
						print(f'falhando aqui? {e}')
						temp_chat_list = cliente.chats_ctt()
						temp_chat_list += cliente.contatos()
						temp_chat_list = list(dict.fromkeys(temp_chat_list))
						st.session_state.contatos_salvos = pd.DataFrame(temp_chat_list, columns=['contatos'], index=None)
						with open('contatos.csv', "w", encoding="utf-8") as fileDriver:
							for each in st.session_state.contatos_salvos:
								fileDriver.write(f'{each}\n')
						
						with open('contatos.csv', "a", encoding="utf-8") as fileDriver_:
							contatos_permitidos = set(list(st.session_state.contatos_salvos['contatos'])) -  set (list(st.session_state.black_list))
						
							for e_ach in contatos_permitidos:
								fileDriver_.write(f'{e_ach}\n')
					motorista.quit()
					st.experimental_rerun()

		except Exception as e:
			if "user data directory is already in use" in str(e):
				st.error("feche a janela do whats aberta anteriormente. Recarregue a página e tente novamente.")
			elif "Ordinal0" in str(e):
				st.info(e)
				st.info(f'você pode refazer a operação excluindo o contatos virtuais já vistos')
			else:
				st.info(f'Já definimos o cliente e os contatos. Erro: {e}')

	else:
		st.write('Você precisa se conectar ao **Whatsapp** da barra lateral')
		st.write('')
		st.write('')
		st.write('Você precisa deixar o WhatsApp Beta habilitado para usar esse app')
		st.write('')
		st.write('')
		st.write('Android · Abra WhatsApp > Mais opções > Dispositivos Conectados >  Multi-Dipositivos beta > Entrar no Beta.')
		st.write('')
		st.write('')
		st.write('iPhone · Open Config WhatsApp > Linked Devices > Multi-Device Beta > Join Beta')
#endregion 




if __name__ == '__main__': #
	main_call()