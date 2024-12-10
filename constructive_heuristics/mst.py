import heapq
from functools import reduce

from .base import ConstructiveHeuristic


class Mst(ConstructiveHeuristic):
    def __gen_edge_matrix(
        self, cordenates: list[list[int, int]]
    ) -> dict[int, list[tuple[int, int]]]:
        """
        Generate a dict to mapping each node to your edges list
        in a heap struct
        """
        edge_matrix = {}
        edge_list = None
        for node, (cordx, cordy) in enumerate(cordenates):
            edge_list = edge_matrix.get(node, [])
            for node2, (cordx2, cordy2) in enumerate(cordenates):
                if node != node2:
                    edge_list.append(
                        (
                            ((cordx - cordx2) ** 2 + (cordy - cordy2) ** 2) ** 0.5,
                            node,
                            node2,
                        )
                    )
            edge_matrix[node] = edge_list
            heapq.heapify(edge_matrix[node])
        return edge_matrix

    def __get_first_unconnected(
        self, visited: set[int], adjacent_to_tree: list[tuple[int, int]]
    ):
        _, _, to = adjacent_to_tree[0]
        while to in visited:
            heapq.heappop(adjacent_to_tree)
            _, _, to = adjacent_to_tree[0]
        min_edge = heapq.heappop(adjacent_to_tree)
        return min_edge

    def __gen_mst(self, edge_matrix: dict[int, list[tuple[int, int]]], first_city: int):
        mst = {first_city: []}
        visited = {
            first_city,
        }
        adjacent_to_tree = edge_matrix[first_city]
        visited.add(first_city)
        for _ in range(len(edge_matrix) - 1):
            _, from_node, to_node = self.__get_first_unconnected(
                visited, adjacent_to_tree
            )
            from_childrens = mst.get(from_node, [])
            from_childrens.append(to_node)
            mst[from_node] = from_childrens
            visited.add(to_node)
            visited.add(from_node)
            adjacent_to_tree += edge_matrix[to_node]
            heapq.heapify(adjacent_to_tree)
        return mst

    def __init__(self, cordenates: list[list[int, int]], first_city: int):
        edge_matrix: dict[int, list[tuple[int, int]]] = self.__gen_edge_matrix(
            cordenates
        )
        self.__first_city = first_city
        self.__mst = self.__gen_mst(edge_matrix, first_city)

    def solve(self):
        """
        Makes a pre ordem walking in mst to extract a possible solution to tsp
        """

        def walk(current: int) -> list[int]:
            return reduce(
                lambda x, y: x + y,
                [walk(node) for node in self.__mst.get(current, [])],
                [current],
            )

        return walk(self.__first_city) + [self.__first_city]
