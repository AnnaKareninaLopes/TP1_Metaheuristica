from .base import ConstructiveHeuristic

class CheapestInsertion(ConstructiveHeuristic):

    def inicio_heuristica(self, matriz_distancias, dicionario, cidade_inicial):
        # Inicializa o vetor de candidatos com todas as cidades (exceto a cidade inicial)
        vetor_candidatos = list(dicionario.keys())
        vetor_candidatos.remove(cidade_inicial)  # Remover a cidade inicial dos candidatos
        vetor_solucao = [cidade_inicial]  # Começa a solução com a cidade inicial
        distancias_total = 0

        # Obtém a cidade mais próxima da cidade inicial
        cidade_atual = cidade_inicial
        cidade_proxima = dicionario[cidade_atual][0]  # Acessa diretamente a cidade mais próxima
        distancia_primeiro_traco = matriz_distancias[cidade_atual][cidade_proxima]  # Distância até a primeira cidade
        distancias_total += distancia_primeiro_traco  # Adiciona a distância
        vetor_solucao.append(cidade_proxima)

        # Remover a cidade já visitada do vetor de candidatos
        vetor_candidatos.remove(cidade_proxima)

        # Segunda cidade: mais próxima da cidade inicial e da cidade já conectada
        cidade_atual = cidade_proxima

        # Excluir as cidades já visitadas (cidade_inicial e cidade_proxima)
        cidades_visitadas = set(vetor_solucao)
        cidades_disponiveis = [cidade for cidade in dicionario[cidade_inicial] + dicionario[cidade_atual]
                            if cidade not in cidades_visitadas]  # Exclui as cidades já visitadas

        cidade_proxima_2 = min(
            cidades_disponiveis,
            key=lambda x: matriz_distancias[cidade_inicial][x]  # Ordena pela distância
        )
        distancia_segundo_traco = matriz_distancias[cidade_inicial][cidade_proxima_2]
        distancias_total += distancia_segundo_traco  # Adiciona a distância
        vetor_solucao.append(cidade_proxima_2)

        # Remover a cidade já visitada do vetor de candidatos
        vetor_candidatos.remove(cidade_proxima_2)

        # Agora, o ciclo é fechado: cidade_proxima_2 -> cidade_inicial
        distancia_fechamento = matriz_distancias[cidade_proxima_2][cidade_inicial]
        distancias_total += distancia_fechamento  # Adiciona a distância de fechamento
        vetor_solucao.append(cidade_inicial)

        return vetor_solucao, distancias_total

    def heuristica_insercao_mais_barata(self, dicionario, vetor_solucao, distancias_total, matriz_distancias):
        # Candidatos são todas as cidades que ainda não foram visitadas
        vetor_candidatos = list(dicionario.keys())
        # Remove as cidades já presentes no vetor de solução
        for cidade in vetor_solucao:
            if cidade in vetor_candidatos:
                vetor_candidatos.remove(cidade)

        # Enquanto houver cidades candidatas
        while vetor_candidatos:
            menor_custo = float('inf')
            melhor_candidato = None
            melhor_posicao = None

            # Para cada cidade candidata, tentamos inseri-la em todas as posições do vetor_solucao
            for candidato in vetor_candidatos:
                for i in range(1, len(vetor_solucao)):
                    cidade_anterior = vetor_solucao[i]
                    cidade_posterior = vetor_solucao[i]
                    # Cálculo do custo de inserção: a distância total entre cidades será alterada
                    custo = (matriz_distancias[cidade_anterior][candidato] +
                            matriz_distancias[candidato][cidade_posterior] -
                            matriz_distancias[cidade_anterior][cidade_posterior])

                    # Verifica se o custo calculado é o menor custo encontrado até agora
                    if custo < menor_custo:
                        menor_custo = custo
                        melhor_candidato = candidato
                        melhor_posicao = i

            # Atualiza a solução com a cidade candidata escolhida e a posição
            vetor_solucao.insert(melhor_posicao, melhor_candidato)
            # Atualiza a distância total com o menor custo encontrado
            distancias_total += menor_custo
            # Remove a cidade candidata do vetor de candidatos
            vetor_candidatos.remove(melhor_candidato)

        return vetor_solucao, distancias_total

    def __init__(self, cordenates: list[list[int, int]], first_city: int):
        matriz_distancias = self.criar_matriz_distancias(cordenates)
        self.cordenates = cordenates
        self.dicionario_ordenado = self.criar_dicionario_cidades_ordenadas(matriz_distancias)
        self.matriz_distancias = matriz_distancias
        self.first_city = first_city

    def solve(self):
        solucao_inicial = self.inicio_heuristica(self.matriz_distancias, self.dicionario_ordenado, self.first_city)
        solucao, distancia = self.heuristica_insercao_mais_barata(self.dicionario_ordenado, *solucao_inicial, self.matriz_distancias)
        return solucao, distancia
