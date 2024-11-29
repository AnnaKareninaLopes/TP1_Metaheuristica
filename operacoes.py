from enum import Enum
import math
import os
import time
from typing import Type

import pandas as pd

from constructive_heuristics import (
    ConstructiveHeuristic,
    CheapestInsertion,
    Mst,
    NearestNeighbor,
)

class Heuristics(str, Enum):
    MST = "agm"
    CLOSEST_NEIGHBOR = "nn"
    CHEAPEST_INSERTION = "ci"

    def get_heuristic_class(self) -> Type[ConstructiveHeuristic]:
        heuristic_mapping = {
            Heuristics.MST: Mst,
            Heuristics.CLOSEST_NEIGHBOR: NearestNeighbor,
            Heuristics.CHEAPEST_INSERTION: CheapestInsertion,
        }
        return heuristic_mapping[self]

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
    nome_instancia = os.path.basename(nome_instancia)
    df = pd.read_csv(arquivo_csv, thousands='.', decimal=',')

    # Acessa a linha correspondente à instância
    linha = df[df['Instancia'] == nome_instancia]

    if not linha.empty:
        return linha['Otimo'].values[0] # Retorna o valor ótimo
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


def save_results(linha_dados: list, arquivo_saida:str):
    if not os.path.exists(arquivo_saida):
        cabecalho = ["INSTANCE", "METHOD", "PARAM", "OBJECTIVE_FUNCTION", "OPTIMUM", "GAP", "TIME", "NODES", "ARCS"]
        df = pd.DataFrame([linha_dados], columns=cabecalho)
        with open(arquivo_saida, "w", encoding='utf-8') as f:
            f.write(str(df.to_string(index=False, col_space=12, justify="left")))
        return
    with open(arquivo_saida, "r", encoding='utf-8') as f:
        existing_data = pd.read_csv(arquivo_saida, sep="\s+")
        new_data = pd.DataFrame([linha_dados], columns=existing_data.columns)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    with open(arquivo_saida, "w", encoding='utf-8') as f:
        f.write(str(updated_data.to_string(index=False, col_space=12, justify="left")))


# Função para medir o tempo de execução e calcular todos os resultados
def run_constructive_heuristic(coordenadas, cidade_inicial, arquivo_entrada, arquivo_saida, otimo, heuristica: Heuristics):

    print("Otimo na função executar_tsp: ", otimo)

    # Medindo o tempo de execução
    start_time = time.time()

    # Executando o heurístico de vizinho mais próximo
    heuristic_class = heuristica.get_heuristic_class()
    heuristic = heuristic_class(cordenates=coordenadas, first_city=coordenadas.index(cidade_inicial))
    tour = heuristic.solve()

    # Calculando o tempo de execução
    end_time = time.time()
    tempo_execucao = end_time - start_time

    # Calculando o valor da função objetivo (distância total do tour)
    distances = []
    for city, neighbor in zip(tour, tour[1:]):
        distances.append(distancia_euclidiana_2d(coordenadas[city], coordenadas[neighbor]))

    funcao_objetivo = calcular_funcao_objetivo(distances)

    # Calculando o número de nós (cidades) e arcos (viagens)
    numero_nos = len(coordenadas)
    numero_arcos = (numero_nos * (numero_nos - 1)) / 2

    # Calculando o GAP
    gap = 100 * (abs(funcao_objetivo - otimo) / otimo)

    print("Gap na função executar_tsp: ", gap)

    linha_dados = [arquivo_entrada, str(heuristica), str(coordenadas.index(cidade_inicial)) ,str(funcao_objetivo), str(otimo), f"{gap:.2f}", f"{tempo_execucao:.4f}", str(numero_nos), str(numero_arcos) ]
    save_results(linha_dados, arquivo_saida)

    print(f"Função Objetivo: {funcao_objetivo:.2f}")
    print(f"Tempo de Execução: {tempo_execucao:.4f} segundos")
    print(f"Número de Nós: {numero_nos}")
    print(f"Número de Arcos: {numero_arcos}")
    print(f"Tour: {tour}")
    print(f"GAP: {gap:.2f}")