# ==============================
# Módulo de funções de pilotos
# ==============================

import pandas as pd
from utils.data_frames import *

# ------------------------------
# Função genérica de carregamento
# ------------------------------
def carregar_dados(entidade_df: pd.DataFrame, filtros: dict = None, joins: list[dict] = None, remover_ids: bool = True) -> pd.DataFrame:
    """
    Carrega dados genéricos com base em filtros e junções.

    Args:
        entidade_df (pd.DataFrame): DataFrame base da entidade (ex: pilotos)
        filtros (dict): Campos e valores para filtrar
        joins (list[dict]): Lista de joins [{'df': ..., 'on': ..., 'how': ...}]
        remover_ids (bool): Remove colunas que terminam com 'Id' (case-insensitive)

    Returns:
        pd.DataFrame: DataFrame filtrado e unido
    """
    df = entidade_df.copy()

    # Aplicar filtros
    if filtros:
        for col, val in filtros.items():
            df = df[df[col] == val]

    if df.empty:
        print("Nenhum dado encontrado com os filtros fornecidos.")
        return pd.DataFrame()

    # Aplicar joins
    resultado = df.copy()
    if joins:
        for join in joins:
            jdf = join['df']
            on = join['on']
            how = join.get('how', 'left')
            resultado = resultado.merge(jdf, on=on, how=how)

    # Remover colunas de ID
    if remover_ids:
        resultado = resultado.loc[:, ~resultado.columns.str.lower().str.endswith("id")]

    return resultado

# ------------------------------
# Funções específicas
# ------------------------------
def get_corridas_piloto(name: str = "", surname: str = "") -> pd.DataFrame:
    """Retorna todas as corridas de um piloto com dados de construtor e status."""
    filtros = {}
    if name:
        filtros['forename'] = name
    if surname:
        filtros['surname'] = surname

    return carregar_dados(
        entidade_df=df_pilotos,
        filtros=filtros,
        joins=[
            {'df': df_results, 'on': 'driverId'},
            {'df': df_corridas, 'on': 'raceId'},
            {'df': df_status, 'on': 'statusId'},
            {'df': df_construtores, 'on': 'constructorId'}
        ]
    )

def get_piloto_info(name: str = "", surname: str = "") -> pd.DataFrame:
    """Retorna informações básicas de um piloto."""
    filtros = {}
    if name:
        filtros['forename'] = name
    if surname:
        filtros['surname'] = surname

    return carregar_dados(
        entidade_df=df_pilotos,
        filtros=filtros,
        joins=[],
        remover_ids=False
    )

def get_sprints_piloto(name: str = "", surname: str = "") -> pd.DataFrame:
    """Retorna todas as corridas sprint de um piloto com dados de construtor e status."""
    filtros = {}
    if name:
        filtros['forename'] = name
    if surname:
        filtros['surname'] = surname

    return carregar_dados(
        entidade_df=df_pilotos,
        filtros=filtros,
        joins=[
            {'df': df_sprints, 'on': 'driverId'},
            {'df': df_construtores, 'on': 'constructorId'},
            {'df': df_corridas, 'on': 'raceId'},
            {'df': df_status, 'on': 'statusId'}
        ]
    )

# ------------------------------
# Estatísticas
# ------------------------------
def get_estatisticas_piloto(name: str, surname: str) -> dict:
    """Retorna estatísticas gerais de um piloto."""
    corridas = get_corridas_piloto(name, surname)
    sprints = get_sprints_piloto(name, surname)

    stats = {}

    # Corridas
    if not corridas.empty:
        stats["total_corridas"] = len(corridas)
        stats["vitorias"] = (corridas["positionOrder"] == 1).sum()
        stats["podios"] = (corridas["positionOrder"] <= 3).sum()
        stats["abandono"] = corridas["status"].str.contains(
            "Accident|Collision|Engine|Gearbox", case=False, na=False
        ).sum()
        stats["media_posicao_final"] = corridas["positionOrder"].mean().round(2)
        stats["melhor_posicao"] = corridas["positionOrder"].min()

    # Sprints
    if not sprints.empty:
        stats["total_sprints"] = len(sprints)
        stats["vitorias_sprint"] = (sprints["positionOrder"] == 1).sum()
        stats["podios_sprint"] = (sprints["positionOrder"] <= 3).sum()

    return stats

# ------------------------------
# Desempenho por temporada
# ------------------------------
def desempenho_por_temporada(name: str, surname: str) -> pd.DataFrame:
    """Retorna a média da posição final do piloto por temporada."""
    corridas = get_corridas_piloto(name, surname)
    if corridas.empty:
        return pd.DataFrame()

    desempenho = (
        corridas.groupby("year")["positionOrder"]
        .mean()
        .reset_index()
        .rename(columns={"positionOrder": "media_posicao"})
    )
    return desempenho

# ------------------------------
# Grid vs Resultado
# ------------------------------
def grid_vs_resultado(name: str, surname: str) -> pd.DataFrame:
    """Retorna a diferença entre posição de largada (grid) e posição final."""
    corridas = get_corridas_piloto(name, surname)
    if corridas.empty:
        return pd.DataFrame()

    corridas["ganho_posicoes"] = corridas["grid"].fillna(0) - corridas["positionOrder"].fillna(0)
    return corridas[["raceId", "name", "year", "grid", "positionOrder", "ganho_posicoes"]]
