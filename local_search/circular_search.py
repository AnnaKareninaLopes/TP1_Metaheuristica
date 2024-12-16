from constructive_heuristics import ConstructiveHeuristic
from instance_handler import InstanceHandler
from neighborhood_structure import NeighborhoodStructure

from .local_search import LocalSearch



class CircularSearch(LocalSearch):

    def __init__(
        self,
        initial_heuristic: ConstructiveHeuristic,
        avaible_neighborhoods: list[NeighborhoodStructure],
    ):
        self.__avaible_neighborhoods = avaible_neighborhoods
        self.__initial_heuristic = initial_heuristic

    def __improve(
        self,
        current_solution: list[int],
        current_cost: int,
        instance_handler: InstanceHandler
    )->tuple[int, list[int]] | tuple[None, None]:
        last_feasible = current_solution
        last_feasible_cost = current_cost
        for neighborhood in self.__avaible_neighborhoods:
            nc, ns = neighborhood.improve(
                instance_handler, last_feasible_cost, last_feasible
            )
            if nc:
                last_feasible = ns
                last_feasible_cost = nc
        if last_feasible_cost != current_cost:
            return last_feasible_cost, last_feasible
        return None, None

    def solve(self, instance_handler: InstanceHandler) -> tuple[int, list[int]]:
        best_solution = self.__initial_heuristic.solve()
        best_cost = instance_handler.calcular_funcao_objetivo(best_solution)
        while True:
            new_cost, new_solution = self.__improve(
                best_solution, best_cost, instance_handler
            )
            if not new_solution:
                break
            best_solution = new_solution
            best_cost = new_cost
        return best_cost, best_solution
