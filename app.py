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
import strings as literais
from whats import Cliente
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options as opts_google
#from selenium.webdriver.firefox.options import Options

from streamlit_quill import st_quill as text_editor
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

st.set_page_config(
	page_title='Absolut',
	layout='wide',
	initial_sidebar_state='expanded',
	page_icon=literais.apple_dragon_icon,
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

#barra lateral
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
	gb.configure_grid_options(domLayout='normal',onCellValueChanged=literais.js_code_highlight_cell,)
	gb.configure_default_column( editable=editavel, resizable=True)
	gridOptions = gb.build()

	return_mode = list(DataReturnMode.__members__)
	#st.sidebar.radio('modos de retorno', return_mode)
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
					for ctt in contatos_permitidos:#grid_response['data']['contatos']:
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
					for ctt in contatos_permitidos:#grid_response['data']['contatos']:
						f2.write(ctt + '\n')
			except:
				st.info('falha ao reescrever arquivo. verique a integridade')
			
			finally:
				st.session_state.contatos_salvos = pd.read_csv("contatos.csv")
				st.experimental_rerun()
		
		if st.button('🗑️',help='remove itens selecionados'):
			#st.write(f"{grid_response['selected_rows']}")
			#data_response = pd.DataFrame(grid_response['data'], index=None)
			#todos_ctts = data_response.to_csv(index=False)
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
	if st.session_state["swtich_browser"] or st.session_state.beta_on == '':#'BETA':
		try:
			if st.session_state.beta_on == '':#'BETA':
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
					#opts = Options()
					#opts.add_argument("-profile")
					#opts.add_argument('log-level=3')
					#opts.set_preference("dom.webnotifications.enabled", False);
					#opts.add_argument(r"C:\Users\Victor\AppData\Roaming\Mozilla\Firefox\Profiles\027qdkr7.default-release")
					#srvc = Service(r'C:\Users\Victor\Notebook\AbsolutApp\geckodriver.exe')
					if escolha_de_navegador == 'Gecko':
						motorista = webdriver.Firefox(service=srvc,options=opts)
						cliente = Cliente(motorista)
					else:
						motorista = webdriver.Chrome(options=opts)
						cliente = Cliente(motorista)
					#se_navegador_aberto = psutil.Process(motorista.service.process.pid).is_running()
					
					st.session_state.beta_on = cliente.login()
					try:
						st.session_state.contatos_salvos = pd.read_csv("contatos.csv")
					except Exception as e:
						print(f'falhando aqui? {e}')
						temp_chat_list = cliente.chats_ctt()
						#temp_chat_list = cliente.contatos()
						temp_chat_list += cliente.contatos()
						temp_chat_list = list(dict.fromkeys(temp_chat_list))
						st.session_state.contatos_salvos = pd.DataFrame(temp_chat_list, columns=['contatos'], index=None)
						with open('contatos.csv', "w", encoding="utf-8") as fileDriver:
							for each in st.session_state.contatos_salvos:
								fileDriver.write(f'{each}\n')
						
						with open('contatos.csv', "a", encoding="utf-8") as fileDriver_:
							contatos_permitidos = set(list(st.session_state.contatos_salvos['contatos'])) -  set (list(st.session_state.black_list))
						
							for e_ach in contatos_permitidos:#st.session_state.contatos_salvos['contatos']:
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