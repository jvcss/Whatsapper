import re
import urllib.parse

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

msg = """<p>Para tudo e se liga nessa super promo que tá rolando aqui na Absolut </p><p><strong>SE LIGA, HEEEEIN!</strong></p><p><br></p><p>Não perca nenhum desconto! Vem conferir </p><p><br></p><p><br></p><p>Loja 1: Av. T-11, N. 393, St. Bueno</p><p><br></p><p><br></p><p>🥜 ABSOLUT - PRODUTOS NATURAIS 🟡🔵</p><p><br></p><p><br></p><p>📱 62 9 9918-4004</p><p>☎️ 62 3091-7324</p>"""
#print(html_to_wppedit(msg),'\n\n')

print(html_to_url_wppedit(msg))