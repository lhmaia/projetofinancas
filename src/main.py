#!/usr/bin/env python3
import pre_processar as pp
import acao
import pandas as pd
import talib
from sklearn import preprocessing
from subprocess import call
from datetime import datetime

def get_indicadores(acao):
    candles = acao.get_candles_dict()
    cpd = pd.DataFrame.from_dict(candles, dtype='f8')
    close = cpd.close.values
    
    alvo = []
    for v in range(1, len(close)):
        if close[v] > close[v -1]:
            alvo.append(1)
        if close[v] < close[v -1]:
            alvo.append(-1)
        if close[v] == close[v -1]:
            alvo.append(0)
        
    alvo.append(alvo[len(alvo) - 1])
    
    sma = talib.SMA(close)[29:]
    macd = talib.MACD(close)
    bbands = talib.BBANDS(close)
    ifr = talib.RSI(close)[29:]
        
    #min_max_scaler = preprocessing.MinMaxScaler()
    #sma_scaled = min_max_scaler.fit_transform(sma)
    #ifr_scaled = min_max_scaler.fit_transform(ifr)
            
    indicadores = pd.DataFrame()
    indicadores['alvo'] = alvo[29:]
    indicadores['preco'] = close[29:]
    #indicadores['sma'] = sma_scaled
    indicadores['sma'] = sma
    #indicadores['macd'] = macd
    #indicadores['bbands'] = bbands
    #indicadores['ifr'] = ifr_scaled
    indicadores['ifr'] = ifr
    
    return indicadores

def get_entradas_svm(nome_ativo, lista = None):
    #retorna dataframe com as entradas, utilizar pp.gera_arquivo para gerar arquivo para libsvm
    
    acoes = acao.carrega_candles(nome_ativo)
    
    newspp = pp.pre_processa(nome_ativo, lista)
    
    newspp_ordenado = pp.ordena_por_datahora(newspp, 'text', 'date')
    
    print("Get target ...")
    alvo = pp.get_target(newspp_ordenado, acoes.candles)
    
    news_features = pp.extrai_features(newspp_ordenado, 'text')
    
    input_svm = pp.get_entrada(news_features, alvo)
    
    return input_svm

def get_entradas_svm_indicadores(nome_ativo):
    #retorna dataframe com as entradas, utilizar pp.gera_arquivo para gerar arquivo para libsvm
    
    acoes = acao.carrega_candles(nome_ativo)
    
    #newspp = pp.pre_processa()
    
    #newspp_ordenado = pp.ordena_por_datahora(newspp, 'text', 'date')
    
    #alvo = pp.get_target(newspp_ordenado, acoes.candles)
    
    #news_features = pp.extrai_features(newspp_ordenado, 'text')
    

    
    #input_svm = pp.get_entrada(indicadores, alvo)
    
    return indicadores

def executar_ativo(nome_ativo, nome_arquivo, percentual=60, lista = None):
    input = get_entradas_svm(nome_ativo, lista)
    pp.gera_arquivo(input, nome_arquivo, percentual)
    
def executar_ativo_naive_bayes(nome_ativo):
    
    acoes = acao.carrega_candles(nome_ativo)
    
    newspp = pp.pre_processa(nome_ativo)
    
    newspp_ordenado = pp.ordena_por_datahora(newspp, 'text', 'date')
    
    alvo = pp.get_target(newspp_ordenado, acoes.candles)
    
    news_features = pp.extrai_features(newspp_ordenado, 'text')
    
    pp.executa_naive_bayes(news_features, alvo)

def executa_bloco_naive_bayes():
    ativos = pd.read_csv('../Dados/ativos.txt')
    for ativo in ativos['sigla']:
        executar_ativo_naive_bayes(ativo)
        
def executar_indicadores(nome_ativo, nome_arquivo, percentual=60):
    input = get_entradas_svm_indicadores(nome_ativo)
    pp.gera_arquivo_indicadores(input, nome_arquivo, percentual)
    
def executa_bloco(ativos):
    #ativos = pd.read_csv('../Dados/ativos.txt')
    for ativo in ativos:#['sigla']:
        nome_arquivo = ativo['sigla'] + 'news2016'
        executar_ativo(ativo['sigla'], nome_arquivo, 60, ativo['lista'])

def executa_svm_bloco(ativos):
    #ativos = pd.read_csv('../Dados/ativos.txt')
    print("Executa SVM ...")
    inicio = datetime(2016, 01, 28)
    fim = datetime(2016, 02, 10)
    for ativo in ativos:#['sigla']:
        nome_arquivo = ativo['sigla'] + 'news2016'
        call(['./executa_svm.sh', nome_arquivo])
        acoes = acao.carrega_candles(ativo['sigla'])
        acoes.plotar_previsoes(nome_arquivo + '.pred', nome_arquivo + '.out', inicio, fim)
        
def executar():
    ativos = []
    #ativos.append({'sigla': 'petr3', 'lista': [82054, 84001, 84051, 84151, 80061]})
    ativos.append({'sigla': 'petr4', 'lista': [82055, 84001, 84051, 84151, 80061]})
    ativos.append({'sigla': 'BBDC4', 'lista': [82004, 80013, 84010, 84087, 84235, 84089,84240]})
    ativos.append({'sigla': 'ITUB4', 'lista': [82038, 80045, 80046, 84010, 84087, 84235, 84089,84240, 80015]})
    ativos.append({'sigla': 'ITSA4', 'lista': [82037, 80045, 80046, 84010, 84087, 84235, 84089,84240]})
    executa_bloco(ativos)
    executa_svm_bloco(ativos)
