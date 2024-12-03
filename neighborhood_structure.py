from abc import ABC, abstractmethod
import pickle
from typing import Optional

from instance_handler import InstanceHandler


class NeighborhoodStructure(ABC):
    @abstractmethod
    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ) -> tuple[Optional[int], Optional[list[int]]]:
        """
        Should to try improve a current solution with base a specific
        neighborhood structure
        """


class TwoOpt(NeighborhoodStructure):
    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ) -> tuple[int | None, list[int] | None]:
        best_solution = None
        best_cost = None
        solution_pdump = pickle.dumps(solution)
        for i in range(len(solution) - 1):
            for j in range(i + 2, len(solution) - 1):
                cost_i_to_j = instance_handler.calculate_isolated_cost(
                    solution[i], solution[j]
                )
                cost_i1_to_j1 = instance_handler.calculate_isolated_cost(
                    solution[i + 1], solution[j + 1]
                )
                cost_i_to_i1 = instance_handler.calculate_isolated_cost(
                    solution[i], solution[i + 1]
                )
                cost_j_to_j1 = instance_handler.calculate_isolated_cost(
                    solution[j], solution[j + 1]
                )
                new_cost = (
                    scost + cost_i_to_j + cost_i1_to_j1 - cost_i_to_i1 - cost_j_to_j1
                )
                if new_cost < scost:
                    new_solution = pickle.loads(solution_pdump)
                    new_solution[i + 1 : j + 1] = list(
                        reversed(new_solution[i + 1 : j + 1])
                    )
                    best_solution = new_solution
                    best_cost = new_cost
        return best_cost, best_solution
