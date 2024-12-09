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

    def realocate(
        self, i: int, j: int, s_at: list[int], s_ofv: int, instance_handler: InstanceHandler
    ):
        """
        Realoca a subsequência de `s_at[i]` a `s_at[i+1]` para a posição `j`, recalculando o custo total.
        
        Delta1 = custo dos arcos que envolvem `i` e `i+1` antes da realocação.
        Delta2 = custo dos arcos que envolvem `j` e `j+1` após a realocação.
        """

        delta1 = (
            instance_handler.calculate_isolated_cost(s_at[i - 1], s_at[i]) +
            instance_handler.calculate_isolated_cost(s_at[j], s_at[j + 1])
        )

        delta2 = (
            instance_handler.calculate_isolated_cost(s_at[i-1], s_at[j]) +
            instance_handler.calculate_isolated_cost(s_at[i], s_at[j + 1])
        )

        FONova = s_ofv - delta1 + delta2

        return FONova

    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ) -> tuple[int, list[int]] | tuple[None, None]:
        n = len(solution)
        solucao_atual = solution[:]
        fo_atual = scost
        melhor_solucao = None
        melhor_FO = None

        for i in range(1, n-1):
            for j in range(i + 1, n-1):
                FONova = self.realocate(i, j, solucao_atual, fo_atual, instance_handler)

                if FONova < scost:
                    fo_atual = FONova
                    solucao_atual[i:j + 1] = solucao_atual[i:j + 1][::-1]

        return melhor_FO, melhor_solucao

class Swap(NeighborhoodStructure):

    def swap(self, instance_handler: InstanceHandler, i: int, n:int,  solucao: list[int], FO: int):
        n = len(solucao)
        solucao_vizinha = solucao[:]
        print("Tamanho solução na função swap: ", n)
        print("Solução na função swap: ", solucao_vizinha)

        # Inicializando deltas
        delta1 = 0
        delta2 = 0

        print(f"Tentando realizar o swap no índice {i}...")


        if i == 0:
            delta1 = (
                instance_handler.calculate_isolated_cost(solucao[n-2], solucao[n-1])
                + instance_handler.calculate_isolated_cost(solucao[1], solucao[2])
            )
            delta2 = (
                instance_handler.calculate_isolated_cost(solucao[0], solucao[2])
                + instance_handler.calculate_isolated_cost(solucao[n-2], solucao[1])
            )
            return FO - delta1 + delta2
        elif i == n-2:
            delta1 = (
                instance_handler.calculate_isolated_cost(solucao[n-3], solucao[n-2])
                + instance_handler.calculate_isolated_cost(solucao[0], solucao[1])
            )
            delta2 = (
                instance_handler.calculate_isolated_cost(solucao[n-3], solucao[n-1])
                + instance_handler.calculate_isolated_cost(solucao[n-2], solucao[1])
            )
            return FO - delta1 + delta2
        else:
            delta1 = (
                instance_handler.calculate_isolated_cost(solucao[i-1], solucao[i])
                + instance_handler.calculate_isolated_cost(solucao[i+1], solucao[i+2])
            )
            delta2 = (
                instance_handler.calculate_isolated_cost(solucao[i-1], solucao[i+1])
                + instance_handler.calculate_isolated_cost(solucao[i], solucao[i+2])
            )
            return FO - delta1 + delta2


    def busca_local_swap(self, instance_handler: InstanceHandler, solucao, FO):

        n = len(solucao)
        solucao_atual = solucao[:]
        FO_atual = FO
        melhor_solucao = None
        melhor_FO = None

        for i in range(0, n - 1):
            FOvizinho = self.swap(instance_handler, i, n, solucao_atual, FO_atual)

            if FOvizinho < FO_atual:
                FO_atual = FOvizinho
                solucao_atual[i], solucao_atual[i + 1] = solucao_atual[i + 1], solucao_atual[i]
                if i == 0:
                    solucao_atual[-1] = solucao_atual[0]
                elif i == n-2:
                    solucao_atual[0] = solucao_atual[-1]
                melhor_solucao = solucao_atual
                melhor_FO = FO_atual

        return melhor_FO, melhor_solucao
    def improve(
        self, instance_handler: InstanceHandler, scost: int, solution: list[int]
    ):
        return self.busca_local_swap(instance_handler, solution, scost)
