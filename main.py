import argparse
import time

from constructive_heuristics import HeuristicsEnum
from local_search.hill_climbing import HillClimbing
from neighborhood_structure import NeighborhoodStructureEnum
from instance_handler import InstanceHandler

def run_local_search(
    initial_heuristic: HeuristicsEnum,
    instance_handler: InstanceHandler,
    first_city: int,
    neighborhood_structure: NeighborhoodStructureEnum,
):
    neighborhood_structure_class = neighborhood_structure.get_neighborhood_structure_class()
    neighborhood_structure_instance = neighborhood_structure_class()
    start_time = time.time()
    heuristic_class = initial_heuristic.get_heuristic_class()
    cordenadas = instance_handler.cordenadas
    heuristic = heuristic_class(cordenates=cordenadas, first_city=first_city)

    local_search = HillClimbing(heuristic, neighborhood_structure_instance)
    cost, solution = local_search.solve(instance_handler)

    end_time = time.time()
    execution_time = end_time - start_time
    instance_handler.save_results(
        solution=solution,
        heuristic=initial_heuristic,
        city_initial=first_city,
        objective_function=cost,
        execution_time=execution_time,
    )

def create_parser():
    parser = argparse.ArgumentParser(description="Execução do TSP com heurísticas")
    parser.add_argument(
        "filename",
        type=str,
        help="Nome do arquivo de entrada"
    )
    parser.add_argument(
        "output",
        type=str,
        help="nome do arquivo de saida para os resultados do benchmark"
    )
    parser.add_argument(
        "heuristic",
        type=HeuristicsEnum,
        help="Heurística a ser utilizada"
    )
    parser.add_argument(
        "neighborhood_structure",
        type=NeighborhoodStructureEnum,
        help="Estrutura de vizinhança a ser utilizada"
    )
    parser.add_argument(
        "initial_node",
        type=int,
        help="Nó inicial onde vai começar o caminho do tsp"
    )
    return parser

def main():
    p = create_parser()
    args = p.parse_args()
    instance_handler = InstanceHandler(args.filename, args.output)

    heuristic: HeuristicsEnum = args.heuristic
    neighborhood_structure: NeighborhoodStructureEnum = args.neighborhood_structure

    # Nome do arquivo de saída
    arquivo_saida = args.output

    # Executa o TSP com a heurística escolhida
    run_local_search(heuristic, instance_handler, args.initial_node, neighborhood_structure)

    print(f"Resultados salvos em {arquivo_saida}")

if __name__ == "__main__":
    main()
