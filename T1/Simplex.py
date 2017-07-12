# -*- coding: utf-8 -*-
"""
Implementacao do algoritmo Simplex para resolucao de problemas de 
programação linear na forma canonica
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""
#Le o arquivo com o formato gerado pelo site http://www.cos.ufrj.br/splint/
ppl = open('ppl_3.txt', 'r')
#le a primeira linha que contem o numero de variaveis na ppl
linha = ppl.readline()
#Separa apenas o numero da linha
numeroVariaveis = int(linha[5:])
#le a segunda linha que contem a quantidade de restricoes na ppl
linha = ppl.readline()
#Separa apenas o numero
numeroRestricoes = int(linha[5:])
#le a terceira linha que contem as restricoes da ppl
linha = ppl.readline()
#Separa do primeiro colchete para frente, removendo o colchete do final tambem
restricoes = linha[6:].replace(']', '')
#Separa as restricoes, marcadas por ponto e virgula, e tambem cada numero, unidos por virgula
#note que no ultimo valor tambem se separa o resultado da resolucao, sendo que no momento
#apenas equacoes com menor ou igual estao sendo aceitas, pois elas fazem parte da forma canonica
restricoes = restricoes.split(';')
for i in range(numeroRestricoes):
   restricoes[i] = restricoes[i].split(',')
   restricoes[i][numeroVariaveis-1] = restricoes[i][numeroVariaveis-1].split('<=')
#le a quarta linha que contem a funcao objetivo
linha = ppl.readline()
#Separa do primeiro colchete para frente, removendo o colchete do final tambem
#Note que nao estah sendo feita a verificacao se de fato eh uma funcao de maximizacao, 
#no momento serah assumido que todas as funcoes objetivo buscam maximizar 
objetivo = linha[9:].replace(']', '')
#Separa o coeficiente de cada variavel
objetivo = objetivo.split(',')
#Fecha o arquivo, pois ele nao sera mais necessario
ppl.close()
#Criacao da matriz ja preenchida por 0 onde serah resolvido o PPL. Composto por:
#- Indice x: Numero de restricoes + Funcao objetivo
#- Indice y: Numero de variaveis + numero de resticoes (pois cada uma cria uma variavel a mais)
matrizResolucao = [[0 for y in range(numeroRestricoes+numeroVariaveis)] for x in range(numeroRestricoes+1)] 
#Criacao do vetor que armazena os resultados de cada equacao ou restricao da matriz,
#sendo que ela nao ficara na matriz para facilitar nos calculos
constante = [0 for x in range(numeroRestricoes+1)] 
#Criacao do vetor relacionado com constante[], armazenando a qual variavel eh aquele valor
variaveis = ["" for x in range(numeroRestricoes+1)]
#O primeiro sempre eh o resultado da funcao objetivo
variaveis[0] = "z"
#Insere as constantes, ja invertidas, da funcao objetivo na matriz
for i in range(numeroVariaveis):
    matrizResolucao[0][i] = int(objetivo[i]) * -1
#Insere as constantes das restricoes na matriz
for i in range(1, numeroRestricoes+1):
    for j in range(numeroVariaveis):
        #Verifica se atingiu o ultimo valor da restricao
        if (j != (numeroVariaveis-1)):
            matrizResolucao[i][j] = int(restricoes[i-1][j])
        else:
            #Caso atingiu, eh necessario tambem coletar a constante da restricao
            matrizResolucao[i][j], constante[i] = int(restricoes[i-1][j][0]), int(restricoes[i-1][j][1])
            #Tambem marca a variavel que aquela linha armazena o valor
            variaveis[i] = "x" + str(numeroVariaveis+i)
    #Atribui o valor 1 na coluna que corresponde a base daquela linha (a variavel criada)
    matrizResolucao[i][numeroVariaveis+i-1] = 1
#Loop onde o simplex eh resolvendo, sendo ele mantido enquanto na linha da funcao objetivo 
#possuir um valor negativo
while(min(matrizResolucao[0]) < 0):
    #Limpa a variavel razao
    razao = float('inf')
    #Armazena o indice de onde localiza-se o menor valor da funcao objetivo.
    #Note que caso haja varios numeros empatados como menor valor, sempre o primeiro indice deles sera pego
    coluna = matrizResolucao[0].index(min(matrizResolucao[0]))
    #Busca a menor razao nao negativa
    for i in range(1, numeroRestricoes+1):
        #Tratamento de erro caso ocorra uma divisao por zero
        try:
            razaoParcial = constante[i]/matrizResolucao[i][coluna]
        except ZeroDivisionError:
            razaoParcial = 0
        #Caso encontrou a menor razao e ela eh positiva nao nula, salva a linha onde ela estah 
        if ((razao > razaoParcial) and (razaoParcial > 0)):
            linha = i
            razao = razaoParcial
    #Nova linha pivo
    numeroPivo = matrizResolucao[linha][coluna]
    #Normaliza todos os valores daquela linha, tanto na matriz como na constante
    for i in range(numeroRestricoes+numeroVariaveis):
        matrizResolucao[linha][i] = matrizResolucao[linha][i] / numeroPivo
    constante[linha] = constante[linha] / numeroPivo
    #Atualiza o resto da matriz
    for i in range(numeroRestricoes+1):  
        #Verifica se a linha que sera atualizada eh a linha pivo
        if (i == linha):
            #Caso seja, apenas atualiza a variavel que ela armazena o valor
            variaveis[i] = "x" + str(coluna+1)
        else:
            #Caso nao seja, atualiza os valores da matriz e da constante
            coeficienteLinha = matrizResolucao[i][coluna] * -1
            for j in range(numeroRestricoes+numeroVariaveis):
                matrizResolucao[i][j] = matrizResolucao[i][j] + (coeficienteLinha * matrizResolucao[linha][j])
            constante[i] = constante[i] + (coeficienteLinha * constante[linha])
#Cria a string que sera impressa para o usuario contendo o resultado
stringFinal = "Solução ótima:"
for i in range(numeroRestricoes+numeroVariaveis):
    #Limpa a variavel de controle
    ehZero = True
    #Verifica se a variavel avaliada se encontra no vetor das variaveis
    for j in range(1, numeroRestricoes+1):
        if (("x" + str(i+1)) == variaveis[j]):
            #Caso ela seja encontrada, atualiza a string com seu valor e desativa a variavel de controle
            stringFinal = stringFinal + "\nx" + str(i+1) + " = " + str(constante[j])
            ehZero = False
    #Se ela nao foi encontrada, quer dizer que seu valor eh zero, entao atualiza a string com isso
    if (ehZero):
        stringFinal = stringFinal + "\nx" + str(i+1) + " = 0"
#Ultima atualizacao da string, inserindo o valor maximo obtido na funcao objetivo
stringFinal = stringFinal + "\nz = " + str(constante[0])
print(stringFinal)