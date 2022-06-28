import random
import sys

import numpy as np
import h5py
from itertools import permutations
from scipy.spatial import distance

x, y, total_mutacoes, melhor_custo, melhor_solucao = 0, 0, 0, 0, 0


# Carrega o arquivo especificado e transforma em um array de int
# Obs.: Deve ser um arquivo .csv
def gerar_populacao(nome_arquivo):
    csv_data = open(nome_arquivo)
    array_processado = np.loadtxt(csv_data, dtype=int, delimiter=";")
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
    matriz_distancia = np.zeros((tamanho_matriz, tamanho_matriz))  # instancia a matriz de distancias

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

    for idx, gene in enumerate(cromossomo):  # usa-se enumerate() para buscar outras posicoes do array na mesma iteracao
        if (idx < (len(cromossomo) - 1)):  # o calculo de distancia so eh realizado ate a penultima posicao do array
            custo += matriz_distancia[gene][cromossomo[idx + 1]]
    return custo


# sorteia 5 casais de pais a partir de uma roleta. Não pode haver um casal com dois pais iguais
def escolhe_pais(grupo):
    roleta = gerar_roleta(grupo)

    casais = [[], [], [], [], []]

    for idx, item in enumerate(casais):
        idx_pai1 = random.randint(0, 54)
        pai1 = roleta[idx_pai1]
        idx_pai2 = random.randint(0, 54)
        pai2 = roleta[idx_pai2]
        while np.array_equal(valida_range(idx_pai2), valida_range(idx_pai1)):
            idx_pai2 = random.randint(0, 54)
            pai2 = roleta[idx_pai2]

        casais[idx] = [pai1, pai2]

    return casais

def valida_range(numero):
    if -1 < numero > 10:
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    elif 9 < numero > 19:
        return [10, 11, 12, 13, 14, 15, 16, 17, 18]
    elif 18 < numero > 27:
        return [19, 20, 21, 22, 23, 24, 25, 26]
    elif 26 < numero > 34:
        return [27, 28, 29, 30, 31, 32, 33]
    elif 33 < numero > 40:
        return [34, 35, 36, 37, 38, 39]
    elif 39 < numero > 45:
        return [40, 41, 42, 43, 44]
    elif 44 < numero > 49:
        return [45, 46, 47, 48]
    elif 48 < numero > 52:
        return [49, 50, 51]
    elif 51 < numero > 54:
        return [52, 53]
    elif numero == 54:
        return [54]

# Para determinar a distribuição do conjunto de cromossomos que serão escolhidos para a
# reprodução, calculamos a probabilidade, na qual distribuímos os valores inversamente
def gerar_roleta(lista):
    roleta = []
    i = 10
    for item in lista:
        j = i
        while j > 0:
            roleta.append(item[1])
            j -= 1
        i -= 1
    return roleta


# Como no nosso caso o agente visita somente uma vez cada cidade, utilizaremos para fazer a
# Recombinação (crossover) a técnica de “cycle”
def recombinar(casais):
    filhos = []
    i = 0
    while i < 5:
        trocar_ultima_posicao = False
        descendente1 = casais[i][0].copy()
        descendente2 = casais[i][1].copy()
        print("Pai 1: " + str(descendente1))
        print("Pai 2: " + str(descendente2))

        indice_troca = random.randint(0, 19) # Escolhemos um local aleatório dentro do cromossomo.
        if indice_troca == 0: # Se o ponto de partida foi escolhido, é necessário trocar o ponto de destino
            trocar_ultima_posicao = True

        #  Os dois cromossomos pais trocam os números inteiros neste local para gerar os descendentes.
        valor_antigo = descendente1[indice_troca]
        descendente1[indice_troca] = descendente2[indice_troca]
        descendente2[indice_troca] = valor_antigo

        # Em seguida, mudamos o número duplicado da primeira descendência com o
        # mesmo local do número da segunda descendência.
        tratar_valores_iguais(descendente1, descendente2, indice_troca)
        if trocar_ultima_posicao:
            descendente1[20] = descendente1[0]
            descendente2[20] = descendente2[0]

        print("Filho 1: " + str(descendente1))
        print("Filho 2: " + str(descendente2))
        print("--------------------------")
        filhos.append(descendente1)
        filhos.append(descendente2)
        i += 1
    return filhos


# Troca os valores dos descendentes até não houver mais números repetidos
def tratar_valores_iguais(descendente1, descendente2, indice_ultima_troca):
    while possui_valor_repetido(descendente1) is True or possui_valor_repetido(descendente2) is True:
        if possui_valor_repetido(descendente1) is True:
            resolver_repeticoes(descendente1, descendente2, indice_ultima_troca)
        elif possui_valor_repetido(descendente2) is True:
            resolver_repeticoes(descendente2, descendente1, indice_ultima_troca)


# Troca os números dos descentendes até não houver mais repetições
def resolver_repeticoes(descendente1, descendente2, indice_ultima_troca):
    valor_repetido = possui_valor_repetido(descendente1)
    while valor_repetido:
        valor = obter_valor_duplicado(descendente1)
        indices = obter_indices(descendente1, valor)
        indice = indices[0]
        if indice == indice_ultima_troca: # Verificar para não ficar trocando a mesma posição infinitamente
            indice = indices[1]
        valor_antigo = descendente1[indice]
        descendente1[indice] = descendente2[indice]
        descendente2[indice] = valor_antigo
        indice_ultima_troca = indice
        if indice_ultima_troca == 0: # Se o ponto de partida foi escolhido, é necessário trocar o ponto de destino
            descendente1[20] = descendente1[0]
            descendente2[20] = descendente2[0]
        valor_repetido = possui_valor_repetido(descendente1)


# Retorna o valor duplicado da lista
def obter_valor_duplicado(descendente):
    lista = []
    for i in descendente:
        if i not in lista:
            lista.append(i)
        else:
            return i


# Retorna todos os índices que possuem um determinado valor
def obter_indices(descendente, valor):
    indices = []
    i = 0
    while i < (len(descendente) - 1):
        if valor == descendente[i]:
            indices.append(i)
        i += 1
    return list(dict.fromkeys(indices))


# Verifica se um descendente possui números repetidos
def possui_valor_repetido(descendente):
    i = 0
    valores = []
    while i < 20:
        if descendente[i] not in valores:
            valores.append(descendente[i])
        else:
            return True
        i += 1
    return False


# O operador de mutação escolhe aleatoriamente dois números inteiros em um cromossomo
# da nova geração e os troca. O operador de mutação atua sobre cada membro da nova
# geração com probabilidade de 0,05.
def mutacao(populacao_nova):
    global total_mutacoes
    for i in populacao_nova:
        mutacao_aleatoria = random.randint(1, 100)
        if 1 <= mutacao_aleatoria <= 5:
            print("ocorreu mutação")
            indices = gerar_indices()
            valor_antigo = i[indices[0]]
            i[indices[0]] = i[indices[1]]
            i[indices[1]] = valor_antigo
            if indices[0] == 0 or indices[1] == 0: # Se o ponto de partida foi escolhido, é necessário trocar o ponto de destino
                i[20] = i[0]
            total_mutacoes += 1


# Retorna dois índices diferentes para serem usados na mutação
def gerar_indices():
    indices = []
    indice_valido = False
    while indice_valido is False:
        indice1 = random.randint(0, 19)
        indice2 = random.randint(0, 19)
        if indice1 != indice2:
            indice_valido = True
            indices.append(indice1)
            indices.append(indice2)
    return indices


# Exibe os resultados da execução
def print_resultados():
    media_mutacao = 0
    if total_mutacoes != 0:
        media_mutacao = total_mutacoes / 10000
        media_mutacao = media_mutacao * 100

    print("Tamanho da população: 20")
    print("Probabilidade de ocorrer mutação: 0,05")
    print("Mutações ocorridas: " + str(total_mutacoes))
    print("Média de mutações: " + str(media_mutacao) + "%")
    print("Número de cidades: 20")
    print("Melhor custo: " + str(melhor_custo))
    print("melhor solução: " + str(melhor_solucao))


# Contem todos os processos do algoritmo
def main():
    # 1. Codificar a população de indivíduos (20 individuos)
    populacao = gerar_populacao("matriz_inicial.csv")
    posicoes = gerar_posicoes("cidades.csv")
    x = posicoes[0]
    y = posicoes[1]

    distancias = gerar_distancias(populacao, x, y)

    ciclos = 0
    global melhor_custo, melhor_solucao
    melhor_custo = sys.float_info.max
    while ciclos < 10000:
        # 2. Aplicado a funcao de custo/aptidao para cada individuo/cromossomo e organiza-os de menor ao maior
        # Obs.: quanto menor o custo, melhor
        custos_populacao = np.empty(len(populacao),
                                    dtype=float)  # cria lista onde serao armazenados os custos de cada cromossomo/individuo

        for idx, cromossomo in enumerate(populacao):
            custos_populacao[idx] = func_custo(cromossomo,
                                               distancias)  # realiza o calculo de custo para cada cromossomo

        custos_cromossomos = list(
            zip(custos_populacao, populacao))  # parelha a lista de custos com a lista de cromossomos
        custos_cromossomos.sort(key=lambda x: x[0])  # organiza a lista de menor para maior
        if melhor_custo > custos_cromossomos[0][0]:
            melhor_custo = custos_cromossomos[0][0]
            melhor_solucao = custos_cromossomos[0][1]

        # 3. Metodo de selecao dos pais
        populacao = []  # selecionar os 10 melhores individuos/cromossomos

        i = 0
        while i < 10:
            populacao.append(custos_cromossomos[i])
            i += 1

        casais = escolhe_pais(populacao)
        filhos = recombinar(casais)
        mutacao(filhos)
        nova_geracao = []
        # Junta os pais com os filhos
        for item in populacao:
            nova_geracao.append(item[1])
        for filho in filhos:
            nova_geracao.append(filho)
        populacao = nova_geracao
        print("fim do ciclo " + str(ciclos))
        ciclos += 1
    print_resultados()


main()
