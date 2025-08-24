import os
from glob import glob
import pandas as pd


def carregar_dados() -> dict:
    """Função de carregar dados"""
    path = os.path.join(os.getcwd(), "data")
    # print(f"Caminho: {path}")
    
    files = glob(os.path.join(path, "*.csv"))
    if not files:
        print("Nenhum arquivo CSV encontrado!")
        return
    
    # print("Arquivos encontrados:", files)
    
    dicf = {}
    
    for f in files:
        nome = os.path.splitext(os.path.basename(f))[0]
        df = pd.read_csv(f, sep=',', na_values="\\N")
        dicf[nome] = df
    
    # print("DataFrames carregados:", list(dicf.keys()))

    return dicf

data_frames = carregar_dados()