# -*- coding: utf-8 -*-
"""
Implementacao dos algoritmos de Prim e Dijkstra
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""

import networkx as nx
import numpy as np
import random as rm

def Prim (GP, raizGP):
    #Inicializacao do grafo que vai receber o MST resultante da execucao do Prim
    GrafoPrim = nx.Graph()
    #Atribuicao de todos os nos que existem no grafo original sem nenhuma aresta
    GrafoPrim.add_nodes_from(GP)
    for i in GP.nodes():
        #Atribui peso infinito para todos os nos, corrigindo depois a raiz
        GP.node[i]['peso'] = float('inf')
    GP.node[raizGP]['peso'] = 0
    #Percorre os nos para saber qual possui o menor peso
    while (GP.number_of_nodes() > 0):
        #Limpa a variavel de menor peso
        menorPeso = float('inf')
        #Verifica qual eh o vertice com menor peso, simulando a primitiva EXTRACT-MIN
        for i in GP.nodes():
            #Atualiza a tabela de menor peso
            if GP.node[i]['peso'] <= menorPeso:
                verticeMenorPeso = i
                menorPeso = GP.node[i]['peso']
        #Percorre todos os vizinhos do no com o menor peso
        for i in GP.neighbors(verticeMenorPeso):
            #Verifica se o peso da aresta eh menor que o peso armazendo ate o momento
            if GP.node[i]['peso'] > GP.get_edge_data(verticeMenorPeso,i)['weight']:
                GP.node[i]['peso'] = GP.get_edge_data(verticeMenorPeso,i)['weight']
                #Armazena o peso e o vizinho do no para que, ao final da execucao, a MST seja criada
                GrafoPrim.node[i]['peso'] = GP.get_edge_data(verticeMenorPeso,i)['weight']
                GrafoPrim.node[i]['vizinho'] = verticeMenorPeso
        #Remove o vertice do menor peso
        GP.remove_node(verticeMenorPeso)
    #Atribuicao das arestas escolhidas para compor a MST no grafo que estah apenas com os nos
    for i in GrafoPrim.nodes():
        #Raiz nao eh adicionada pois ela nao tem vizinho armazenado
        if (i != raizGP):            
            GrafoPrim.add_edge(i, GrafoPrim.node[i]['vizinho'], weight=GrafoPrim.node[i]['peso'])
    return GrafoPrim

def Dijkstra(G, raiz):
    #Grafo que representará a MST gerada por Dijkstra
    GrafoDijkstra = nx.Graph() 
    # Inicialização do custoAtual(v) e predecessores(v)
    #Cada nó (!= raiz) começa com custo atual = infinito e nenhum predecessor
    for node in G.nodes():
        G.node[node]['custoAtual'] = float('inf')
        G.node[node]['predecessor'] = None
   #Agora consertando a raiz para custoAtual = 0
    G.node[raiz]['custoAtual'] = 0
   
    #Fila de Prioridades (menor distancia > prioridade)
    Q = [] 
    #Armazena os nós que já foram visitados e sairam da fila
    nosVisitados = [] 

    #Colocando todos os nós na fila (nenhum foi visitado ainda)
    for node in G.nodes():
        Q.append((G.node[node]['custoAtual'], node))
    
    #Enquanto a fila não for vazia
    #Execução do Algoritmo de Dijkstra
    while len(Q) != 0:
        #Ordena a fila, pois é uma fila de prioridades
        #A fila será ordenada pelo custoAtual
        Q.sort() 
        #Retira o elemento de menor custoAtual, ou seja, o primeiro da fila
        u = Q.pop(0)
        #Como o nó foi removido e colocado em u, temos q pegar o nó que está em u[1] (u[0] contém o custo)
        u = u[1] 
        #Coloca o nó u (nó atual) na lista de nósVisitados
        nosVisitados.append(u) 

        #Agora, os vizinhos do nó atual(u) são verificados para fazer o relaxamento das arestas
        #Ou seja, calcula o custo da raiz até u
        for node in G.neighbors(u):
            #Se o nó vizinho não está em visitados e se o custoAtual dele é maior que o custo do nó atual + o peso dele
            if ((not node in nosVisitados) and (G.node[node]['custoAtual'] > G.get_edge_data(u,node)['weight'] + G.node[u]['custoAtual'])):
                #então significa que o melhor caminho da raiz até o no foi encontrado
                #remove ele de Q
                Q.remove((G.node[node]['custoAtual'], node))
                #atualiza o custo atual
                G.node[node]['custoAtual'] = G.node[u]['custoAtual']+G[u][node]['weight']
                #coloca o nó atualizado de volta na fila
                Q.append((G.node[node]['custoAtual'], node))
                #marca o no vizinho com o nó atual sendo seu predecessor
                G.node[node]['predecessor'] = u

    
    #Depois do loop e calculo dos custos atuais, adiciona-se os nós no grafo MST
    for u in G.nodes():
        GrafoDijkstra.add_node(u)
        if G.node[u]['predecessor'] is not None:
            GrafoDijkstra.add_edge(u, G.node[u]['predecessor'])
            GrafoDijkstra[u][G.node[u]['predecessor']]['weight'] = G[u][G.node[u]['predecessor']]['weight']

    return GrafoDijkstra
    
    
#Leitura de um grafo por meio de uma lista de arestas
GP = nx.read_edgelist('women.txt', nodetype=int, data=(('weight',float),))

#Define um vertice inicial aleatorio
vertices = GP.nodes()
raizGP = vertices[rm.randint(0,GP.number_of_nodes()-1)]
#Chama o algoritmo de Prim. 
#Note que nao eh passada a lista de pesos das arestas como no algoritmo 
#original, pois ela eh facilmente obtida por GP.get_edge_data(v1, v2)['weight']
MSTPrim = Prim(GP, raizGP)
print("-------------PRIM-----------------")
print(MSTPrim.nodes())
print(MSTPrim.edges(data = True))

#Lendo o mesmo grafo para Dijkstra através da lista de arestas
GD = nx.read_edgelist('women.txt', nodetype=int, data=(('weight',float),))
vertices = GD.nodes()
#Pegando a mesma raiz usada em Prim
raizGD = raizGP

print("-------------DIJKSTRA-----------------")
MSTDijkstra = Dijkstra(GD, raizGD)
print(MSTDijkstra.nodes())
print(MSTDijkstra.edges(data=True))

#Leitura de um grafo por meio de uma matriz de adjacencia
MAdj = np.loadtxt('cidades.txt')
GD = nx.from_numpy_matrix(MAdj)