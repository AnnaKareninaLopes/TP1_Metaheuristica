from typing import Optional

from constructive_heuristics import ConstructiveHeuristic
from neighborhood_structure import NeighborhoodStructure
from instance_handler import InstanceHandler

class HillClimbing:

    def __init__(
        self,
        constructive_heuristic: ConstructiveHeuristic,
        neighborhood_structure: NeighborhoodStructure
    ):
        self.__initial_heuristic = constructive_heuristic
        self.__neighborhood_structure = neighborhood_structure

    def improve_solution(
        self,
        solution: list[int],
        cost: int,
        instance_handler: InstanceHandler
    ) -> tuple[Optional[list[int]], Optional[int]]:
        """
        Get a better solution from the neighborhood of the current solution
        """
        for neighbor in self.__neighborhood_structure.enumerate_neighbors(solution):
            new_cost = instance_handler.calcular_funcao_objetivo(neighbor)
            if new_cost < cost:
                return neighbor, new_cost
        return None, None

    def solve(self, instance_handler: InstanceHandler) -> tuple[int, list[int]]:
        """
        Solve the TSP problem using the hill climbing algorithm
        returns a tuple with the cost of the solution and a list that is the
        encode of the path
        """
        initial_solution = self.__initial_heuristic.solve()[:-1]
        best_solution = initial_solution
        best_cost = instance_handler.calcular_funcao_objetivo(best_solution)
        while True:
            new_solution, new_cost = self.improve_solution(
                best_solution, best_cost, instance_handler
            )
            if not new_solution:
                break
            best_solution = new_solution
            best_cost = new_cost
        best_solution = best_solution + best_solution[0:1]
        return instance_handler.calcular_funcao_objetivo(best_solution), best_solution
