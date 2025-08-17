import streamlit as st
import pandas as pd
import os

def carregando_df(path: str = "") -> pd.DataFrame:
    """
    Função genérica para carregar DataFrames a partir de arquivos CSV.
    """
    if not path:
        st.error("Caminho do arquivo não fornecido. Por favor, forneça um caminho válido.")
        return pd.DataFrame()
    
    try:
        return pd.read_csv(os.path.abspath(path))
    except FileNotFoundError:
        st.warning(f"Arquivo não encontrado: {os.path.abspath(path)}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo {path}: {e}")
        return pd.DataFrame()

# Mapeamento dos nomes das variáveis aos arquivos CSV
arquivos_csv = {
    "df_circuitos": "data/circuits.csv",
    "df_construtores_resultados": "data/constructor_results.csv",
    "df_construtores": "data/constructors.csv",
    "df_pilotos_posicao": "data/driver_standings.csv",
    "df_pilotos": "data/drivers.csv",
    "df_tempo_de_volta": "data/lap_times.csv",
    "df_pit_stops": "data/pit_stops.csv",
    "df_qualificacao": "data/qualifying.csv",
    "df_corridas": "data/races.csv",
    "df_results": "data/results.csv",
    "df_temporadas": "data/seasons.csv",
    "df_sprints": "data/sprint_results.csv",
    "df_status": "data/status.csv"
}

# Carregamento automático dos DataFrames em um dicionário
dfs = {nome: carregando_df(caminho) for nome, caminho in arquivos_csv.items()}

# Desempacotar os DataFrames em variáveis individuais
globals().update(dfs)
