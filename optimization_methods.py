from abc import ABC, abstractmethod
from argparse import Namespace
from enum import Enum
import time
from typing import Callable, Type

from constructive_heuristics import (
    ConstructiveHeuristic,
    CheapestInsertion,
    Mst,
    NearestNeighbor,
)
from local_search import CircularSearch, LocalSearch, HillClimbing, VND
from metaheuristics import Grasp
from neighborhood_structure import Reallocate, Swap, SwapDistance, TwoOpt
from instance_handler import InstanceHandler


class HeuristicMethods(str, Enum):
    MST = "agm"
    CLOSEST_NEIGHBOR = "nn"
    CHEAPEST_INSERTION = "ci"

    def solve(self, instance_handler: InstanceHandler, args: Namespace) -> list[int]:
        start_city = args.initial_node
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
        return [city + 1 for city in path]


class LocalSearchMethods(str, Enum):
    LS2OPT = "ls2opt"
    LSREALLOCATE = "lsreallocate"
    SWAP = "lsswap"
    VNDTSR = "vndtsr"
    VNDTRS = "vndtrs"
    VNDSTR = "vndstr"
    VNDSRT = "vndsrt"
    VNDRTS = "vndrts"
    VNDRST = "vndrst"
    CSTSR = "cstsr"

    def solve(self, instance_handler: InstanceHandler, args: Namespace) -> list[int]:
        start_city = args.initial_node
        neighborhood_struct_mapping: dict[str, Callable[[InstanceHandler, int], tuple[ConstructiveHeuristic, LocalSearch]]] = {
            LocalSearchMethods.LS2OPT: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), HillClimbing(TwoOpt())),
            LocalSearchMethods.LSREALLOCATE: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), HillClimbing(Reallocate())),
            LocalSearchMethods.SWAP: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), HillClimbing(Swap())),
            LocalSearchMethods.VNDTSR: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), VND([TwoOpt(), SwapDistance(), Reallocate()])),
            LocalSearchMethods.VNDTRS: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), VND([TwoOpt(), Reallocate(), Swap()])),
            LocalSearchMethods.VNDSTR: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), VND([Swap(), TwoOpt(), Reallocate()])),
            LocalSearchMethods.VNDSRT: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), VND([Swap(), Reallocate(), TwoOpt()])),
            LocalSearchMethods.VNDRTS: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), VND([Reallocate(), TwoOpt(), Swap()])),
            LocalSearchMethods.VNDRST: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), VND([Reallocate(), Swap(), TwoOpt()])),
            LocalSearchMethods.CSTSR: lambda ih, start: (NearestNeighbor(ih.cordenadas, start), CircularSearch([TwoOpt(), Swap(), Reallocate()]))
        }
        start_time = time.time()
        constructive_heuristic, local_search = neighborhood_struct_mapping[self](instance_handler, start_city)
        initial_solution = constructive_heuristic.solve()
        cost, path = local_search.solve(initial_solution, instance_handler)
        end_time = time.time()
        run_time = end_time - start_time
        instance_handler.save_results(
            solution=path,
            heuristic=self.value,
            city_initial=start_city,
            objective_function=cost,
            execution_time=run_time,
        )
        return [city + 1 for city in path]


class MetaheuristicRunner(ABC):

    @abstractmethod
    def solve(self, instance_handler: InstanceHandler, args: Namespace) -> list[int]:
        pass

class GraspRunner(MetaheuristicRunner):

    def solve(self, instance_handler: InstanceHandler, args: Namespace) -> list[int]:
        start_city = args.initial_node
        alpha = args.grasp_alpha
        max_it = args.grasp_max_it
        with_vnd = args.with_vnd
        heuristic_name = "GRASP_" + ("VND" if with_vnd else "HILLCLIMBING")
        local_search = VND([TwoOpt(), SwapDistance(), Reallocate()]) if with_vnd else HillClimbing(TwoOpt())
        start_time = time.time()
        grasp = Grasp(alpha, start_city, local_search, max_it)
        cost, path = grasp.solve(instance_handler)
        end_time = time.time()
        run_time = end_time - start_time
        instance_handler.save_results(
            solution=path,
            heuristic=heuristic_name,
            city_initial=start_city,
            objective_function=cost,
            execution_time=run_time,
            MAX_IT=max_it,
            ALPHA=alpha,
        )
        return [city + 1 for city in path]
