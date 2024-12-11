from constructive_heuristics import ConstructiveHeuristic
from instance_handler import InstanceHandler
from neighborhood_structure import NeighborhoodStructure

from .local_search import LocalSearch

class VND(LocalSearch):

    def __init__(
        self,
        initial_heuristic: ConstructiveHeuristic,
        avaible_neighborhoods: list[NeighborhoodStructure],
    ):
        self.__initial_heuristic = initial_heuristic
        self.__avaible_neighborhoods = avaible_neighborhoods

    def improve(self, instance_handler: InstanceHandler, current_solution: list[int], current_cost: int) -> tuple[int, list[int]] | tuple[None, None]:
        """
        Improve the current solution using some neighborhood structure that was
        able of provides some improvement to current solution, if nothing is able
        returns a tuple of None, None

        Warning: The order of the neighborhoods in the list is important, the
        first is always the main neighborhood structure that will be used, therefore
        it could be considered as the condutor of the search, the others only
        are used if the main neighborhood structure is not able to provide any
        improvement
        """
        for neighborhood in self.__avaible_neighborhoods:
            nc, ns = neighborhood.improve(instance_handler, current_cost, current_solution)
            if ns:
                return nc, ns
        return None, None

    def solve(self, instance_handler: InstanceHandler) -> tuple[int, list[int]]:
        """
        Solve the TSP problem using the VND local search algorithm
        """
        best_solution = self.__initial_heuristic.solve()
        best_cost = instance_handler.calcular_funcao_objetivo(best_solution)
        while True:
            new_cost, new_solution = self.improve(instance_handler, best_solution, best_cost)
            if not new_solution:
                break
            best_solution = new_solution
            best_cost = new_cost
        return best_cost, best_solution
