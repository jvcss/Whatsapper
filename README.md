
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

- caso não tenha instalado o selenium

`pip install selenium`

```bash
git clone https://github.com/jvcss/whatspper.git

cd whatspper

streamlit run app.py
```
- abra a interface com
> $ streamlit run app.py

### `Importante!`

- Salvamento automático da lista de contatos e chats, criada no arquivo **contatos.csv**
- caso seu chrome não abra talvez seja porque o drive que utilizo não seja compativel com a sua versão procure a versão do driver compativel com o seu navegador [AQUI](https://chromedriver.chromium.org/downloads)
- para saber a versão do seu chrome é so ir nas configurações no navegador
- esse app roda no windows e linux com o chrome, em linux não é possivel adicionar imagens
