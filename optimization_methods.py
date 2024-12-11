from enum import Enum
import time
from typing import Callable, Type

from constructive_heuristics import (
    ConstructiveHeuristic,
    CheapestInsertion,
    Mst,
    NearestNeighbor,
)
from local_search import LocalSearch, HillClimbing, VND
from neighborhood_structure import Reallocate, Swap, SwapDistance,  TwoOpt
from instance_handler import InstanceHandler


class HeuristicMethods(str, Enum):
    MST = "agm"
    CLOSEST_NEIGHBOR = "nn"
    CHEAPEST_INSERTION = "ci"

    def solve(self, instance_handler: InstanceHandler, start_city: int) -> list[int]:
        heuristic_mapping: dict[HeuristicMethods, Type[ConstructiveHeuristic]] = {
            HeuristicMethods.MST: Mst,
            HeuristicMethods.CLOSEST_NEIGHBOR: NearestNeighbor,
            HeuristicMethods.CHEAPEST_INSERTION: CheapestInsertion,
        }
        class_method = heuristic_mapping[self]
        start_time = time.time()
        heuristic = class_method(instance_handler.cordenadas, start_city)
        path = heuristic.solve()
        end_time = time.time()
        run_time = end_time - start_time
        cost = instance_handler.calcular_funcao_objetivo(path)
        instance_handler.save_results(
            solution=path,
            heuristic=self.value,
            city_initial=start_city,
            objective_function=cost,
            execution_time=run_time,
        )
        return [city+1 for city in path]


class LocalSearchMethods(str, Enum):
    LS2OPT = "ls2opt"
    LSREALLOCATE = "lsreallocate"
    SWAP = "lsswap"
    VND = "vnd"

    def solve(self, instance_handler: InstanceHandler, start_city: int) -> list[int]:
        neighborhood_struct_mapping: dict[str, Callable[[InstanceHandler, int], LocalSearch]] = {
            LocalSearchMethods.LS2OPT: lambda ih, start: HillClimbing(NearestNeighbor(ih.cordenadas, start), TwoOpt()),
            LocalSearchMethods.LSREALLOCATE: lambda ih, start: HillClimbing(NearestNeighbor(ih.cordenadas, start), Reallocate()),
            LocalSearchMethods.SWAP: lambda ih, start: HillClimbing(NearestNeighbor(ih.cordenadas, start), Swap()),
            LocalSearchMethods.VND: lambda ih, start: VND(NearestNeighbor(ih.cordenadas, start), [TwoOpt(), SwapDistance(), Reallocate()])
        }
        start_time = time.time()
        local_search = neighborhood_struct_mapping[self](instance_handler, start_city)
        cost, path = local_search.solve(instance_handler)
        end_time = time.time()
        run_time = end_time - start_time
        instance_handler.save_results(
            solution=path,
            heuristic=self.value,
            city_initial=start_city,
            objective_function=cost,
            execution_time=run_time,
        )
        return [city+1 for city in path]
