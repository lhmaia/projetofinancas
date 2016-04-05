f = open('20150725_candles_ibov_15min_10campos_comCabecalho.txt', 'r')

acoes = []

#descarta cabecalho
f.readline()

for linha in f:
    acao = linha[0: linha.find(',')]
    if not acao in acoes:
        acoes.append(acao)

acoes.sort()
print 'Numero de acoes: ' + str(len(acoes))

for acao in acoes:
    print acao

f.close()
