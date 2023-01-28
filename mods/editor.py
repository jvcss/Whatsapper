#!/usr/bin/env python3
import streamlit as st
import strings as literais
from streamlit_ace import st_ace
import os
from os import listdir
from os.path import isfile, join

THEMES = ["ambiance", "chaos", "chrome", "clouds", "clouds_midnight", "cobalt", 
"crimson_editor", "dawn", "dracula", "dreamweaver", "eclipse", 
"github", "gob", "gruvbox", "idle_fingers", "iplastic","katzenmilch", 
"kr_theme", "kuroir", "merbivore", "merbivore_soft", "mono_industrial", 
"monokai", "nord_dark", "pastel_on_dark", "solarized_dark", "solarized_light", 
"sqlserver", "terminal","textmate", "tomorrow", "tomorrow_night", 
"tomorrow_night_blue", "tomorrow_night_bright", "tomorrow_night_eighties", 
"twilight", "vibrant_ink", "xcode"]

LANGUAGES = [
    "python","dart","abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", 
    "asciidoc", "asl", "assembly_x86", "autohotkey", "batchfile", "c9search", "c_cpp", "cirru", 
    "clojure", "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra", 
    "csound_score", "csp", "css", "curly", "d",  "diff", "django", "dockerfile", "dot", "drools", 
    "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp", "fsl", "ftl", 
    "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema", "groovy", "haml", 
    "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir", "html_ruby", "ini", 
    "io", "jack", "jade", "java", "javascript", "json", "json5", "jsoniq", "jsp", "jssm", "jsx", "julia", 
    "kotlin", "latex", "less", "liquid", "lisp", "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", 
    "lucene", "makefile", "markdown", "mask", "matlab", "maze", "mediawiki", "mel", "mixal", "mushcode", 
    "mysql", "nginx", "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "pascal", "perl", "perl6", 
    "pgsql", "php", "php_laravel_blade", "pig", "plain_text", "powershell", "praat", "prisma", "prolog", 
    "properties", "protobuf", "puppet", "qml", "r", "razor", "rdoc", "red", "redshift", "rhtml", 
    "rst", "ruby", "rust", "sass", "scad", "scala", "scheme", "scss", "sh", "sjs", "slim", "smarty", 
    "snippets", "soy_template", "space", "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", 
    "terraform", "tex", "text", "textile", "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", 
    "velocity", "verilog", "vhdl", "visualforce", "wollok", "xml", "xquery", "yaml"
]

st.set_page_config(page_title='Ace Editor', layout='wide',initial_sidebar_state='expanded', page_icon=literais.apple_dragon_icon, 
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)
my_laguage = st.sidebar.selectbox('languages', LANGUAGES)
my_theme = st.sidebar.selectbox('themes', THEMES)
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