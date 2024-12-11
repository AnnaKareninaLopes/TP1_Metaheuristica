from abc import ABC, abstractmethod

from instance_handler import InstanceHandler

class LocalSearch(ABC):

    @abstractmethod
    def solve(self, instance_handler: InstanceHandler) -> tuple[int, list[int]]:
        """
        Should solve a tsp instance using some local search algorithm
        """
