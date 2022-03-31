
<h2 align="center">
  <img src="https://img.icons8.com/dusk/128/000000/whatsapp.png"/>
  <img src="https://img.icons8.com/dusk/128/000000/bot.png"/>
  <br/>
  <b>Whatspper</b>
</h2>

### O que é?

- Interface para envio de menssagens automaticas no whatsapp.

### O que utiliza?

- **Ferramentas**
  - Python
  - Selenium
  - Chromedriver
  - Streamlit
  - Regular Expression

### Como rodar?

- caso não tenha instalado o Selenium

`pip install selenium`

```bash
git clone https://github.com/jvcss/whatspper.git

cd whatspper

streamlit run app.py
```
- abra a interface com
> $ streamlit run app.py

### `Importante!`

- Cria **contatos.csv** automático a partir da lista de **contatos** e **conversas**

- verificação automática das palavras chave **sair** para inclusão na lista de contatos bloqueados antes de enviar a mensagem

- Permite atualizar a base de contatos retirando os que foram excluídos após execução

- caso seu Chrome não abra talvez seja porque o drive que utilizo não seja compatível com a sua versão procure a versão do driver compatível com o seu navegador [AQUI](https://chromedriver.chromium.org/downloads)

- Executável `Windows` e `Linux`

- Windows permite envio de imagens e textos com edição

- Linux não permite adicionar imagens na mensagem

![Whatspper](images/plao_fundo_info_whatspper_automation.jpg)