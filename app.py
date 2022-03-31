
import streamlit as st
import os
if os.name == 'nt':
	import win32clipboard
	from PIL import Image
	from base64 import b64decode
	from io import BytesIO
	import psutil

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
from selenium.webdriver.chrome.options import Options

from streamlit_quill import st_quill as text_editor
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
st.set_page_config(
	 page_title='MKT',
	 layout='wide',
	 initial_sidebar_state='expanded',
	 page_icon=literais.apple_dragon_icon, #"favicon.png" #expanded / collapsed
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)

if "contatos_salvos" not in st.session_state: st.session_state["contatos_salvos"] = pd.DataFrame([''], columns=['contatos'])

if "beta_on" not in st.session_state: st.session_state["beta_on"] = ""

if "wusername" not in st.session_state: st.session_state["wusername"] = "Public"

if "black_list" not in st.session_state: st.session_state["black_list"] =  []

if "flagger_typing" not in st.session_state: st.session_state["flagger_typing"] = True
#if st.sidebar.button('copiar'):
#    send_to_clipboard(f'imagem-0.jpeg')

#barra lateral
#region
abrir = st.sidebar.button('🎈 Whatsapp')

try:
	if st.session_state.contatos_salvos.empty:
		st.sidebar.info('Você não sincronizou a lista Online')
except Exception as e:
	st.info('A lista Online está denificada. Recarregue a página')

st.sidebar.write(st.session_state['beta_on'])

st.sidebar.markdown('____')
st.sidebar.subheader('Lista Contatos Online')
st.sidebar.write(st.session_state.contatos_salvos)
st.sidebar.markdown('____')
st.sidebar.subheader('Lista Negra')
st.sidebar.write(st.session_state['black_list'])
st.sidebar.markdown('____')

enable_selection = st.sidebar.checkbox("Selecionar Contatos", value=True, help='Para poder deletar contatos é necessário permitir a seleção')
selection_mode = st.sidebar.radio("Modo de Seleça", ['single','multiple'], help='Selecione o primeiro contato e com CTRL pressionado selecione os demais')
use_checkbox = st.sidebar.checkbox("Marcador de Linha")
editavel = st.sidebar.radio("Modo Edição", [True, False], help='Para habilitar duplo click na linha e alterar o conteúdo')
available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material"]
selected_theme = st.sidebar.selectbox("Tema", available_themes)

st.session_state["wusername"] = st.sidebar.text_input("Usuário", placeholder='SouCliente', help='Nome do usuário Windows C:\\Users\\SouCliente\\ ')
if st.sidebar.button('Apagar Arquivos'):
	try:
		os.remove("contatos.csv")
		os.remove("contatos_e_status.csv")
		st.info('Contatos Apagados')
	except:
		st.info('não há mais arquivos para deletar')
if st.sidebar.button('Consulta Conta Whatsapp'):
	opts = Options()
	moss_do_ceu = f'--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4'
	#opts.add_experimental_option('excludeSwitches', ['enable-logging'])
	opts.add_argument('log-level=3')
	opts.add_argument(moss_do_ceu)#(fr"--user-data-dir=C:\\Users\\{st.session_state.pc_user}\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	opts.add_experimental_option("detach", True)
	motorista = webdriver.Chrome(options=opts)
	cliente = Cliente(motorista)
	cliente.consultar()

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

	#contatos_permitidos = set(list(grid_response['data']['contatos'])) -  set (list(st.session_state.black_list))
	#print(f'PERMITIDO {contatos_permitidos}')
	#endregion
	st.markdown(literais.css_code_tres_botoes_lado_a_lado, unsafe_allow_html=True)
	with st.container():
		if st.button('+',help='adiciona item'):
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
		
		if st.button('⎌',help='salva itens modificados'):
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
		
		if st.button('🗑',help='remove itens selecionados'):
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
if abrir or st.session_state.beta_on == 'BETA':
	
	opts = Options()
	opts.add_argument(F"--user-data-dir=C:\\Users\\{st.session_state['wusername']}\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	opts.add_experimental_option("detach", True)
	#opts.add_argument("--headless")
	try:
		if st.session_state.beta_on == 'BETA':#depois do primeiro acesso abre aqui
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
					#st.markdown(literais.css_remove_unused_itens, unsafe_allow_html=True)
					
					listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{content}')
					enviar =  st.button('Enviar')
					
					if enviar:
						motorista = webdriver.Chrome(options=opts)#options=opts ---headless
						cliente = Cliente(motorista)
						cliente.envia_msg(st.session_state.contatos_salvos,content)
						st.subheader("Resultado")
						#st.session_state["flagger_typing"] = True
					#flaggerTyping = True
					#if content:
						#in case image already placed in the texteditor
					if len(listar_imgs) > 0:
						pos = 0
						if st.session_state["flagger_typing"]:#enquanto tiver sem imagem vai ser verdadeiro e pode entrar
							for _ in listar_imgs:	#cria as imagens localmente
								with open(f"imagem-{pos}.{listar_imgs[pos][0]}", 'wb') as wrb:
									wrb.write(b64decode(listar_imgs[pos][1]))
								send_to_clipboard(f"imagem-0.png")
								
								pos += 1
							if st.session_state["flagger_typing"] == True:
								st.session_state["flagger_typing"] = not st.session_state["flagger_typing"]#reset state
							print (f'SAIDA <DEVE SER FALSE >{st.session_state["flagger_typing"]}')
					else:
						st.markdown('____')
						st.markdown(content, unsafe_allow_html=True)
						st.markdown('____')
						st.session_state["flagger_typing"] = not st.session_state["flagger_typing"]
						print (f'loop sem imagem em anexo <DEVE SER FALSE >{st.session_state["flagger_typing"]}')
			with col2:
				try:
					grade()
				except Exception as falha_grade:
					print(f'grade retornando erro {falha_grade}')
				try:
					with st.form('exibir_arquivo'):
						st.subheader('Arquivo Contatos')
						if st.form_submit_button('⇩', help='Mostrar arquivo'):
							st.write(pd.read_csv('contatos.csv'))
				except Exception as e:
					st.info('contatos_salvos ausente')
					print(f'FALHA AO EXIBIR ARQUIVO {e}')
				finally:
					st.download_button('contatos.csv', st.session_state.contatos_salvos.to_csv().encode('utf-8'),'contatos.csv', help='faça o download dos seus contatos do whatsapp')
		else:
			if abrir: #PRIMEIRO ACESSO: listar contatos e salvar arquivo
				motorista = webdriver.Chrome(options=opts)
				se_navegador_aberto = psutil.Process(motorista.service.process.pid).is_running()
				cliente = Cliente(motorista)
				st.session_state.beta_on = cliente.login()
				try:
					st.session_state.contatos_salvos = pd.read_csv("contatos.csv")
				except Exception as e:
					temp_chat_list = cliente.chats_ctt()
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
			st.info(f'algum item não foi encontrado durante o envio')
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
