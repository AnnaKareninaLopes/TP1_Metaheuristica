from abc import ABC, abstractmethod
import pickle

from instance_handler import InstanceHandler


class NeighborhoodStructure(ABC):
    @abstractmethod
    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ) -> tuple[int, list[int]] | tuple[None, None]:
        """
        Should to try improve a current solution with base a specific
        neighborhood structure
        """


class TwoOpt(NeighborhoodStructure):
    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ) -> tuple[int, list[int]] | tuple[None, None]:
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
                    return new_cost, new_solution
        return None, None

class TreeOpt(NeighborhoodStructure):
    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ) -> tuple[int | None, list[int] | None]:
        tour = solution[:]
        if tour[0] == tour[-1]:
            tour = tour[:-1]
        melhor_FO = scost
        n = len(solution)
        melhorou = True

        while melhorou:
            melhorou = False

            for i in range(n - 2):
                for j in range(i + 1, n - 1):
                    for k in range(j + 1, n):
                        variantes = [
                            tour[:i] + tour[i:j][::-1] + tour[j:k][::-1] + tour[k:],
                            tour[:i] + tour[j:k][::-1] + tour[i:j] + tour[k:],
                            tour[:i] + tour[j:k][::-1] + tour[i:j][::-1] + tour[k:],
                            tour[:i] + tour[i:j] + tour[j:k][::-1] + tour[k:],
                            tour[:i] + tour[i:j][::-1] + tour[k:j:-1] + tour[j:],
                            tour[:i] + tour[k:j:-1] + tour[i:j] + tour[j:],
                            tour[:i] + tour[k:j:-1] + tour[i:j][::-1] + tour[j:],
                            tour[:i] + tour[i:j] + tour[k:j:-1] + tour[j:]
                        ]

                        for variante in variantes:
                            melhor_FO_nova = instance_handler.calcular_funcao_objetivo(variante)
                            if melhor_FO_nova < melhor_FO:
                                tour = variante
                                melhor_FO = melhor_FO_nova
                                melhorou = True
                                break

                        if melhorou:
                            break
                    if melhorou:
                        break
                if melhorou:
                    break


        return melhor_FO, tour
