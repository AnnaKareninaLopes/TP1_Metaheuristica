from enum import Enum
import time
from typing import Type

from constructive_heuristics import (
    ConstructiveHeuristic,
    CheapestInsertion,
    Mst,
    NearestNeighbor,
)
from local_search.hill_climbing import HillClimbing
from neighborhood_structure import TwoOpt
from instance_handler import InstanceHandler


class HeuristicMethods(str, Enum):
    MST = "agm"
    CLOSEST_NEIGHBOR = "nn"
    CHEAPEST_INSERTION = "ci"

    def solve(self, instance_handler: InstanceHandler, start_city: int) -> None:
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


class LocalSearchMethods(str, Enum):
    LS2OPT = "ls2opt"

    def solve(self, instance_handler: InstanceHandler, start_city: int) -> None:
        neighborhood_struct_mapping = {
            LocalSearchMethods.LS2OPT: TwoOpt,
        }
        neighborhood_struct = neighborhood_struct_mapping[self]()
        start_time = time.time()
        local_search = HillClimbing(
            NearestNeighbor(instance_handler.cordenadas, start_city), neighborhood_struct
        )
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
