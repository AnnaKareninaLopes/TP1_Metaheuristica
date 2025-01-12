import argparse
from typing import Union

from instance_handler import InstanceHandler
from optimization_methods import HeuristicMethods, LocalSearchMethods, MetaheuristicRunner, GraspRunner

def create_parser():
    parser = argparse.ArgumentParser(description="Execução do TSP com heurísticas")
    parser.add_argument("filename", type=str, help="Nome do arquivo de entrada")
    parser.add_argument(
        "output",
        type=str,
        help="Nome do arquivo de saída para os resultados do benchmark",
    )
    parser.add_argument(
        "initial_node", type=int, help="Nó inicial onde vai começar o caminho do TSP"
    )

    subparsers = parser.add_subparsers(dest="method_type", required=True, help="Tipo de método a ser utilizado")

    heuristic_parser = subparsers.add_parser("heuristic", help="Heurística a ser utilizada")
    heuristic_parser.add_argument(
        "--method",
        type=HeuristicMethods,
        required=True,
        help="Heurística específica",
    )

    local_search_parser = subparsers.add_parser("local-search", help="Método de busca local a ser utilizado")
    local_search_parser.add_argument(
        "--method",
        type=LocalSearchMethods,
        required=True,
        help="Busca local específica",
    )

    grasp_parser = subparsers.add_parser("grasp", help="Metaheurística a ser utilizada")
    grasp_parser.add_argument(
        "--grasp-max-it",
        type=int,
        required=True,
        help="Número máximo de iterações para GRASP",
    )
    grasp_parser.add_argument(
        "--grasp-alpha",
        type=float,
        help="Fator de gulosidade ou aleatoriadade do GRASP",
    )
    grasp_parser.add_argument(
        "--with-vnd",
        action="store_true",
        help="Utilizar VND no GRASP",
    )
    grasp_parser.set_defaults(
        method=GraspRunner()
    )

    return parser

def main():
    p = create_parser()
    args = p.parse_args()
    instance_handler = InstanceHandler(args.filename, args.output)

    method: Union[HeuristicMethods, LocalSearchMethods, MetaheuristicRunner] = args.method

    # Nome do arquivo de saída
    arquivo_saida = args.output

    path = method.solve(instance_handler, args)

    print("Caminho encontrado:")
    print(path)
    print(f"Resultados salvos em {arquivo_saida}")


if __name__ == "__main__":
    main()
