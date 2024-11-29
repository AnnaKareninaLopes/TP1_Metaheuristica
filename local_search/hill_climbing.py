from constructive_heuristics import ConstructiveHeuristic
from neighborhood_structure import NeighborhoodStructure
from operacoes import calcular_funcao_objetivo

class HillClimbing:

    def __init__(
        self,
        constructive_heuristic: ConstructiveHeuristic,
        neighborhood_structure: NeighborhoodStructure
    ):
        self.__initial_heuristic = constructive_heuristic
        self.__neighborhood_structure = neighborhood_structure

    def solve(self) -> tuple[float, list[int]]:
        """
        Solve the TSP problem using the hill climbing algorithm
        returns a tuple with the cost of the solution and a list that is the
        encode of the path
        """
        initial_solution = self.__initial_heuristic.solve()
        best_solution = initial_solution
        best_cost = calcular_funcao_objetivo(best_solution)
        while True:
            if not self.__neighborhood_structure.get_better_neighbor(best_solution):
                break
            best_cost = calcular_funcao_objetivo(best_solution)
        return best_cost, best_solution
