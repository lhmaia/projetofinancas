#!/usr/bin/python
from acao import Acao, Candle
from datetime import datetime
from matplotlib import pyplot as plt

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

inicial = datetime.strptime('20000101', '%Y%m%d')
final = datetime.strptime('20150101', '%Y%m%d')
#acoes[0].plotar(inicial, final)


x=[]
y=[]
ultimo = datetime.strptime('1800', '%H%M')

for candle in acoes[3].candles:
    if candle.datahora >= inicial and candle.datahora <= final:# and candle.datahora.time() == ultimo.time():
        #print str(candle.datahora) + ': ' + str(candle.fechamento_atual)
        x.append(candle.datahora)
        y.append(candle.fechamento_atual)

plt.ylabel(acao.codigo)
plt.plot(x, y)
#plt.show()


d = open('data.txt')
f = open('teste.txt')

t = []
s = []

anterior = 0

for i in range(0,2118):
    auxX = d.readline()
    auxY = f.readline()
    auxY = float(auxY[:-1])
    dt = datetime.strptime(auxX[:-1],'%d/%m/%Y')
    if dt >= inicial and dt <= final:
        #print auxX[:-1] + ': ' + auxY[:-1]
        t.append(dt)
        if auxY == 0:
            auxY = anterior
        else:
            auxY = auxY - 6
        anterior = auxY
        s.append(auxY)

'''
for linha in d:
    #print datetime.strptime(linha[:-1],'%d/%m/%Y')
    dt = datetime.strptime(linha[:-1],'%d/%m/%Y')
    if dt >= inicial and dt <= final:
        t.append(dt)


for linha in f:
    if linha[:-1] == '0':
        linha = anterior

    anterior = linha
    s.append(linha)
'''
plt.plot(t,s)
plt.show()


f.close()
