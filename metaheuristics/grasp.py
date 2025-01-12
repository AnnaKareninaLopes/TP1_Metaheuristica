import random

from instance_handler import InstanceHandler
from local_search import LocalSearch

from .base import Metaheuristics

class RCL:

    def __init__(
        self,
        alpha: float,
    ):
        self.__alpha = alpha

    def build_rcl(
        self,
        current_solution: list[int],
        instance_handler: InstanceHandler
    ) -> list[int]:
        current = current_solution[-1]
        candidates = [city for city in instance_handler.get_cities() if city not in current_solution]
        if not candidates:
            return []
        costs = [instance_handler.calculate_isolated_cost(current, city) for city in candidates]
        min_cost = min(costs)
        max_cost = max(costs)
        rlc = [candidates[index] for index, cost in enumerate(costs) if cost <= (min_cost + self.__alpha*(max_cost-min_cost))]
        return rlc

class Grasp(Metaheuristics):

    def __init__(
        self,
        alpha: float,
        initial_city:int,
        local_search: LocalSearch,
        max_it: int,
    ):
        self.__alpha = alpha
        self.__local_search = local_search
        self.__initial_city = initial_city
        self.__max_it = max_it

    def __construct_greedy_random_solution(
        self,
        alpha:float,
        initial_city: int,
        instance_handler: InstanceHandler
    ) -> list[int]:
        current_solution = [initial_city]
        rcl = RCL(alpha)
        candidates = rcl.build_rcl(current_solution, instance_handler)
        while candidates:
            city = random.choice(candidates)
            current_solution.append(city)
            candidates = rcl.build_rcl(current_solution, instance_handler)
        return current_solution + current_solution[0:1]

    def solve(
        self, instance_handler: InstanceHandler,
    ) -> tuple[int, list[int]]:
        best_cost = float("inf")
        best_solution = None
        max_it = self.__max_it
        alpha = self.__alpha
        initial_city = self.__initial_city
        for _ in range(max_it):
            greedy_solution = self.__construct_greedy_random_solution(alpha, initial_city, instance_handler)
            cost, solution = self.__local_search.solve(greedy_solution, instance_handler)
            if cost < best_cost:
                best_cost = cost
                best_solution = solution
        return best_cost, best_solution
