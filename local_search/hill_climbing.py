from instance_handler import InstanceHandler
from neighborhood_structure import NeighborhoodStructure

from .local_search import LocalSearch


class HillClimbing(LocalSearch):
    def __init__(
        self,
        neighborhood_structure: NeighborhoodStructure,
    ):
        self.__neighborhood_structure = neighborhood_structure

    def solve(self, initial_solution:list[int], instance_handler: InstanceHandler) -> tuple[int, list[int]]:
        """
        Solve the TSP problem using the hill climbing algorithm
        returns a tuple with the cost of the solution and a list that is the
        encode of the path
        """
        best_solution = initial_solution
        best_cost = instance_handler.calcular_funcao_objetivo(best_solution)
        while True:
            new_cost, new_solution = self.__neighborhood_structure.improve(
                instance_handler, best_cost, best_solution
            )
            if not new_solution:
                break
            best_solution = new_solution
            best_cost = new_cost
        return best_cost, best_solution
