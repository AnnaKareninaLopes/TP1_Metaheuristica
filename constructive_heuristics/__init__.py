from enum import Enum
from typing import Type

from .base import ConstructiveHeuristic
from .ci import CheapestInsertion
from .nn import NearestNeighbor
from .mst import Mst

class HeuristicsEnum(str, Enum):
    MST = "agm"
    CLOSEST_NEIGHBOR = "nn"
    CHEAPEST_INSERTION = "ci"

    def get_heuristic_class(self) -> Type[ConstructiveHeuristic]:
        heuristic_mapping = {
            HeuristicsEnum.MST: Mst,
            HeuristicsEnum.CLOSEST_NEIGHBOR: NearestNeighbor,
            HeuristicsEnum.CHEAPEST_INSERTION: CheapestInsertion,
        }
        return heuristic_mapping[self]
