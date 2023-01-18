#!/usr/bin/env python3
import streamlit as st
import strings as literais
from streamlit_ace import st_ace
import os
from os import listdir
from os.path import isfile, join

st.set_page_config(page_title='Ace Editor', layout='wide',initial_sidebar_state='expanded', page_icon=literais.apple_dragon_icon, 
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)
my_laguage = st.sidebar.selectbox('languages', literais.LANGUAGES)
my_theme = st.sidebar.selectbox('themes', literais.THEMES)
# Display editor's content as you type

def list_files():
    cwd = os.getcwd()
    onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
    onlyfiles_ = [os.path.join(cwd, f) for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f)) and f[-2:] =="py"]
    #print(f'DIRETORIO {cwd}\n {onlyfiles_}')
    return onlyfiles_
def file_reader(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as arqv:
        tudo = arqv.read()
    return tudo

st.header("Aws dog editor")
arquivo_selecionado = st.selectbox('list python scripts', list_files())
content = st_ace(value=file_reader(arquivo_selecionado),height=800,theme=my_theme,language=my_laguage,)


st.sidebar.header("Observador")
salvar = st.sidebar.button('salvar')
if salvar:
    with open(arquivo_selecionado, 'w', encoding='utf-8') as arquivo:
        arquivo.write(content)
    
    #st.code(content)