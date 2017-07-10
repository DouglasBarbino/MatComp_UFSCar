# -*- coding: utf-8 -*-
"""
Implementacao do classificador Bayesiano sob hipótese Gaussiana e do
classificador KNN, calculando sua taxa de erro
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""
import random

def divideDataset(dataset, taxaAprendizado):
    #Calcula o tamanho que deve ficar o conjunto de treinamento
    tamanhoConjTeste = int(len(dataset) * taxaAprendizado)
    conjTeste = []
    #No inicio todo o conjunto de dados vai para o conjunto de treino, depois 
    #que a porcentagem de instancias pedidas vao para o conjunto de teste
    conjTreino = list(dataset)
    while len(conjTeste) < tamanhoConjTeste:
        #Seleciona aleatoriamente uma instancia do conjunto de treino
        index = random.randint(0, len(conjTreino)-1)
        #Remove a instancia escolhida do conjunto de treino e o passa pro conjunto de teste
        conjTeste.append(conjTreino.pop(index))
    return [conjTreino, conjTeste]
    
def dividePorClasse(dataset, atributoClasse):
    #Cria um conjunto onde ficarao as classes divididas
    divisaoClasses = {}
    #Cria um vetor para armazenar os possiveis valores de classes
    classesPossiveis = []
    for i in range(len(dataset)):
        #guarda a instancia
        instancia = dataset[i]
        #Encontrou classe nova, cria um indice para ela e a coloca no vetor de classes possiveis
        if (instancia[atributoClasse] not in divisaoClasses):
            divisaoClasses[instancia[atributoClasse]] = []
            classesPossiveis.append(instancia[atributoClasse])
        divisaoClasses[instancia[atributoClasse]].append(instancia)
    return divisaoClasses, classesPossiveis

def ClassificadorBayesiano(dados):
    #Divide o conjunto de dados passado como parametro
    conjTeste, conjTreino = divideDataset(dados, 0.5)
    #-2 pois ele conta o /n como atributo...
    divisaoClassesTeste, classesPossiveis = dividePorClasse(conjTeste, -2)
    print(divisaoClassesTeste)
    print(classesPossiveis)
    return
    
def ClassificadorKNN():
    return 
    
#Carrega um dos conjuntos de dados
conjunto1 = open('dados_multivariados/4-diabetes/pima-indians-diabetes.data', 'r')
#Todo o texto do arquivo eh transformado em matriz
dados1 = list(conjunto1)
conjunto1.close()
ClassificadorBayesiano(dados1)
#base: http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
#Depois monto os creditos direitinho