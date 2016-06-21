import pandas as pd
from matplotlib import pyplot as plt

def gera(nome_teste, nome_pred):
    pred = pd.read_csv('dados/'+ nome_teste, delimiter=' ', usecols=[0, 1], header=None, names=['alvo', 'preco'])
    out = pd.read_csv('dados/'+ nome_pred, delimiter=' ', usecols=[0], header=None, names=['resultado'])
    
    print len(pred)
    print len(out)
    
    errosx = []
    errosy = []
    acertosx = []
    acertosy = []
    precosx = []
    precosy = []
    for i in range(0, len(pred)):
        precosx.append(i)
        precosy.append(float(pred['preco'][i][2:]))
        if pred['alvo'][i] == out['resultado'][i]:
            acertosx.append(i)
            acertosy.append(float(pred['preco'][i][2:]))
        else:
            errosx.append(i)
            errosy.append(float(pred['preco'][i][2:]))
            

    plt.plot(precosx, precosy)
    plt.plot(errosx, errosy, 'rx')
    plt.plot(acertosx, acertosy, 'x')
    plt.show()

