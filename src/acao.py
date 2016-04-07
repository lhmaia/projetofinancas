#codigo,fechamento_atual,abertura,maximo,minimo,fechamento_anterior,negocios,quantidade_papeis,volume_financeiro,datahora
class Candle:
    '''classe contendo os valores de um candle'''
    fechamento_atual = 0.0
    abertura = 0.0
    maximo = 0.0
    minimo = 0.0
    fechamento_anterior = 0.0
    negocios = 0
    quantidade_papeis = 0
    volume_financeiro = 0.0
    datahora = None


class Acao:
    '''classe representando uma acao '''
    codigo = ''
    candles = []
    def __init__(self, codigo):
        self.codigo = codigo

    def __eq__(self, other):
        return self.codigo == other.codigo


