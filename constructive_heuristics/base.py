from abc import ABC, abstractmethod
import math


def distancia_euclidiana_2d(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class ConstructiveHeuristic(ABC):
    def criar_matriz_distancias(
        self, coordenadas: list[list[int, int]]
    ) -> list[list[int]]:
        tamanho = len(coordenadas)
        matriz = [[0] * tamanho for _ in range(tamanho)]

        for i in range(tamanho):
            for j in range(tamanho):
                if i != j:
                    matriz[i][j] = distancia_euclidiana_2d(
                        coordenadas[i], coordenadas[j]
                    )

        return matriz

    def criar_dicionario_cidades_ordenadas(
        self, matriz_distancias: list[list[int]]
    ) -> dict[int, list[int]]:
        dicionario = {}

        for i in range(len(matriz_distancias)):
            distancias = [
                (j, matriz_distancias[i][j])
                for j in range(len(matriz_distancias))
                if i != j
            ]
            distancias_ordenadas = sorted(distancias, key=lambda x: x[1])
            dicionario[i] = [cidade for cidade, _ in distancias_ordenadas]
        return dicionario

    @abstractmethod
    def __init__(self, cordenates: list[list[int, int]], first_city: int):
        pass

    @abstractmethod
    def solve(self) -> list[int]:
        pass
