#codigo,fechamento_atual,abertura,maximo,minimo,fechamento_anterior,negocios,quantidade_papeis,volume_financeiro,datahora

import pandas as pd
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
        
    def plotar_previsoes(self, nome_teste, nome_pred, data_inicial = None, data_final = None):
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
        
        pred = pd.read_csv('dados/'+ nome_teste, delimiter=' ', usecols=[0, 1], header=None, names=['alvo', 'preco'])
        out = pd.read_csv('dados/'+ nome_pred, delimiter=' ', usecols=[0], header=None, names=['resultado'])
        datahora = pd.read_csv('dados/' + nome_teste + '.date', delimiter=';', usecols=[0, 1], header=None, names=['datahora', 'precoalvo'])
        out_datahora = open('dados/' + nome_pred + '.datahora', 'w')
                
        errosx = []
        errosy = []
        acertosx = []
        acertosy = []
        out_datahora.write('datahora;preco;alvo;resultado\n')
        for i in range(0, len(pred)):
            out_datahora.write(datahora['datahora'][i] + ';' + pred['preco'][i][2:] + ';' + str(datahora['precoalvo'][i]) + ';' +  str(pred['alvo'][i]) + ';' + str(out['resultado'][i]) + '\n')
            if pred['alvo'][i] == out['resultado'][i]:
                acertosx.append(datahora['datahora'][i])
                acertosy.append(float(pred['preco'][i][2:]))
            else:
                errosx.append(datahora['datahora'][i])
                errosy.append(float(pred['preco'][i][2:]))
                
        out_datahora.close()
        
        plt.plot(x, y)
        plt.plot(errosx, errosy, 'rx')
        plt.plot(acertosx, acertosy, 'gx')
        plt.savefig('dados/' + nome_pred + '.png')
        plt.close('all')
    
        
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
    #f = open('../Dados/20150725_candles_ibov_15min_10campos_comCabecalho.txt', 'r')
    #f = open('../Dados/petr4diario.txt', 'r')
    f = open('../Dados/candles_15m_2016.txt', 'r')
    
    #descarta cabecalho
    f.readline()
    
    a = Acao(nome_acao)
    
    for linha in f:
        if nome_acao.upper() in linha:
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