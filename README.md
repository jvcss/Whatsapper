
<h2 align="center">
  <img src="https://img.icons8.com/clouds/2x/whatsapp.png"/>
  <img src="https://img.icons8.com/nolan/2x/bot.png"/>
  <br/>
  <b>Whatsapper</b>
  <p>Aplicativo para automatizar Whatsapp</p>
</h2>

## O que é

- Aplicativo Visual para envio de menssagens automáticas no whatsapp.

## O que utiliza

- **Ferramentas**
  - Python
  - Selenium
  - Chromedriver
  - Streamlit
  - Regular Expression

## Como Executar

- caso não tenha instalado as bibliotecas necessárias

`pip install selenium`

```bash
git clone https://github.com/jvcss/whatspper.git

cd whatspper

streamlit run app.py
```

## Funcionalidades do Aplicativo

- Cria **contatos.csv** automático a partir da lista de **contatos** e **conversas**

- Verificação automática das palavras chave **sair** para inclusão na lista de contatos bloqueados antes de enviar a mensagem

- Permite atualizar a base de contatos retirando os que foram excluídos após execução

- Executável `Windows` e `Linux`

- Windows permite envio de imagem e textos com edição

- Linux não permite adicionar imagem na mensagem

- Chrome precisa de uma versão do driver compatível com o seu navegador [Baixar](https://chromedriver.chromium.org/downloads)

![Whatspper](images/plao_fundo_info_whatspper_automation.jpeg)
