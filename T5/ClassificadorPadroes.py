# -*- coding: utf-8 -*-
"""
Implementacao do classificador Bayesiano sob hipotese Gaussiana e do
classificador KNN, calculando sua taxa de erro
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""
import random
import math
import operator
import csv
import numpy as np


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
    return conjTreino, conjTeste
    
def dividePorClasse(dataset, atributoClasse):
    #Cria um conjunto onde ficarao as classes divididas
    divisaoClasses = {}
    #Variavel onde se armazena o numero de classes possiveis para controle da matriz de covariancia e da media
    nroClassesPossiveis = 0
    for i in range(len(dataset)):
        #guarda a instancia
        instancia = dataset[i]
        #Encontrou classe nova, cria um indice para ela
        if (instancia[atributoClasse] not in divisaoClasses):
            divisaoClasses[instancia[atributoClasse]] = []
            nroClassesPossiveis += 1
        divisaoClasses[instancia[atributoClasse]].append(instancia)
    return divisaoClasses, nroClassesPossiveis

def calculoMatrizCovarianciaMedia(divisaoClassesTeste, nroClassesPossiveis):
    matrizCovariancia = []
    #O vetor de media eh inicializado com seu tamanho certo, ou seja,
    #possui a altura do numero de classes possiveis e a largura do numero de atributos
    media = [[0 for y in range(len(divisaoClassesTeste[0][0]))] for x in range(nroClassesPossiveis)] 
    for i in divisaoClassesTeste:
        matrizCovariancia.append(np.cov(divisaoClassesTeste[i]))
        #Percorre cada atributo
        for j in range((len(divisaoClassesTeste[i][0]))):
            mediaAtributo = 0
            #Para cada instancia daquela classe, soma na media o valor daquele atributo
            for k in range((len(divisaoClassesTeste[i]))):
                mediaAtributo += (1/len(divisaoClassesTeste[i])) * divisaoClassesTeste[i][k][j]
            media[i][j] = mediaAtributo
    return matrizCovariancia, media

def ClassificadorBayesiano(dados, atributoClasse):
    #Divide o conjunto de dados passado como parametro
    conjTreino, conjTeste = divideDataset(dados, 0.5)
    #Classe eh o ultimo atributo, portanto passa como parametro -1
    divisaoClassesTreino, nroClassesPossiveis = dividePorClasse(conjTreino, atributoClasse)
    #Realiza o calculo da matriz de covariancia e da media dos atributos por classe
    matrizCovariancia, media = calculoMatrizCovarianciaMedia(divisaoClassesTreino, nroClassesPossiveis)
    #Inicializa um vetor onde sera armazenado as classificacoes
    classificacao = [0 for x in range(len(conjTreino))] 
    #Classifica conforme o conjunto teste
    for x in range(len(conjTreino)):
        #Lima variavel de apoio
        maiorDiscriminante = float('-inf')
        for j in range(nroClassesPossiveis): 
            #Calculo do discriminante, sendo:
            #np.log sendo o ln
            #np.transpose a transposta da matriz
            #np.subtract a subtracao entre duas matrizes
            #np.linalg.inv a inversa de uma matriz
            discriminante = np.log(1/nroClassesPossiveis) - (0.5 * np.log(matrizCovariancia[j])) - (0.5 * np.transpose(np.subtract(conjTreino[x], media[j])) * np.linalg.inv(matrizCovariancia[j]) * (np.subtract(x, media[j])))
            #Atualiza o maior discriminante, preenchendo a classe a qual ela pertence           
            if (discriminante > maiorDiscriminante):
                maiorDiscriminante = discriminante
                maiorClasse = conjTreino[x][atributoClasse]
        #Apos obter a maior classe, atualiza no vetor de classificacao 
        classificacao[x] = maiorClasse
    #calcula a precisão de acertos
    precisao = getPrecisao(conjTreino, classificacao)
    print('Precisão Classificador Bayesiano sob hipotese Gaussiana: ' + repr(precisao))

#calcula a distancia euclidiana para 2 objetos de 'tamanho' atributos
def distanciaEuclidiana(obj1, obj2, tamanho):
    distancia = 0
    for x in range(tamanho):
        distancia += pow((obj1[x] - obj2[x]), 2)
    return math.sqrt(distancia)
 
#retorna os vizinhos mais proximos
def getVizinhos(conjTreino, conjTeste, k):
    distancias = []
    tamanho = len(conjTeste)-1
    #percorre todos os itens do conjunto de treino
    for x in range(len(conjTreino)):
        dist = distanciaEuclidiana(conjTeste, conjTreino[x], tamanho)
        distancias.append((conjTreino[x], dist))
        #ordena de acordo com as distancias
    distancias.sort(key=operator.itemgetter(1))
    vizinhos = []
    for x in range(k):
        vizinhos.append(distancias[x][0])
    return vizinhos
 
#depois de obter os k vizinhos mais próximos, temos que olhar as classes deles
#e predizer a classe do dado
def getResposta(vizinhos):
    qtdClasse = {}
    #para cada vizinho encontrado
    for x in range(len(vizinhos)):
        #vê qual é a classe do vizinho
        resposta = vizinhos[x][-1]
        #se a classe ja esta em classVotes, acrescenta um ponto para essa classe
        #ou seja, ganhará a classe que tiver mais representantes como vizinho mais proximo
        if resposta in qtdClasse:
            qtdClasse[resposta] += 1
        else:
            qtdClasse[resposta] = 1
    #ordena as classes por quantidade de votos recebidas.
    sortedVotes = sorted(qtdClasse.items(), key=operator.itemgetter(1), reverse=True)
    #retorna como classe a classe que tem a maioria dos vizinhos da classe
    return sortedVotes[0][0]

#recebe o conjunto de teste a predição das classes que ele retornou com KNN
def getPrecisao(conjTeste, classePredita):
    predicoesCorretas = 0
    tamanhoConjTeste = len(conjTeste)
    #para cada dado no conjunto de teste
    for x in range(tamanhoConjTeste):
        #verifica se a classe do dado é realmente a classe predita
        if conjTeste[x][-1] == classePredita[x]:
            #se sim, incrementa o numero de precisoes corretas
            predicoesCorretas += 1
    #fal o cálculo da previsao = porcentagem de acertos
    precisao= (predicoesCorretas/float(tamanhoConjTeste)) * 100.0
    return precisao

def ClassificadorKNN(dados,k):
    #separa os dados entre conjunto de treino e conjunto de teste
    conjTreino,conjTeste=divideDataset(dados,0.5)
    #lista de predições, servirá para armazenar a classe predita e a classe real
    predicoes=[]
    #armazena o tamanho do conjunto de teste de acordo com a proporção
    tamanhoConjTeste = len(conjTeste)
    #para cada dado no conjunto de teste
    for x in range(tamanhoConjTeste):
        #obtenho os vizinhos mais próximos
        vizinhos = getVizinhos(conjTreino, conjTeste[x], k)
        #pego as respostas
        resultado = getResposta(vizinhos)
        #e adiciono na lista de predições a classe que foi escolhida para o dado para
        #depois comparar com a classe real que o dado pertence
        predicoes.append(resultado)
        print('classe predita=' + repr(resultado) + ', classe real=' + repr(conjTeste[x][-1]))
    #calcula a precisão de acertos
    precisao = getPrecisao(conjTeste, predicoes)
    print('Precisão  KNN: ' + repr(precisao) + '% para k='+repr(k))
    
#Abre o conjunto de dados 
with open('dados_multivariados/4-diabetes/pima-indians-diabetes.data', 'rt') as csvfile:
    #faz a leitura do arquivo, indicando que ele é delimitado por ','
    reader = csv.reader(csvfile,delimiter=',')
    #converte as colunas para seus respectivos dados de acordo com o dataset
    dataset = [(int(col1),int(col2),int(col3),int(col4),int(col5),float(col6),float(col7),int(col8),int(col9)) for col1,col2,col3,col4,col5,col6,col7,col8,col9 in reader]
#chama classificador Knn com k=11
ClassificadorKNN(dataset,11)
#chama o classificador Bayesiano, passando como parametro o atributo da classe
ClassificadorBayesiano(dataset, -1)
#base: http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
#Depois monto os creditos direitinho