from abc import ABC, abstractmethod


class ConstructiveHeuristic(ABC):

    @abstractmethod
    def __init__(
        self,
        cordenates: list[list[int, int]],
        first_city: int
    ):
        pass

    @abstractmethod
    def solve(self) -> list[int]:
        pass
