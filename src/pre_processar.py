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
            abertura = datetime.strptime("11:00", "%H:%M")
            fechamento = datetime.strptime("19:00", "%H:%M")
            noticia = json.loads(line[:-2])
            datahora = datetime.strptime(noticia['date'], '%Y-%m-%dT%H:%M:%S')

            if datahora.time() >= abertura.time() and datahora.time() <= fechamento.time():
                noticia['date'] =   datahora
                noticias_js.append(noticia)
        
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
        aux['text'] = BeautifulSoup(noticia['text'], 'lxml').get_text().lower().split()
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

def ordena_por_datahora(clean_data, field_text, field_date):
    news_text = pd.DataFrame()
    news_text[field_text] = map(lambda field : field[field_text], clean_data)
    news_text[field_date] = map(lambda field : field[field_date], clean_data)
    news_text = news_text.sort_values('date')
    return news_text

def get_target(news, candles):
    contador = 0
    ultima_acao = 0
    
    feature_preco = []
    target = []
    for dh in news['date']:
        i = ultima_acao
        while (candles[i].datahora < dh):
            i = i + 1
        ultima_acao = i - 1
        feature_preco.append(candles[ultima_acao].fechamento_atual)
        variacao = 0
        if candles[ultima_acao + 2].fechamento_atual > candles[ultima_acao].fechamento_atual:
            variacao = 1
        if candles[ultima_acao + 2].fechamento_atual < candles[ultima_acao].fechamento_atual:
            variacao = -1
        target.append(variacao)
        #print str(str(dh) + ", " + str(candles[ultima_acao].datahora) + ": " + str(candles[ultima_acao].fechamento_atual) + ", " + str(candles[ultima_acao + 2].datahora) + ": "  + str(candles[ultima_acao + 2].fechamento_atual))
    
    aux = pd.DataFrame()
    aux['preco'] = feature_preco
    aux['alvo'] = target
    return aux
        
def get_entrada(features, alvo):
    entrada = pd.DataFrame()
    entrada['alvo'] = alvo['alvo']
    entrada['preco'] = alvo['preco']
    aux = pd.DataFrame(features)
    return entrada.join(aux)

def gera_arquivo(entradas, arq):
    f = open(arq, 'w')
    for i, e in entradas.iterrows():
        linha = str(e['alvo']) + " " + "0:" + str(e['preco'])
        for i in range(1,5000):
            linha = linha + " " + str(i) + ":" + str(e[i - 1])
        linha = linha + "\n"
        f.write(linha)
    f.close()
    
    
def extrai_features(news_text, fieldname):
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, stop_words = None, max_features = 5000)
    features = vectorizer.fit_transform(news_text[fieldname])
    features = features.toarray()
    return features
