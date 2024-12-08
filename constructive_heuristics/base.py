from abc import ABC, abstractmethod


class ConstructiveHeuristic(ABC):

    def criar_dicionario_cidades_ordenadas(self, matriz_distancias):
        dicionario = {}

        for i in range(len(matriz_distancias)):
            distancias = [(j, matriz_distancias[i][j]) for j in range(len(matriz_distancias)) if i != j]
            distancias_ordenadas = sorted(distancias, key=lambda x: x[1])
            dicionario[i + 1] = [cidade + 1 for cidade, _ in distancias_ordenadas]  # Adiciona +1 para ajustar os índices
        return dicionario

    @abstractmethod
    def __init__(self, cordenates: list[list[int, int]], first_city: int):
        pass

    @abstractmethod
    def solve(self) -> list[int]:
        pass
