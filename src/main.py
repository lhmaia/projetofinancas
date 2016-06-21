#!/usr/bin/env python3
import pre_processar as pp
import acao
import pandas as pd
import talib
from sklearn import preprocessing

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

def get_entradas_svm():
    #retorna dataframe com as entradas, utilizar pp.gera_arquivo para gerar arquivo para libsvm
    nome_ativo = 'PETR4'
    
    acoes = acao.carrega_candles(nome_ativo)
    
    newspp = pp.pre_processa(nome_ativo)
    
    newspp_ordenado = pp.ordena_por_datahora(newspp, 'text', 'date')
    
    alvo = pp.get_target(newspp_ordenado, acoes.candles)
    
    news_features = pp.extrai_features(newspp_ordenado, 'text')
    
    input_svm = pp.get_entrada(news_features, alvo)
    
    return input_svm

def get_entradas_svm_indicadores():
    #retorna dataframe com as entradas, utilizar pp.gera_arquivo para gerar arquivo para libsvm
    
    acoes = acao.carrega_candles('PETR4')
    
    #newspp = pp.pre_processa()
    
    #newspp_ordenado = pp.ordena_por_datahora(newspp, 'text', 'date')
    
    #alvo = pp.get_target(newspp_ordenado, acoes.candles)
    
    #news_features = pp.extrai_features(newspp_ordenado, 'text')
    indicadores = get_indicadores(acoes)
    
    #input_svm = pp.get_entrada(indicadores, alvo)
    
    return indicadores

def executar(nome_arquivo, percentual=60):
    input = get_entradas_svm()
    pp.gera_arquivo(input, nome_arquivo, percentual)

def executar_indicadores(nome_arquivo, percentual=60):
    input = get_entradas_svm_indicadores()
    pp.gera_arquivo_indicadores(input, nome_arquivo, percentual)