from abc import ABC, abstractmethod
from math import inf

from operacoes import calcular_funcao_objetivo

class NeighborhoodStructure(ABC):

    @abstractmethod
    def get_better_neighbor(self, solution: list[int]) -> bool:
        """
        get the best neighbor of a solution according with the specify
        neighborhood structure
        """

    @abstractmethod
    def get_neighbor(self, solution: list[int]) -> None:
        """
        get a neighbor of a solution according with the specify neighborhood,
        not necessarily the best, only a neighbor
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

    def get_better_neighbor(self, solution: list[int]) -> bool:
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

    def get_neighbor(self, solution: list[int]) -> None:
        pass
