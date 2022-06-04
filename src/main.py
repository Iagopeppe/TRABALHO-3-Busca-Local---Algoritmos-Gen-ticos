import numpy as np
import h5py
from itertools import permutations
from scipy.spatial import distance

global x, y


# Carrega o arquivo especificado e transforma em um array de int
# Obs.: Deve ser um arquivo .csv
def gerar_populacao(nome_arquivo):
    CSVData = open(nome_arquivo)
    array_processado = np.loadtxt(CSVData, dtype=int, delimiter=";")
    return array_processado

# Carrega a lista de posicoes [x,y]
def gerar_posicoes(nome_arquivo):
    CSVData = open(nome_arquivo)
    array_processado = np.loadtxt(CSVData, dtype=float, delimiter=";")
    return array_processado

# Gera uma matriz com as distancias entre cada item/elemento do array
# Obs.: utiliza das variaveis globais [x,y] para pegar as coordenadas
def gerar_distancias(populacao, x, y):
    tamanho_matriz = len(populacao)
    matriz_distancia = np.zeros((tamanho_matriz, tamanho_matriz)) #instancia a matriz de distancias

    for idx_i, i in enumerate(matriz_distancia):
        coordenada_i = x[idx_i], y[idx_i]
        for idx_j, j in enumerate(i):
            coordenada_j = x[idx_j], y[idx_j]
            matriz_distancia[idx_i][idx_j] = distance.euclidean(coordenada_i, coordenada_j)

    return matriz_distancia

# Funcao de custo para o problema do caixeiro viajante
# Deve-se passar como argumento um individuo/cromossomo de uma populacao
def func_custo(cromossomo, matriz_distancia):
    custo = 0.00

    for idx, gene in enumerate(cromossomo):
        if (idx < (len(cromossomo) - 1)):
            custo += matriz_distancia[gene][cromossomo[idx+1]]
    return custo

# Contem todos os processos do algoritmo
def main():

    # 1. Codificar a população de indivíduos (20 individuos)
    populacao = gerar_populacao("matriz_inicial.csv")
    posicoes = gerar_posicoes("cidades.csv")
    x = posicoes[0]
    y = posicoes[1]

    distancias = gerar_distancias(populacao, x, y)



main()