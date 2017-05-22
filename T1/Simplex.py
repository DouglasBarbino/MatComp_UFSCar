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
#note que no ultimo valor tambem se separa o resultado da resolucao, sendo que no momento
#apenas equacoes com menor ou igual estao sendo aceitas, pois elas fazem parte da forma canonica
restricoes = restricoes.split(';')
#print(restricoes)
for i in range(numeroRestricoes):
   restricoes[i] = restricoes[i].split(',')
   restricoes[i][numeroVariaveis-1] = restricoes[i][numeroVariaveis-1].split('<=')
   #print(restricoes[i])
#print(restricoes[0][2][1])
#le a quarta linha que contem a funcao objetivo
linha = ppl.readline()
#Separa do primeiro colchete para frente, removendo o colchete do final tambem
#Note que nao estah sendo feita a verificacao se de fato eh uma funcao de maximizacao, 
#no momento serah assumido que todas as funcoes objetivo buscam maximizar 
objetivo = linha[9:].replace(']', '')
#Separa o coeficiente de cada variavel
objetivo = objetivo.split(',')
#print(objetivo)
#Criacao da matriz ja preenchida por 0 onde serah resolvido o PPL. Composto por:
#- Indice x: Numero de restricoes + Funcao objetivo
#- Indice y: Numero de variaveis + numero de resticoes (pois cada uma cria uma variavel a mais) + Constante
matrizResolucao = [[0 for y in range(numeroRestricoes+numeroVariaveis+1)] for x in range(numeroRestricoes+1)] 
#print(matrizResolucao[3][6])
#Insere as constantes da funcao objetivo na matriz já invertidas
for i in range(numeroVariaveis):
    matrizResolucao[0][i] = int(objetivo[i]) * -1
#print(matrizResolucao[0][2])
#Insere as constantes das restricoes na matriz
for i in range(1, numeroRestricoes+1):
    for j in range(numeroVariaveis):
        #Verifica se atingiu o ultimo valor da restricao
        if (j != (numeroVariaveis-1)):
            matrizResolucao[i][j] = int(restricoes[i-1][j])
        else:
            #Caso atingiu, eh necessario tambem coletar a constante da restricao
            matrizResolucao[i][j], matrizResolucao[i][numeroVariaveis+numeroRestricoes] = int(restricoes[i-1][j][0]), int(restricoes[i-1][j][1])
#print(matrizResolucao[0][1])
#print(matrizResolucao[1][7])
#print(matrizResolucao[2][0])
#print(matrizResolucao[4][7])
ppl.close()