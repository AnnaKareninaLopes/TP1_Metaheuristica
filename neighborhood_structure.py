from abc import ABC, abstractmethod
from enum import Enum
from typing import Generator, Type

class NeighborhoodStructure(ABC):

    @abstractmethod
    def enumerate_neighbors(self, solution: list[int]) -> Generator[list[int], None, None]:
        """
        Should enumerate all neighbors of a given current solution of according with a
        specify neighborhood structure
        """

class SwapDistant(NeighborhoodStructure):

    def enumerate_neighbors(self, solution: list[int]) -> Generator[list[int], None, None]:
        for index, _ in enumerate(solution):
            for index2, _ in enumerate(solution):
                solution[index], solution[index2] = solution[index2], solution[index]
                yield solution
                solution[index], solution[index2] = solution[index2], solution[index]



class NeighborhoodStructureEnum(str, Enum):
    SWAPDISTANT = "SwapDistant"

    def get_neighborhood_structure_class(self) -> Type[NeighborhoodStructure]:
        neighborhood_structure_mapping = {
            NeighborhoodStructureEnum.SWAPDISTANT: SwapDistant
        }
        return neighborhood_structure_mapping[self]
