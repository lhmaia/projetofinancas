#!/usr/bin/env python3
import ler_dados as ld
import pre_processar as pp

def get_entradas_svm():
    
    acoes = ld.carrega_candles()
    
    newspp_ordenado = pp.ordena_por_datahora(newspp, 'text', 'date')
    
    alvo = pp.get_target(newspp_ordenado, acoes[0].candles)
    
    news_features = pp.extrai_features(newspp_ordenado, 'text')
    
    input_svm = pp.get_entrada(news_features, alvo)
    
    return input_svm



