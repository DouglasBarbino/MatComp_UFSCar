# -*- coding: utf-8 -*-
"""
Implementacao do algoritmo Simplex para resolucao de problemas de 
programação linear na forma canonica
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""

import math

ppl = open('ppl_2.txt', 'r')
#le a primeira linha que contem o numero de variaveis na ppl
linha = ppl.readline()
#Separa apenas o numero da linha
numeroVariaveis = int(linha[5:])
#print(numeroVariaveis)
#le a segunda linha que contem a quantidade de restricoes na ppl
linha = ppl.readline()
#Separa apenas o numero
numeroRestricoes = int(linha[5:])
#print(numeroRestricoes)
#le a terceira linha que contem as restricoes da ppl
linha = ppl.readline()
#Separa do primeiro colchete para frente, removendo o colchete do final tambem
restricoes = linha[6:].replace(']', '')
#Separa as restricoes, marcadas por ponto e virgula, e tambem cada numero, unidos por virgula
#note que o ultimo valor tambem armazena o resultado da restricao, o que serah tratado depois
restricoes = restricoes.split(';')
print(restricoes)
for i in range(numeroRestricoes):
   restricoes[i] = restricoes[i].split(',')
   print(restricoes[i])
#print(restricoes)
#print(linha)
ppl.close()