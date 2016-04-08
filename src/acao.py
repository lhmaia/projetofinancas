#codigo,fechamento_atual,abertura,maximo,minimo,fechamento_anterior,negocios,quantidade_papeis,volume_financeiro,datahora
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


