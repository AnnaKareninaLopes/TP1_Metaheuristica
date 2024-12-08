from .base import ConstructiveHeuristic

class NearestNeighbor(ConstructiveHeuristic):

    def __init__(self, cordenates: list[list[int, int]], first_city: int):
        self.cordenates = cordenates
        self.first_city = first_city
        matriz_distancias = self.criar_matriz_distancias(cordenates)
        self.matriz_distancias = matriz_distancias
        self.dicionario_ondenado = self.criar_dicionario_cidades_ordenadas(matriz_distancias)

    def solve(self) -> list[int]:
        dicionario = self.dicionario_ondenado
        matriz_distancias = self.matriz_distancias
        cidade_atual = self.first_city
        cidade_inicial = self.first_city
        vetor_solucao = [cidade_atual]
        distancia_total = 0

        while len(vetor_solucao) < len(dicionario):
            menor_distancia = float('inf')
            vizinho_mais_proximo = None

            for vizinho in dicionario[cidade_atual]:
                if vizinho not in vetor_solucao:
                    distancia = matriz_distancias[cidade_atual][vizinho]
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        vizinho_mais_proximo = vizinho

            if vizinho_mais_proximo is not None:
                vetor_solucao.append(vizinho_mais_proximo)
                distancia_total += menor_distancia
                cidade_atual = vizinho_mais_proximo

        # Adiciona a distância de retorno à cidade inicial
        distancia_total += matriz_distancias[cidade_atual][cidade_inicial]
        vetor_solucao.append(cidade_inicial)

        return vetor_solucao
