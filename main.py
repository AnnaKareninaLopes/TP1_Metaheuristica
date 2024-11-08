import random
import operacoes


if __name__ == "__main__":
    # Solicita o nome do arquivo ao usuário
    nome_arquivo = input("Digite o nome do arquivo: ")

    # Chamada da função para ler as coordenadas
    matriz_coordenadas = operacoes.leitor_coordenadas_tsp(nome_arquivo)
    print(matriz_coordenadas)

    otimo_instancia_dada = operacoes.obter_otimo('otimos.csv', nome_arquivo)
    print(f"Ótimo da instância dada: {otimo_instancia_dada}")

    # Seleciona um índice aleatório para a cidade inicial
    indice_cidade_inicial = random.randint(0, len(matriz_coordenadas) - 1)
    cidade_inicial = matriz_coordenadas[indice_cidade_inicial]
    print(f"Cidade inicial aleatória: {cidade_inicial}, cujo índice é {indice_cidade_inicial}")

    # Menu para selecionar a heurística
    print("\nSelecione a heurística para o TSP:")
    print("1. Vizinho Mais Próximo")
    print("2. Inserção Mais Barata")
    print("3. Árvore Geradora Mínima")

    escolha = input("Digite o número da heurística desejada: ")

    # Define a heurística escolhida com base na entrada do usuário
    if escolha == '1':
        heuristica = operacoes.heuristica_vizinho_mais_proximo
    elif escolha == '2':
        heuristica = operacoes.heuristica_insercao_mais_barata
    elif escolha == '3':
        heuristica = operacoes.heuristica_arvore_geradora_minima
    else:
        print("Escolha inválida! Selecione uma opção de 1 a 3.")
        exit(1)

    # Nome do arquivo de saída
    arquivo_saida = 'resultado_tsp.txt'

    # Executa o TSP com a heurística escolhida
    operacoes.executar_tsp(matriz_coordenadas, cidade_inicial, arquivo_saida, otimo_instancia_dada, heuristica)

    print(f"Resultados salvos em {arquivo_saida}")
