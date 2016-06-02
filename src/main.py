#!/usr/bin/env python3
import pre_processar as pp
import acao
import pandas as pd
import talib

def get_indicadores(acao):
    candles = acao.get_candles_dict()
    cpd = pd.DataFrame.from_dict(candles, dtype='f8')
    close = cpd.close.values
    
    alvo = []
    for v in range(1, len(close)):
        if close[v] > close[v -1]:
            alvo.append(1)
        if close[v] <= close[v -1]:
            alvo.append(0)
        
    alvo.append(alvo[len(alvo) - 1])
    
    sma = talib.SMA(close)
    macd = talib.MACD(close)
    bbands = talib.BBANDS(close)
    ifr = talib.RSI(close)
        
    indicadores = pd.DataFrame()
    indicadores['alvo'] = alvo
    indicadores['preco'] = close
    indicadores['sma'] = sma
    #indicadores['macd'] = macd
    #indicadores['bbands'] = bbands
    indicadores['ifr'] = ifr
    
    return indicadores

def get_entradas_svm():
    #retorna dataframe com as entradas, utilizar pp.gera_arquivo para gerar arquivo para libsvm
    
    acoes = acao.carrega_candles('PETR4')
    
    newspp = pp.pre_processa()
    
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