import math
import time

import pandas as pd

from mst import Mst

# Lê o arquivo de corrdenas e retorna uma lista com elas
def leitor_coordenadas_tsp(arquivo):
    with open(arquivo, 'r') as arquivo:
        coordenadas = []
        secao_coord = False

        for linha in arquivo:
            linha = linha.strip()
            if linha.startswith('NODE_COORD_SECTION'):
                secao_coord = True
                continue

            if secao_coord:
                if linha == 'EOF':
                    break
                partes = linha.split()
                x, y = float(partes[1]), float(partes[2])
                coordenadas.append([x, y])

    return coordenadas

# Função para obter o valor ótimo da instância
def obter_otimo(arquivo_csv, nome_instancia):
    df = pd.read_csv(arquivo_csv)  # Lê o arquivo CSV

    # Acessa a linha correspondente à instância
    linha = df[df['Instancia'] == nome_instancia]

    if not linha.empty:
        return linha['Otimo'].values[0]  # Retorna o valor ótimo
    return None  # Retorna None se não encontrar a instância

# Função para calcular a distância Euclidiana em 2D
def distancia_euclidiana_2d(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Função que implementa o algoritmo guloso para encontrar o vizinho mais próximo
def algoritmo_guloso(vetor_candidatos, cidade_atual):
    # Encontra a cidade mais próxima da cidade atual
    vizinho_mais_proximo = min(
        vetor_candidatos,
        key=lambda cidade: distancia_euclidiana_2d(cidade_atual, cidade)
    )
    return vizinho_mais_proximo

# Função para calcular a função objetivo (distância total do tour)
def calcular_funcao_objetivo(distancias_tour):
    return sum(distancias_tour)

# Função que executa a heurística e calcula as distâncias durante a execução
def heuristica_vizinho_mais_proximo(coordenadas, cidade_inicial):

    # Criação do vetor de cidades (índices) e definição da cidade atual
    vetor_cadidatos = list(range(len(coordenadas)))

    # Define a cidade inicial como cidade atual
    cidade_atual = cidade_inicial
    cidade_atual_index = vetor_cadidatos[coordenadas.index(cidade_atual)]  # Encontra o índice da cidade inicial
    vetor_solucao = [cidade_atual_index]  # Armazena o índice da cidade atual

    # Retira do vetor de cidades a cidade atual
    vetor_cadidatos.remove(cidade_atual_index)

    # Lista para armazenar as distâncias entre as cidades consecutivas no tour
    distancias_tour = []

    # Enquanto houver cidades para serem visitadas
    while vetor_cadidatos:
        # Encontra o vizinho mais próximo
        vizinho = algoritmo_guloso([coordenadas[i] for i in vetor_cadidatos], coordenadas[cidade_atual_index])

        # Atualiza a cidade atual
        cidade_atual = vizinho
        cidade_atual_index = coordenadas.index(cidade_atual)  # Encontra o índice da cidade mais próxima

        # Adiciona o índice do vizinho ao vetor de solução
        vetor_solucao.append(cidade_atual_index)

        # Calcula a distância entre a cidade atual e o vizinho e armazena
        distancias_tour.append(distancia_euclidiana_2d(coordenadas[vetor_solucao[-2]], coordenadas[vetor_solucao[-1]]))

        # Remove o vizinho do vetor de candidatos
        vetor_cadidatos.remove(cidade_atual_index)

    # Adiciona a distância de volta à cidade inicial
    distancias_tour.append(distancia_euclidiana_2d(coordenadas[vetor_solucao[-1]], coordenadas[vetor_solucao[0]]))

    return vetor_solucao, distancias_tour, vetor_cadidatos

# Função de inserção mais barata
def heuristica_insercao_mais_barata(coordenadas, cidade_inicial):

    # Etapa 1: Seleciona as três primeiras cidades usando o vizinho mais próximo
    vetor_solucao, distancias_tour, vetor_cadidatos = heuristica_vizinho_mais_proximo(coordenadas, cidade_inicial)

    # Etapa 2: Insere cada cidade restante com a inserção mais barata
    while vetor_cadidatos:
        melhor_aumento = float('inf') # infinito positivo
        melhor_posicao = None
        melhor_cidade = None

        # Testa todas as cidades ainda não inseridas
        for cidade in vetor_cadidatos:
            for i in range(len(vetor_solucao)):
                cidade_anterior = vetor_solucao[i - 1] if i != 0 else vetor_solucao[-1]
                cidade_proxima = vetor_solucao[i]

                # Cálculo do aumento de custo se a cidade for inserida entre cidade_anterior e cidade_proxima
                aumento = (
                    distancia_euclidiana_2d(coordenadas[cidade_anterior], coordenadas[cidade]) +
                    distancia_euclidiana_2d(coordenadas[cidade], coordenadas[cidade_proxima]) -
                    distancia_euclidiana_2d(coordenadas[cidade_anterior], coordenadas[cidade_proxima])
                )

                # Verifica se o aumento é o menor encontrado até agora
                if aumento < melhor_aumento:
                    melhor_aumento = aumento
                    melhor_posicao = i
                    melhor_cidade = cidade

        # Insere a cidade na posição que gera o menor aumento de distância
        vetor_solucao.insert(melhor_posicao, melhor_cidade)
        distancias_tour.insert(melhor_posicao, melhor_aumento)
        vetor_cadidatos.remove(melhor_cidade)

    # Adiciona a distância de volta à cidade inicial para completar o ciclo
    distancias_tour.append(distancia_euclidiana_2d(coordenadas[vetor_solucao[-1]], coordenadas[vetor_solucao[0]]))
    return vetor_solucao, distancias_tour, vetor_cadidatos

def heuristica_arvore_geradora_minima(coordenadas, cidade_inicial):
    index = coordenadas.index(cidade_inicial)
    mst = Mst(coordenadas, index)
    path = mst.solve()
    distances = []
    for current, neighbor in zip(path, path[1:]):
        distances.append(
            distancia_euclidiana_2d(
                coordenadas[current],
                coordenadas[neighbor]
            )
        )
    return path, distances, []

# Função para medir o tempo de execução e calcular todos os resultados
def executar_tsp(coordenadas, cidade_inicial, arquivo_saida, otimo, heuristica):

    print("Otimo na função executar_tsp: ", otimo)

    # Medindo o tempo de execução
    start_time = time.time()

    # Executando o heurístico de vizinho mais próximo
    tour, distancias_tour, candidatos = heuristica(coordenadas, cidade_inicial)

    # Calculando o valor da função objetivo (distância total do tour)
    funcao_objetivo = calcular_funcao_objetivo(distancias_tour)

    # Calculando o número de nós (cidades) e arcos (viagens)
    numero_nos = len(coordenadas)
    numero_arcos = (numero_nos * (numero_nos - 1)) / 2

    # Calculando o GAP
    gap = 100 * (abs(funcao_objetivo - otimo) / otimo)

    print("Gap na função executar_tsp: ", gap)

    # Calculando o tempo de execução
    end_time = time.time()
    tempo_execucao = end_time - start_time

    # Escrevendo os resultados no arquivo de saída
    with open(arquivo_saida, 'w') as f:
        f.write(f"Função Objetivo (Distância Total): {funcao_objetivo:.2f}\n")
        f.write(f"Tempo de Execução: {tempo_execucao:.4f} segundos\n")
        f.write(f"Número de Nós: {numero_nos}\n")
        f.write(f"Número de Arcos: {numero_arcos}\n")
        f.write(f"Tour: {' -> '.join(map(str, tour))}\n")
        f.write(f"GAP: {gap:.2f}\n")

    print(f"Função Objetivo: {funcao_objetivo:.2f}")
    print(f"Tempo de Execução: {tempo_execucao:.4f} segundos")
    print(f"Número de Nós: {numero_nos}")
    print(f"Número de Arcos: {numero_arcos}")
    print(f"Tour: {tour}")
    print(f"GAP: {gap:.2f}")