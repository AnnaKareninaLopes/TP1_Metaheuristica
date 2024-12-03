import argparse
from typing import Union

from instance_handler import InstanceHandler
from optimization_methods import HeuristicMethods, LocalSearchMethods


def create_parser():
    parser = argparse.ArgumentParser(description="Execução do TSP com heurísticas")
    parser.add_argument("filename", type=str, help="Nome do arquivo de entrada")
    parser.add_argument(
        "output",
        type=str,
        help="nome do arquivo de saida para os resultados do benchmark",
    )
    parser.add_argument(
        "initial_node", type=int, help="Nó inicial onde vai começar o caminho do tsp"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--heuristic",
        dest="method",
        type=HeuristicMethods,
        help="Heurística a ser utilizada",
    )
    group.add_argument(
        "--local-search",
        dest="method",
        type=LocalSearchMethods,
        help="Método de busca local a ser utilizado",
    )
    return parser


def main():
    p = create_parser()
    args = p.parse_args()
    instance_handler = InstanceHandler(args.filename, args.output)

    method: Union[HeuristicMethods, LocalSearchMethods] = args.method

    # Nome do arquivo de saída
    arquivo_saida = args.output

    method.solve(instance_handler, args.initial_node)

    print(f"Resultados salvos em {arquivo_saida}")


if __name__ == "__main__":
    main()
