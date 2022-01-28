import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
import time

from bs4 import BeautifulSoup as BS
def num_apperances_of_tag(tag_name,attr, html):
    soup = BS(html)
    return len(soup.find_all(tag_name, attr))

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

    
    def __init__(self, google):
        """
        :param driver: The selenium driver
        :type driver: object
        """
        self.google = google

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
        wait = WebDriverWait(self.google, 30)
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
