import math
import os
import pandas as pd

def distancia_euclidiana_2d(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class InstanceHandler:

    # Lê o arquivo de corrdenas e retorna uma lista com elas
    def leitor_coordenadas_tsp(self, arquivo):
        with open(arquivo, "r", encoding='utf-8') as arquivo:
            coordenadas = []
            secao_coord = False

            for linha in arquivo:
                linha = linha.strip()
                if linha.startswith("NODE_COORD_SECTION"):
                    secao_coord = True
                    continue

                if secao_coord:
                    if linha == "EOF":
                        break
                    partes = linha.split()
                    x, y = float(partes[1]), float(partes[2])
                    coordenadas.append([x, y])

        return coordenadas


    # Função para obter o valor ótimo da instância
    def obter_otimo(self, arquivo_csv:str, nome_instancia:str):
        nome_instancia = os.path.basename(nome_instancia)
        df = pd.read_csv(arquivo_csv, thousands=".", decimal=",")

        # Acessa a linha correspondente à instância
        linha = df[df["Instancia"] == nome_instancia]

        if not linha.empty:
            return linha["Otimo"].values[0]  # Retorna o valor ótimo
        return None  # Retorna None se não encontrar a instância

    def __init__(
        self,
        filename: str,
        output_file: str,
    ):
        cordenadas = self.leitor_coordenadas_tsp(filename)
        optimal = self.obter_otimo('otimos.csv', filename)
        self.__input = filename
        self.cordenadas = cordenadas
        self.__optimal = optimal
        self.__output_file = output_file


    def save_results(
        self,
        solution: list[int],
        heuristic: str,
        city_initial: int,
        objective_function: int,
        execution_time: float,
    ):
        vertex_number = len(solution)
        edge_number = vertex_number*(vertex_number-1)/2
        gap = 100 * (abs(objective_function - self.__optimal) / self.__optimal)
        linha_dados = [
            self.__input,
            heuristic,
            str(city_initial),
            str(objective_function),
            str(self.__optimal),
            f"{gap:.2f}",
            f"{execution_time:.4f}",
            str(vertex_number),
            str(edge_number),
        ]
        if not os.path.exists(self.__output_file):
            cabecalho = [
                "INSTANCE",
                "METHOD",
                "PARAM",
                "OBJECTIVE_FUNCTION",
                "OPTIMUM",
                "GAP",
                "TIME",
                "NODES",
                "ARCS",
            ]
            df = pd.DataFrame([linha_dados], columns=cabecalho)
            with open(self.__output_file, "w", encoding="utf-8") as f:
                f.write(str(df.to_string(index=False, col_space=12, justify="left")))
            return
        with open(self.__output_file, "r", encoding="utf-8") as f:
            existing_data = pd.read_csv(self.__output_file, sep=r"\s+")
            new_data = pd.DataFrame([linha_dados], columns=existing_data.columns)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        with open(self.__output_file, "w", encoding="utf-8") as f:
            f.write(str(updated_data.to_string(index=False, col_space=12, justify="left")))

    def calcular_funcao_objetivo(self, solution: list[int]) -> int:
        total_distance = 0
        for city, neighbor in zip(solution, solution[1:]):
            distance = distancia_euclidiana_2d(self.cordenadas[city], self.cordenadas[neighbor])
            total_distance += distance
        return total_distance
