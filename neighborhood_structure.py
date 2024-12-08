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

class Reallocate(NeighborhoodStructure):

    def aplicar_relocate_primeiro_aprimorante(
        self, solucao: list[int], instance_handler: InstanceHandler, custo_corrente: int
    ):
        if solucao[0] == solucao[-1]:
            solucao = solucao[:-1]

        n = len(solucao)
        melhor_custo = custo_corrente  # Usa o custo inicial passado como parâmetro
        melhor_solucao = solucao[:]
        for i in range(n):  # Início da subsequência
            for j in range(i + 1, n + 1):  # Fim da subsequência
                subsequencia = solucao[i:j]  # Subsequência a ser relocada

                for k in range(n):  # Posição de reinserção
                    if k < i or k >= j:  # Evita reinserir na mesma posição
                        nova_solucao = solucao[:i] + solucao[j:]  # Remove a subsequência
                        nova_solucao = nova_solucao[:k] + subsequencia + nova_solucao[k:]  # Reinsere a subsequência
                        novo_custo = instance_handler.calcular_funcao_objetivo(solution=nova_solucao)
                        if novo_custo < melhor_custo:
                            melhor_custo = novo_custo
                            melhor_solucao = nova_solucao

        # Retorna a melhor solução encontrada
        return melhor_solucao, melhor_custo

    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ) -> tuple[int, list[int]] | tuple[None, None]:
        return self.aplicar_relocate_primeiro_aprimorante(solution, instance_handler, scost)
