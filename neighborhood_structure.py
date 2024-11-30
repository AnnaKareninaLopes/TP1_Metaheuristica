from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Type

from instance_handler import InstanceHandler
class NeighborhoodStructure(ABC):

    @abstractmethod
    def get_better_neighbor(
        self,
        instance_handler: InstanceHandler,
        solution: list[int],
        current_cost: int
    ) -> Optional[int]:
        """
        get the best neighbor of a solution according with the specify
        neighborhood structure
        """

    @abstractmethod
    def get_neighbor(self, solution: list[int]) -> None:
        """
        get a neighbor of a solution according with the specify neighborhood,
        not necessarily the best, just a neighbor
        """

class Exchange(NeighborhoodStructure):

    def __calc_swap_cost(
        self,
        index: int,
        index2: int,
        instance_handler: InstanceHandler,
        solution: list[int],
    ) -> int:
        """
        calculate the swap cost of two elements in the solution
        """
        solution[index], solution[index2] = solution[index2], solution[index]
        cost = instance_handler.calcular_funcao_objetivo(solution)
        solution[index], solution[index2] = solution[index2], solution[index]
        return cost

    def get_better_neighbor(
        self,
        instance_handler: InstanceHandler,
        solution: list[int],
        current_cost: int
    ) -> bool:
        for index, _ in enumerate(solution):
            for index2, _ in enumerate(solution):
                if index != index2:
                    cost = self.__calc_swap_cost(index, index2, instance_handler, solution)
                    if cost < current_cost:
                        solution[index], solution[index2] = solution[index2], solution[index]
                        return cost
        return None

    def get_neighbor(self, solution: list[int]) -> None:
        pass

class NeighborhoodStructureEnum(str, Enum):
    EXCHANGE = "exchange"

    def get_neighborhood_structure_class(self) -> Type[NeighborhoodStructure]:
        neighborhood_structure_mapping = {
            NeighborhoodStructureEnum.EXCHANGE: Exchange
        }
        return neighborhood_structure_mapping[self]
