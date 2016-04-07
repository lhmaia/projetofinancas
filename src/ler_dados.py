#!/usr/bin/python
from acao import Acao, Candle

f = open('../Dados/20150725_candles_ibov_15min_10campos_comCabecalho.txt', 'r')

acoes = []

#descarta cabecalho
f.readline()

for linha in f:
    acao = linha[0: linha.find(',')]
    a = Acao(acao)
    if not a in acoes:
        acoes.append(a)

print 'Numero de acoes: ' + str(len(acoes))

acoes.sort(cmp=lambda x,y: cmp(x.codigo, y.codigo))

for acao in acoes:
    print acao.codigo

f.close()
