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


class TwoOpt(NeighborhoodStructure):

    def enumerate_neighbors(self, solution: list[int]) -> Generator[list[int], None, None]:
        for i, _ in enumerate(solution[:-1]):
            for j, _ in enumerate(solution[:-1]):
                if i != j:
                    solution[i+1], solution[j] = solution[j], solution[i+1]
                    yield solution
                    solution[i+1], solution[j] = solution[j], solution[i+1]

class NeighborhoodStructureEnum(str, Enum):
    TWOOPT = "TwoOpt"

    def get_neighborhood_structure_class(self) -> Type[NeighborhoodStructure]:
        neighborhood_structure_mapping = {
            NeighborhoodStructureEnum.TWOOPT: TwoOpt
        }
        return neighborhood_structure_mapping[self]
