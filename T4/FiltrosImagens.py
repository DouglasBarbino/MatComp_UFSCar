# -*- coding: utf-8 -*-
"""
Implementacao dos filtros da Mediana e de Wiener Adaptativo Pontual 
para tratar o ruido impulssivo e o Gaussiano, respectivamente
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""
import skimage
import numpy as np
from skimage import io

def converteNormalizaImagem(imagem):
    #Converte a imagem para float
    imagemFloat = skimage.util.img_as_float(imagem)
    #Caso o maior pixel nao seja 1.0 (branco puro), eh recomendo normalizar a imagem para melhores resultados
    if (imagemFloat.max() != 1.0):
        #Busca o pixel de maior valor
        valorNormalizacao = imagemFloat.max()
        #Percorre a altura da imagem
        for i in range(0, imagem.shape[0]):
            #Percorre a largura da imagem
            for j in range(0, imagem.shape[1]):
                imagemFloat[i][j] = imagemFloat[i][j] / valorNormalizacao
    return imagemFloat

def FiltroMediana(imagem,dimensaoJanela):
    imagem_normalizada = converteNormalizaImagem(imagem)
    imagemTratada = np.zeros(shape=(imagem.shape[0],imagem.shape[1]))
    pixels = dimensaoJanela*dimensaoJanela
    #Momento de percorrer a imagem para trata-la (loop externo = altura; loop interno = largura)
    for i in range(0, imagem.shape[0]):
        for j in range(0, imagem.shape[1]):
            elementos_janela=[]
            for k in range (pixels):
                #- Primeira coordenada lida com a altura, segunda com a largura.
                #- (dimensaoJanela-1)/2 porque queremos a mesma quantidade de pixels 
                #anteriores e posteriores a janela, alem do pixel na mesma coordenada
                #faz uma lista dos elementos da janela
                elementos_janela.append(imagem_normalizada[((k//dimensaoJanela)+i-((dimensaoJanela-1)/2))%imagem.shape[0]][((k%dimensaoJanela)+j-((dimensaoJanela-1)/2))%imagem.shape[1]] )
            #calcula o tamanho da lista dos elementos da janela
            size_elementos = len(elementos_janela)
            #calcula o indice da mediana
            indiceMediana = size_elementos/2
            #ordena os elementos por ordem crescente
            elementos_janela.sort()
            #calcula a mediana
            mediana = elementos_janela[int(indiceMediana)]
            #Atribuicao do pixel tratado na nova imagem
            imagemTratada[i][j] = mediana
    return imagemTratada
            
    
def FiltroWiener(imagem, dimensaoJanela, sigmaN):
    #Transforma a imagem em uma matriz de float e, se necessario, a normaliza
    imagem_normalizada = converteNormalizaImagem(imagem)
    #Cria uma matriz vazia que sera a saida
    imagemTratada = np.zeros(shape=(imagem.shape[0],imagem.shape[1]))
    #Armazena o numero de pixels que a janela possui
    pixels = dimensaoJanela * dimensaoJanela
    #Momento de percorrer a imagem para trata-la (loop externo = altura; loop interno = largura)
    for i in range(0, imagem.shape[0]):
        for j in range(0, imagem.shape[1]):
            #Limpa algumas variaveis
            miF = 0 #media
            sigmaF = 0 #variancia na janela
            sigmaS = 0 #variancia local
            for k in range (pixels):
                #- Primeira coordenada lida com a altura, segunda com a largura.
                #- (dimensaoJanela-1)/2 porque queremos a mesma quantidade de pixels 
                #anteriores e posteriores a janela, alem do pixel na mesma coordenada
                #- Formula da media: i e j sao as coordenadas que definem o ponto central
                #  *A matriz eh percorrida do modo [0][0], [0][1], ... , [0][4], [1][0], ... , [4][4] 
                #(o k//dimensaoJanela e k%dimensaoJanela), mas nao de 0 a 4, e sim de -2 à 2 ((dimensaoJanela-1)/2)
                #  *imagem.shape[0] e [1] são a altura e largura, respectivamente, 
                #sendo necessario ser modulo delas para nao dar um indice fora da imagem
                miF += (1/pixels) * imagem_normalizada[((k//dimensaoJanela)+i-((dimensaoJanela-1)/2))%imagem.shape[0]][((k%dimensaoJanela)+j-((dimensaoJanela-1)/2))%imagem.shape[1]] 
            for k in range (pixels):
                #Calculo da variancia na janela eh semelhante a da media,
                #apenas acrescentando a subtracao pela media e elevando esse valor ao quadrado
                sigmaF += (1/pixels) * (imagem_normalizada[((k//dimensaoJanela)+i-((dimensaoJanela-1)/2))%imagem.shape[0]][((k%dimensaoJanela)+j-((dimensaoJanela-1)/2))%imagem.shape[1]] - miF)**2
            #Modifica sigmaS caso sigmaF - sigmaN sejam maiores do que 0, 
            #caso contrario fica o valor limpo anteriormente (0)
            if (sigmaF - sigmaN > 0):
                sigmaS = sigmaF - sigmaN
            #Atribuicao do pixel tratado na nova imagem
            imagemTratada[i][j] = miF + (sigmaS * (imagem_normalizada[i][j] - miF) / (sigmaS + sigmaN))
    return imagemTratada
    
#Carrega a imagem
imagem1 = io.imread('imagens_ruidosas\\camera_gaussian.png')
imagem2= io.imread('imagens_ruidosas\\camera_sal_e_pimenta.png')

'''--Comandos importantes--'''
#Coordenadas
#print(imagem1.shape)
#Altura
#print(imagem1.shape[0])
#Largura
#print(imagem1.shape[1])
'''----------'''
#Chama o Filtro de Wiener com uma janela 5x5 e variancia do ruido (sigma_n) = 0.01
imagem1Tratada = FiltroWiener(imagem1, 5, 0.01)
#Salvar imagem tratada
io.imsave('imagens_ruidosas\camera_gaussian_tratada5.png', imagem1Tratada)
imagem2Tratada = FiltroMediana(imagem2,3)
#Salvar imagem tratada
io.imsave('imagens_ruidosas\\camera_sal_e_pimenta_tratado.png', imagem2Tratada)