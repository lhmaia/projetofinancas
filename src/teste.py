#!/usr/bin/python
from datetime import datetime
from matplotlib import pyplot as plt

d = open('data.txt')
f = open('teste.txt')

x = []
y = []

for linha in d:
    #print datetime.strptime(linha[:-1],'%d/%m/%Y')
    x.append(datetime.strptime(linha[:-1],'%d/%m/%Y'))

for linha in f:
    y.append(linha)

print len(x)
print len(y)

plt.plot(x,y)
plt.show()
