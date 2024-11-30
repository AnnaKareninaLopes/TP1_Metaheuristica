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

class DeleteInsert(NeighborhoodStructure):

    def enumerate_neighbors(self, solution: list[int]) -> Generator[list[int], None, None]:
        for index, element in enumerate(solution):
            for index2, _ in enumerate(solution):
                if index != index2:
                    cp = solution.copy()
                    cp.pop(index)
                    cp.insert(index2, element)
                    yield cp

class NeighborhoodStructureEnum(str, Enum):
    SWAPDISTANT = "SwapDistant"
    DELETEINSERT = "DeleteInsert"

    def get_neighborhood_structure_class(self) -> Type[NeighborhoodStructure]:
        neighborhood_structure_mapping = {
            NeighborhoodStructureEnum.SWAPDISTANT: SwapDistant,
            NeighborhoodStructureEnum.DELETEINSERT: DeleteInsert,
        }
        return neighborhood_structure_mapping[self]
