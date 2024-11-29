import argparse

import operacoes

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
        type=operacoes.Heuristics,
        help="Heurística a ser utilizada"
    )
    parser.add_argument(
        "initial_node",
        type=int,
        help="Nó inicial onde vai começar o caminho do tsp"
    )
    return parser

if __name__ == "__main__":
    p = create_parser()
    args = p.parse_args()
    matriz_coordenadas = operacoes.leitor_coordenadas_tsp(args.filename)
    print(matriz_coordenadas)

    otimo_instancia_dada = operacoes.obter_otimo('otimos.csv', args.filename)
    print(f"Ótimo da instância dada: {otimo_instancia_dada}")

    # Seleciona um índice aleatório para a cidade inicial
    indice_cidade_inicial = args.initial_node
    cidade_inicial = matriz_coordenadas[indice_cidade_inicial]
    print(f"Cidade inicial aleatória: {cidade_inicial}, cujo índice é {indice_cidade_inicial}")

    heuristic: operacoes.Heuristics = args.heuristic

    # Nome do arquivo de saída
    arquivo_saida = args.output

    # Executa o TSP com a heurística escolhida
    operacoes.run_constructive_heuristic(matriz_coordenadas, cidade_inicial, args.filename, arquivo_saida, otimo_instancia_dada, heuristic)

    print(f"Resultados salvos em {arquivo_saida}")
