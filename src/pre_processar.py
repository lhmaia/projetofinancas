#!/usr/bin/python

import json
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def pre_processa():
    arq = open('../Dados/news_sentimento.json', 'r')
    
    noticias_js = []
    
    for line in arq:
        try:
            noticia = json.loads(line[:-2])
            noticia['date'] = datetime.strptime(noticia['date'], '%Y-%m-%dT%H:%M:%S')
            noticias_js.append(noticia)
        except:
            continue
        
    noticias_js.sort(cmp=lambda x, y: cmp(x['date'], y['date']))
        
    #print len(noticias_js)
    #print noticias_js[0]['date']
    #print noticias_js[len(noticias_js) - 1]['date']
    
    dttxt = open('date_news.txt', 'w')
    for noticia in noticias_js:
        dttxt.write(str(noticia['date']) + "\n")
    
    dttxt.close()
    
    #noticias = pd.DataFrame()
    
    #noticias['title'] = map(lambda noticia: noticia['title'], noticias_js)
    #noticias['text'] = map(lambda noticia: noticia['text'], noticias_js)
    #noticias['date'] = map(lambda noticia: datetime.strptime(noticia['date'], '%Y-%m-%dT%H:%M:%S'), noticias_js)
    
    #=====================================================================================
    #limpa tags HTML
    noticias_whtml = []
    
    for noticia in noticias_js:
        aux = noticia
        aux['text'] = BeautifulSoup(noticia['text'], 'html').get_text().lower().split()
        noticias_whtml.append(aux)
        
    #=====================================================================================    
    #removendo pontuacao e numeros
    '''
    noticias_so_letras = []
    
    conta_erros = 0
    for noticia in noticias_whtml:
        aux = noticia
        aux['text'] = re.sub("[^a-zA-Z0-9]", " ", noticia['text']).lower().split()
        noticias_so_letras.append(aux)
    '''
    #=====================================================================================
    #removendo stopwords
    noticias_wstopwords = []
    stpwords = set(stopwords.words('portuguese'))
    
    for noticia in noticias_whtml:
        aux = noticia
        aux['text'] = [w for w in noticia['text'] if not w in stpwords]
        noticias_wstopwords.append(aux)
    
    #======================================================================================
    #juntando as palavras novamente em uma string
    noticias = []
    
    for noticia in noticias_wstopwords:
        aux = noticia
        aux['text'] = " ".join(noticia['text'])
        noticias.append(aux)
    
    #for i in range(1, 10):
    #    print noticias[i - 1]['text']
    
    return noticias

def extrai_features(clean_data, field_name):
    news_text = pd.DataFrame()
    news_text[field_name] = map(lambda field : field[field_name], clean_data)
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, stop_words = None, max_features = 5000)
    features = vectorizer.fit_transform(news_text[field_name])
    features = features.toarray()
    return features
