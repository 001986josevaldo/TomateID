import csv
import os
from collections import Counter

class CruzamentoSaver:
    def __init__(self, output_dir="Relatorio"):
        """
        Inicializa o salvador de cruzamentos, criando o diretório de saída se necessário.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def salvar_csv(self, cruzamentos, input_video_path):
        """
        Salva o dicionário cruzamentos_registrados em um arquivo CSV com o nome do vídeo de entrada.
        
        :param cruzamentos: dicionário {obj_id: nomeClass}
        :param input_video_path: caminho do vídeo de entrada
        """
        # Gera o nome do arquivo baseado no vídeo de entrada
        base_name = os.path.splitext(os.path.basename(input_video_path))[0]
        filename = f"{base_name}.csv"
        path = os.path.join(self.output_dir, filename)

        # Salva o CSV
        with open(path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Classe"])
            for obj_id, nome_class in cruzamentos.items():
                writer.writerow([int(obj_id), nome_class])
                
        print(f"✅ Cruzamentos salvos em: {path}")

    def salvar_totais_csv(self, cruzamentos, input_video_path):
        """
        Gera um CSV com o total de cada classe a partir dos cruzamentos.
        
        :param cruzamentos: dicionário {obj_id: nomeClass}
        :param input_video_path: caminho do vídeo de entrada
        """
        base_name = os.path.splitext(os.path.basename(input_video_path))[0]
        filename = f"{base_name}_totais.csv"
        path = os.path.join(self.output_dir, filename)

        contador = Counter(cruzamentos.values())

        with open(path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Classe", "Total"])
            for classe, total in contador.items():
                writer.writerow([classe, total])
                
        print(f"✅ Totais por classe salvos em: {path}")