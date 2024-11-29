from abc import ABC, abstractmethod
from math import inf

from operacoes import calcular_funcao_objetivo

class NeighborhoodStructure(ABC):

    @abstractmethod
    def generate_neighborhood(self, solution: list[int]) -> bool:
        """
        generate the next neighboor to a local search of according with the
        specify neighborhood structure
        """

class Exchange(NeighborhoodStructure):

    def __calc_swap_cost(self, solution: list[int], index: int, index2: int) -> int:
        """
        calculate the cost of swap two elements in the solution
        """
        solution[index], solution[index2] = solution[index2], solution[index]
        cost = calcular_funcao_objetivo(solution)
        solution[index], solution[index2] = solution[index2], solution[index]
        return cost

    def generate_neighborhood(self, solution: list[int]) -> bool:
        """
        generate the next neighboord using the exchange neighborhood structure
        """
        best_cost = inf
        by = None
        that = None
        for index, _ in enumerate(solution):
            for index2, _ in enumerate(solution):
                if index != index2:
                    cost = self.__calc_swap_cost(solution, index, index2)
                    if cost < best_cost:
                        best_cost = cost
                        by = index
                        that = index2
        if best_cost == inf:
            return False
        solution[by], solution[that] = solution[that], solution[by]
        return True
