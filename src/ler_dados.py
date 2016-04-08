#!/usr/bin/python
from acao import Acao, Candle
from datetime import datetime

#f = open('../Dados/20150725_candles_ibov_15min_10campos_comCabecalho.txt', 'r')
f = open('../Dados/dadosTrabalho.txt', 'r')

acoes = []

#descarta cabecalho
f.readline()

for linha in f:
    tmp = linha.split(',') #[0: linha.find(',')]
    a = Acao(tmp[0])
    
    c = Candle()
    c.fechamento_atual = tmp[1]
    c.abertura = tmp[2]
    c.maximo = tmp[3]
    c.minimo = tmp[4]
    c.fechamento_anterior = tmp[5]
    c.negocios = tmp[6]
    c.quantidade_papeis = tmp[7]
    c.volume_financeiro = tmp[8]
    c.datahora = datetime.strptime(tmp[9][:-1], '%Y%m%d%H%M')


    if not a in acoes:
        acoes.append(a)
        acoes[acoes.index(a)].candles.append(c)
    else:
        acoes[acoes.index(a)].candles.append(c)


print 'Numero de acoes: ' + str(len(acoes))

#acoes.sort(cmp=lambda x,y: cmp(x.codigo, y.codigo))

for acao in acoes:
    print acao.codigo + ', numero de candles: ' + str(len(acao.candles))

for i in range(20):
    print acoes[0].candles[i]

f.close()
