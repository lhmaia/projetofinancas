#!/usr/bin/python

import json
import re
#import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup 

arq = open('../Dados/news_sentimento.json', 'r')

noticias_js = []

for line in arq:
    try:
        noticia = json.loads(line[:-2])
        noticias_js.append(noticia)
    except:
        continue
    
print len(noticias_js)

#noticias = pd.DataFrame()

#noticias['title'] = map(lambda noticia: noticia['title'], noticias_js)
#noticias['text'] = map(lambda noticia: noticia['text'], noticias_js)
#noticias['date'] = map(lambda noticia: datetime.strptime(noticia['date'], '%Y-%m-%dT%H:%M:%S'), noticias_js)

#=====================================================================================
#limpa tags HTML
noticias_whtml = []

for noticia in noticias_js:
    aux = noticia
    aux['text'] = BeautifulSoup(noticia['text'], 'html').get_text()
    noticias_whtml.append(aux)

#=====================================================================================    
#removendo pontuacao e numeros
noticias_so_letras = []

conta_erros = 0
for noticia in noticias_whtml:
    aux = noticia
    aux['text'] = re.sub("[^a-zA-Z]", " ", noticia['text']).lower()
    noticias_so_letras.append(aux)
        
print len(noticias_so_letras)
    
for i in range(1, 10):
    print noticias_so_letras[i - 1]['text']

#=====================================================================================