#Algoritmo de Ford Fulkerson para obter o fluxo máximo em redes

#realiza a busca em profundidade no grafo para encontrar todos os caminhos possiveis de 
# S à T
#retorna os caminhos encontrados de S à T
def dfs(C, F, s, t):
        #adiciona s na pilha
        pilha = [s]
        #implementa um dicionario (vertice[verticeanterior,vertice]), ou seja o caminho usado para chegar até ele
        caminhos={s:[]}
        # se o s for igual a t, só é possivel um caminho (s)
        if s == t:
            return caminhos[s]
        #enquanto tiver elementos na pilha
        while(pilha):
                #retira o ultimo vertice adicionado (ultimo descoberto)
                u = pilha.pop()
                #encontra os vizinhos do vertice u retirado da pilha e para cada um deles
                for v in range(len(C)):
                    #verifica se a capacidade-fluxo é maior que 0
                    #e se o vizinho v não está em caminhos
                    if(C[u][v]-F[u][v]>0) and v not in caminhos:
                        #se isso for satisfeito, cria-se um caminho para v onde se adiciona o
                        #caminho de u e u,v
                        caminhos[v] = caminhos[u]+[(u,v)]
                        #se o vizinho é t (chegamos ao destino)
                        if v == t:
                            #retorna o caminho encontrado de s à t
                            return caminhos[v]
                        #coloca o vizinho v na pilha para explorar seus vizinhos
                        pilha.append(v)
        #se não tem mais nenhum elemento descoberto
        return None
#C = matriz de capacidade, S= SAÍDA , D=DESTINO
def max_flow(Graph, s, t):
        n = len(Graph)
        #atribui o fluxo para cada nó como 0 inicialmente
        for i in range(n):
            F = [[0] * n for i in range(n)]
        #procura um caminho
        caminho = dfs(Graph, F, s, t)
        print("Caminhos Encontrados de S à T")
        #enquanto encontrar um caminho possivel
        while caminho != None:
            print(caminho)
            #Procura a capacidade residual mínima das arestas ao longo
            #do caminho encontrado por DFS. Ou seja, procura o fluxo máximo
            #atraves do caminho encontrado
            fluxo = min(Graph[u][v] - F[u][v] for u,v in caminho)
            print("Fluxo Máximo",fluxo)
            #para cada aresta u,v no caminho, atualiza as capacidades residuais
            for u,v in caminho:
                F[u][v] += fluxo #adiciona o fluxo da arestas
                F[v][u] -= fluxo #decrementa o fluxo das arestas reversas
            #busca um outro caminho possivel    
            caminho = dfs(Graph,F,s,t)
            
        soma=0
        for i in range(n):
            print('F[',s,'][',i,']=',F[s][i])
            soma+=F[s][i]
        #retorna a soma dos fluxos das arestas
        return soma
    
#Matriz de Capacidades
Graph = [[0, 16, 13, 0, 0, 0], 
     [0, 0, 10, 12, 0, 0], 
     [0, 4, 0, 0, 14, 0], 
     [0, 0, 9, 0, 0, 20], 
     [0, 0, 0, 7, 0, 4], 
     [0, 0, 0, 0, 0, 0]] 

source = 0  
sink = 5
max_flow_value = max_flow(Graph, source, sink)
print ("Algoritmo de Ford-Fulkerson")
print ("O fluxo máximo encontrado é: ", max_flow_value)