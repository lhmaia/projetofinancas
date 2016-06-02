#codigo,fechamento_atual,abertura,maximo,minimo,fechamento_anterior,negocios,quantidade_papeis,volume_financeiro,datahora

from datetime import datetime
from matplotlib import pyplot as plt

class Candle:
    '''classe contendo os valores de um candle'''

    def __init__(self):
        self.fechamento_atual = 0.0
        self.abertura = 0.0
        self.maximo = 0.0
        self.minimo = 0.0
        self.fechamento_anterior = 0.0
        self.negocios = 0
        self.quantidade_papeis = 0
        self.volume_financeiro = 0.0
        self.datahora = None

    def __str__(self):
        return str(self.fechamento_atual) + ',' + str(self.abertura) + ',' +  str(self.maximo) + ',' + str(self.minimo) + ',' + str(self.fechamento_anterior) + ',' + str(self.negocios) + ',' + str(self.quantidade_papeis) + ',' + str(self.volume_financeiro) + ',' + str(self.datahora) 

class Acao:
    '''classe representando uma acao '''
        
    def __init__(self, codigo):
        self.codigo = codigo
        self.candles = []

    def __eq__(self, other):
        return self.codigo == other.codigo

    def plotar(self, data_inicial = None, data_final = None):
        x = []
        y = []
        if data_inicial is None:
            data_inicial = datetime.strptime('19000101', '%Y%m%d')
        if data_final is None:
            data_final = datetime.strptime('21000101', '%Y%m%d')


        for candle in self.candles:
            if candle.datahora >= data_inicial and candle.datahora <= data_final:
                x.append(candle.datahora)
                y.append(candle.fechamento_atual)
        plt.ylabel(self.codigo)
        plt.plot(x, y)
        plt.show()
        
    def get_candles_dict(self):
        candledict = []
        for candle in self.candles:
            d = {
                'open': float(candle.abertura),
                'high': float(candle.maximo),
                'low': float(candle.minimo),
                'close': float(candle.fechamento_atual),
                'volume': float(candle.volume_financeiro)
            }
            candledict.append(d)
        return candledict

def carrega_candles(nome_acao):
    #f = open('../Dados/dadosTrabalho.txt', 'r')
    f = open('../Dados/20150725_candles_ibov_15min_10campos_comCabecalho.txt', 'r')
    
    #descarta cabecalho
    f.readline()
    
    a = Acao(nome_acao)
    
    for linha in f:
        if nome_acao in linha:
            tmp = linha.split(',')
            
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
            a.candles.append(c)
    
    f.close()
    
    return a