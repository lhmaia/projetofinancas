#!/usr/bin/python

import json
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

n_features = 50
PERCENTUAL_TRAIN = 80

def get_file_to_cluster(saida):
    arq = open('../Dados/news_2016.json', 'r')
    out = open(saida, 'w')
    for line in arq:
        noticia = json.loads(line[:-2])
        out.write("anonimo\t")
        out.write(str(datetime.strptime(noticia['date'], '%Y-%m-%dT%H:%M:%S'))[:10])
        out.write("\t")
        out.write(noticia['title'].encode('utf-8').strip())
        out.write("\n")     
    
    arq.close()
    out.close()
    


def pre_processa(nome_ativo):
    ativo = nome_ativo.lower()
    print ativo
    #arq = open('../Dados/news_sentimento.json', 'r')
    arq = open('../Dados/news_2016.json', 'r')
    entities = pd.read_csv("../Dados/DADOS2-entities.csv")
    codigo_ativo = entities.loc[entities['slug'] == ativo]['id'].values[0]
    
    noticias_js = []
    abertura = datetime.strptime("11:00", "%H:%M")
    fechamento = datetime.strptime("19:00", "%H:%M")

    for line in arq:            
        noticia = json.loads(line[:-2])
        if codigo_ativo in noticia['entities']:
            datahora = datetime.strptime(noticia['date'], '%Y-%m-%dT%H:%M:%S')
            
            if datahora.time() >= abertura.time() and datahora.time() <= fechamento.time():
                noticia['date'] =   datahora
                noticias_js.append(noticia)
                    
    
        
    noticias_js.sort(cmp=lambda x, y: cmp(x['date'], y['date']))
    
    arqteste = open('testedatahora.txt', 'w')
    for n in noticias_js:
        arqteste.write(str(n['date']) + "\n")
    
    arqteste.close()
    
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
        aux['text'] = BeautifulSoup(re.sub("[^a-zA-Z]", " ", noticia['text']), 'lxml').get_text().lower().split()
        noticias_whtml.append(aux)
        
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
    data_hora = []
    preco_alvo = []
    for dh in news['date']:
        i = ultima_acao
        while (candles[i].datahora < dh):
            i = i + 1
        ultima_acao = i - 1
        feature_preco.append(candles[ultima_acao].fechamento_atual)
        data_hora.append(dh)
        preco_alvo.append(candles[ultima_acao + 2].fechamento_atual)
        variacao = 0
        if candles[ultima_acao + 2].fechamento_atual > candles[ultima_acao].fechamento_atual:
            variacao = 1
        if candles[ultima_acao + 2].fechamento_atual < candles[ultima_acao].fechamento_atual:
            variacao = -1
        target.append(variacao)
        #target.append(candles[ultima_acao + 2].fechamento_atual)
        #print str(str(dh) + ", " + str(candles[ultima_acao].datahora) + ": " + str(candles[ultima_acao].fechamento_atual) + ", " + str(candles[ultima_acao + 2].datahora) + ": "  + str(candles[ultima_acao + 2].fechamento_atual))
    
    aux = pd.DataFrame()
    aux['preco_alvo'] = preco_alvo
    aux['preco'] = feature_preco
    aux['alvo'] = target
    aux['data_hora'] = data_hora
    return aux
        
def get_entrada(features, alvo):
    entrada = pd.DataFrame()
    entrada['alvo'] = alvo['alvo']
    entrada['preco'] = alvo['preco']
    entrada['data_hora'] = alvo['data_hora']
    entrada['preco_alvo'] = alvo['preco_alvo']
    aux = pd.DataFrame(features)
    return entrada.join(aux)

def executa_naive_bayes(features, alvo, percentual = PERCENTUAL_TRAIN):
    entrada = pd.DataFrame()
    entrada['preco'] = alvo['preco']
    #entrada['data_hora'] = alvo['data_hora']
    aux = pd.DataFrame(features)
    
    X = entrada.join(aux)
    precos = []
    for p in X['preco']:
        precos.append(float(p))

    num_train = (len(X) * percentual) / 100

    X['preco'] = precos
    Xt = X[0:num_train - 1]
    Xp = X[num_train:len(X) - 1]
    Yt = alvo['alvo'][0:num_train - 1]
    Yp = alvo['alvo'][num_train:len(alvo) - 1]
    clf = MultinomialNB()
    clf.fit(Xt.values, Yt.values)
    print clf.score(Xp.values, Yp.values)
    print clf.predict(Xp.values)
    

def gera_arquivo(entradas, arq, percentual = PERCENTUAL_TRAIN):
    train = 'dados/' + arq + '.train'
    pred = 'dados/' + arq + '.pred'
    data_hora_pred = 'dados/' + arq + '.pred.date'
    data_hora_train = 'dados/' + arq + '.train.date'
    
    ft = open(train, 'w')
    fp = open(pred, 'w')
    ftd = open(data_hora_train, 'w')
    fpd = open(data_hora_pred, 'w')
    
    num_train = (len(entradas) * percentual) / 100
    conta = 0
    for i, e in entradas.iterrows():
        linha = str(e['alvo']) + " " + "0:" + str(e['preco'])
        for t in range(1,n_features):
            freq = 0
            if e[t - 1] > 0: freq = 1
            #linha = linha + " " + str(t) + ":" + str(e[t - 1])
            linha = linha + " " + str(t) + ":" + str(freq)
        linha = linha + "\n"
        conta = conta + 1
        if conta < num_train:
            ft.write(linha)
            ftd.write(str(e['data_hora']) + ';' + str(e['preco_alvo']) + '\n')
        else:
            fp.write(linha)
            fpd.write(str(e['data_hora']) + ';' + str(e['preco_alvo']) + '\n')
    
    ftd.close()
    fpd.close()
    ft.close()
    fp.close()
    
def gera_arquivo_indicadores(entradas, arq, percentual = PERCENTUAL_TRAIN):
    train = 'dados/' + arq + '.train'
    pred = 'dados/' + arq + '.pred'
    data_hora_pred = 'dados/' + arq + '.pred.date'
    data_hora_train = 'dados/' + arq + '.train.date'
    
    ft = open(train, 'w')
    fp = open(pred, 'w')
    ftd = open(data_hora_train, 'w')
    fpd = open(data_hora_pred, 'w')
    
    num_train = (len(entradas) * percentual) / 100
    conta = 0
    for i, e in entradas.iterrows():
        linha = str(e['alvo']) + " " + "0:" + str(e['preco'])
        linha = linha + " 1:" + str(e['sma'])
        linha = linha + " 2:" + str(e['ifr'])
        linha = linha + "\n"
        conta = conta + 1
        
        if conta < num_train:
            ft.write(linha)
            ftd.write(str(e['data_hora']) + ';' + str(e['preco']) + '\n')
        else:
            fp.write(linha)
            fpd.write(str(e['data_hora']) + ';' + str(e['preco']) + '\n')
    
    ftd.close()
    fpd.close()
    ft.close()
    fp.close()
    
    
def extrai_features(news_text, fieldname):
    #vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, stop_words = None, max_features = n_features)
    vectorizer = TfidfVectorizer(analyzer = "word", tokenizer = None, stop_words = None, max_features = n_features)
    features = vectorizer.fit_transform(news_text[fieldname])
    features = features.toarray()
    return features
