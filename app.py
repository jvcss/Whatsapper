from jinja2 import pass_eval_context
import streamlit as st
import pandas as pd
import numpy as np
import re
from sympy import EX
import strings as literais
from whats import Cliente
from selenium import webdriver
import streamlit.components.v1 as components
from selenium.webdriver.chrome.options import Options
import psutil
from streamlit_quill import st_quill as text_editor
import the_modal as modal
import pandas.testing
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


##              VARIAVEIS GLOBAIS  [''],columns=[''],
#region
st.cache(allow_output_mutation=True)
def ChatBlockList():
    return []
st.cache(allow_output_mutation=True)
def ChatList():
    return pd.DataFrame()
st.cache(allow_output_mutation=True)
def UpdateContactsToggle():
    return False

if "contatos_salvos" not in st.session_state:
    st.session_state["contatos_salvos"] = ChatList()
if "att_all_ctts" not in st.session_state:
    st.session_state["att_all_ctts"] = UpdateContactsToggle()
if "entrou" not in st.session_state:
    st.session_state["entrou"] = False
if "beta_on" not in st.session_state:
    st.session_state["beta_on"] = ""
if "black_list" not in st.session_state:
    st.session_state["black_list"] =  ChatBlockList()
df = pd.DataFrame()
if "modal_is_open" not in st.session_state:
    st.session_state.modal_is_open = False

#endregion


def get_data():
    #como não está vazia lê a lista virtual primeiro.
    #devemos comparar para ver se a lista fisica é diferente, e caso seja devemos usar a lista local porque salvamos nela
    if not isinstance(st.session_state.contatos_salvos, pd.DataFrame) :
        df = pd.DataFrame(st.session_state.contatos_salvos, columns=['contatos'])
        print("VERIFIQUE A INTEGRIDADE.----------> NAO é DATAFRAME")
    else:
        df = st.session_state.contatos_salvos#virtual file
        df_csv = pd.read_csv("data/contatos.csv")#arquivo
        if st.session_state.contatos_salvos.empty:#se nao tiver virtual file
            df1 = pd.read_csv("data/contatos.csv")
            print(f"LISTA VIRTUAL VAZIA {type(df1)}")
            st.session_state.contatos_salvos = df1
            return df1
        elif df.equals(df_csv):
            print("SINCRONIZADO")
            return df
        elif not df.equals(df_csv):
            #só escrever aqui se arquivo fisico vazio

            #se não tiver vazia passar Lista Virtual para lista fisica
            print("VIRTUAL DIFERENTE DA FISICA[ get_data -> ar1 = st.session_state.contatos_salvos DataFrame write contatos.csv ]")
            #print(f"{st.session_state.contatos_salvos}")
            ar1 = st.session_state.contatos_salvos
            with open('data\contatos.csv', "w", encoding="utf-8") as fd1:
                for each1 in ar1:
                    fd1.write(f'{each1}\n')
            with open('data\contatos.csv', "a", encoding="utf-8") as fd2:
                for each2 in ar1['contatos']:
                    fd2.write(f'\n{each2}\n')
            return df
            #merge VAR and file

        else:
            print("NEM IGUAL NEM DIFERENTE, COM ERRO?")
            df_ = pd.read_csv("data/contatos.csv")
            return df_

#                       BARRA LATERAL
#region
abrir = st.sidebar.button('Abrir Janela Whatsapp')
st.session_state.att_all_ctts = st.sidebar.checkbox('♻️ Sincronizar Contatos', key="caixa_add_ctt")
try:
    if st.session_state.contatos_salvos == [] or st.session_state.contatos_salvos.empty :
        st.sidebar.info('Você não sincronizou a lista Online')
        st.sidebar.button('.', help='Se você já tiver uma tabela click em Salvar')
        #I can even push a button in JS in my own hackcode D:
except Exception as e:
    pass

st.sidebar.write(st.session_state['beta_on'])
st.sidebar.markdown('____')
enable_selection = st.sidebar.checkbox("Selecionar Contatos", value=True, help='Para poder deletar contatos é necessário permitir a seleção')
selection_mode = st.sidebar.radio("Modo de Seleça", ['single','multiple'], help='Selecione o primeiro contato e com CTRL pressionado selecione os demais')
use_checkbox = st.sidebar.checkbox("Marcador de Linha")
editavel = st.sidebar.radio("Modo Edição", [True, False], help='Para habilitar duplo click na linha e alterar o conteúdo')
available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material"]
selected_theme = st.sidebar.selectbox("Tema", available_themes)
st.sidebar.markdown('____')
#st.sidebar.write(st.session_state.modal_is_open)
st.sidebar.subheader('Lista Contatos Online')
st.sidebar.write(st.session_state.contatos_salvos)
st.sidebar.markdown('____')
st.sidebar.subheader('Lista Negra')
st.sidebar.write(st.session_state['black_list'])

#with open('.streamlit\config.toml') as thema:
#    thema.write()
#    thema.readline()
#endregion


#            get_data()
def grid(data ):
    #df_template = pd.DataFrame(data)
    gb = GridOptionsBuilder.from_dataframe(data)#get_data())

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
    #st.sidebar.radio('hmmm', return_mode)
    update_mode = list(GridUpdateMode.__members__)

    with st.form('formulario') as f:
        #incluir contatos
        if st.form_submit_button('+',help='Adiciona linha no fim da lista'):
            list_inputed = pd.DataFrame(['*--novo-contato--*',], columns=['contatos'])
            st.session_state.contatos_salvos = st.session_state.contatos_salvos.append(list_inputed,ignore_index=True)
            st.experimental_rerun()



        grid_response = AgGrid(st.session_state.contatos_salvos, reload_data=True, 
                                theme=selected_theme, gridOptions=gridOptions, 
                                height=400, data_return_mode = return_mode[1], 
                                update_mode=update_mode[6], 
                                fit_columns_on_grid_load=True, 
                                allow_unsafe_jscode=True, enable_enterprise_modules=False,)

        #st.session_state.contatos_salvos = pd.DataFrame(contatos_new_, columns=['contatos'])
        contatos_new_no_copy_no_iligal = set(list(st.session_state.contatos_salvos['contatos'])) -  set (list(st.session_state.black_list)) 

        #remove valores que não estão na lista de contatos atual st.session_state.contatos_salvos['contatos']
        #lista_negra_fantasmas = set(list(st.session_state.black_list)) -  set (list(st.session_state.contatos_salvos['contatos'])) 
        #for cada in lista_negra_fantasmas:
        #    st.session_state.black_list.remove(cada)

        st.sidebar.write(pd.DataFrame(contatos_new_no_copy_no_iligal, columns=['contatos']))
        #st.session_state.contatos_salvos = pd.DataFrame(contatos_new_no_copy_no_iligal, columns=['contatos'])


        #remover items da lista virtual
        if st.form_submit_button('🗑',help='Apagar contatos selecionados'):
            try:

                if len(grid_response['selected_rows']) > 0:
                    lista_local_43 = [] = list(grid_response['selected_rows'])
                    if isinstance(lista_local_43, list):
                        print('OK OK OK, ')
                    else:
                        print('ERRO FATAL NO RECEBIMENTO DO PACOTE')
                    
                    #for item_ in grid_response['selected_rows']:
                        #st.session_state.black_list.append(item_['contatos'])
                        #st.session_state.black_list = list(dict.fromkeys(st.session_state.black_list))
                else:
                    st.session_state.black_list.append(grid_response['selected_rows'][0]['contatos'])
                    st.session_state.black_list = list(dict.fromkeys(st.session_state.black_list))
                #vars1 = pd.DataFrame()
                #st.session_state.contatos_salvos = pd.concat([vars1, grid_response['data']['contatos']], axis=0, ignore_index=True)
                #st.session_state.contatos_salvos = vars1
                #with open('data\output.csv', 'w', encoding="utf-8") as o:
                #    o.write('contatos\n')
                #    o.write(vars1.to_csv(index=False,header=False ))
                #    o.truncate()
                
            except Exception as e:
                #st.write(selected[0])
                if str(e).find('has no attribute'):
                    print('Exception nenhum item selecionado')
                else:
                    print(f'Falha com {e}')
            finally:
                st.experimental_rerun()






        #salvar retorno da tabela AG na lista virtual
        if st.form_submit_button('Salvar', ):
            try:
                st.session_state.contatos_salvos = pd.DataFrame(grid_response['data'])
            except Exception as e:
                if str(e).find('has no attribute'):
                    st.info('Exception Salvar AG geral. Sem atributo em algo')
                else:
                    st.error(f'Falha com {e}')
            finally:
                st.experimental_rerun()
                print(f"evento salvar > ok")






#                       frontend
#region 

if abrir or st.session_state.beta_on == 'BETA':

    opts = Options()
    opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
    opts.add_experimental_option("detach", True)
    #opts.add_argument("--headless")
    try:
        if st.session_state.entrou:
            pass
            print(f'já abriu o navegador não reabrir {st.session_state.entrou}')
            #st.info()
        else:
            global motorista # this will prevent the browser variable from being garbage collected
            global cliente
            motorista = webdriver.Chrome(options=opts)#options=opts ---headless
            st.session_state.entrou = psutil.Process(motorista.service.process.pid).is_running()#psutil.Process(motorista.service.process.pid)
            cliente = Cliente(motorista)
            st.session_state.beta_on = cliente.login()

            #st.info(f'falha {e}')
            if st.session_state.beta_on == 'BETA':
                #se atualizar contatos selecionado
                if st.session_state.att_all_ctts:
                    temp_chat_list = cliente.chats_ctt()
                    temp_chat_list += cliente.contatos()
                    temp_chat_list = list(dict.fromkeys(temp_chat_list))
                    #salvar sempre como PANDAS DATAFRAME
                    #SALVAR NO ARQUIVO
                    #************************************************
                    st.session_state.contatos_salvos = pd.DataFrame(temp_chat_list, columns=['contatos'])
                    #PEDI PRA ATUALIZAR E VOLTOU COM LISTA VALIDA
                    if st.session_state.contatos_salvos != st.session_state.contatos_salvos.empty():
                        st.session_state['att_all_ctts'] = False
                        with open('data\contatos.csv', "w", encoding="utf-8") as fileDriver:
                            for each in st.session_state.contatos_salvos:
                                fileDriver.write(f'{each}\n')
                        with open('data\contatos.csv', "a", encoding="utf-8") as fileDriver_:
                            for e_ach in st.session_state.contatos_salvos['contatos']:
                                fileDriver_.write(f'{e_ach}\n')
        try:
            col1, col2 = st.columns(2)
            with col1:
                #st.header("Mensagem")
                #msgs = st.container()
                #msgs.text_area('Você pode inserir emoji 🧙‍♂️', placeholder='transmissão ilimitada ⚡ contatos')
                #msgs.file_uploader(label='usar imagens', accept_multiple_files=True)
                caixa = st.container()
                caixa.subheader("Mensagem")
                with caixa:
                    content = text_editor(
                        placeholder="Escreva seu Newsletter Personalizado",
                        html=caixa.checkbox("Entregar como HTML", False),
                        readonly=caixa.checkbox("Apenas leitura", False),
                        key="quill",)
                    if content:
                        if st.button('Enviar'):
                            pass
                            #ENVIAR PARA A LISTA
                            #
                            #
                        st.subheader("Resultado")
                        st.markdown('____')
                        st.markdown(content, unsafe_allow_html=True)
                        st.markdown('____')

            with col2:
    
                st.header('')#padding
                #o_modal(titulo='Retirar Contatos')
                try:
                    grid(get_data())
                except Exception as falha_modal:
                    pass
                    print('GRADE RETORNANDO ERRO {e}')
                finally:
                    pass
                
                
                try:
                    with st.form('exibir_arquivo'):
                        st.subheader('Arquivo Contatos')
                        if st.form_submit_button('⟳'):
                            try:
                                st.write(pd.read_csv('data/contatos.csv'))
                            except Exception as e:
                                st.write(st.session_state.contatos_salvos)
                            finally:
                                pass

                            #st.write(st.session_state.contatos_salvos)
                except Exception as e:
                    st.info(f'arquivo it {e}')
                    print(f'FALHA AO EXIBIR ARQUIVO {e}')
                finally:
                    st.download_button('Contatos.csv', st.session_state.contatos_salvos.to_csv().encode('utf-8'),'contatos.csv', help='faça o download dos seus contatos do whatsapp')

        except Exception as e:
            st.info(f'colunas out {e}')
            pass
            #print('saida das colunas {e}')

    except Exception as e:
        if "user data directory is already in use" in str(e):
            st.error("feche a janela do whats aberta anteriormente. Recarregue a página e tente novamente.")
        else:
            #if st.session_state.modal_is_open:
            ##    print('okok')
            #else:
            st.info(f'Já definimos o cliente e os contatos. Erro: {e}')
            #    st.info('Desmarque Atualizar Contatos. Recarregue a página.')
else:
    st.write('Você precisa se conectar ao **Whatsapp** da barra lateral')
    st.write('')
    st.write('Você precisa deixar o WhatsApp Beta habilitado para usar esse app')
    st.write('')
    st.write('Android · Abra WhatsApp > Mais opções > Dispositivos Conectados >  Multi-Dipositivos beta > Entrar no Beta.')
    st.write('')
    st.write('iPhone · Open Config WhatsApp > Linked Devices > Multi-Device Beta > Join Beta')
#endregion 
