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

    def solve(self, instance_handler: InstanceHandler) -> tuple[float, list[int]]:
        """
        Solve the TSP problem using the hill climbing algorithm
        returns a tuple with the cost of the solution and a list that is the
        encode of the path
        """
        initial_solution = self.__initial_heuristic.solve()[:-1]
        best_solution = initial_solution
        best_cost = instance_handler.calcular_funcao_objetivo(best_solution)
        while True:
            new_cost = self.__neighborhood_structure.get_better_neighbor(instance_handler, best_solution, best_cost)
            if not new_cost:
                break
            best_cost = new_cost
        best_solution = best_solution + best_solution[0:1]
        return instance_handler.calcular_funcao_objetivo(best_solution), best_solution
