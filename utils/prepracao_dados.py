import pandas as pd
from utils.get_info import *



def organizar_ids(df: pd.DataFrame, ids_prioritarios: list = None) -> pd.DataFrame:
    """Função para organizar os ID em primeiro no DF"""
    # Verificando se há ID prioritarios
    if ids_prioritarios is None:
        ids_prioritarios = ['raceId', 'driverId', 'constructorId', 'statusId', 'circuitId', 'resultId', 'ano', 'code', 'nome_completo', 'numero_do_piloto','nome_equipe']

    # Organizando
    ids = [col for col in ids_prioritarios if col in df.columns]

    return df[ids + [col for col in df.columns if col not in ids]]


def merge_tabelas() -> pd.DataFrame:
    """Função para dar merge nos dataframes que precisamos"""

    # Conseguindo os dataframes
    df_sprint = get_sprints_results()
    df_races_result = get_race_results()
    df_status = get_status_race()
    df_races = get_info_corrida()
    df_equipes = get_info_time()
    df_pilotos = get_info_pilotos()


    # Concatenando os df
    df_juntando = pd.concat([df_sprint, df_races_result])

    # Filtrandos as colunas necessárias para análise
    df_races = df_races[['raceId', 'ano', 'circuitId', 'name_circuit']]
    df_pilotos = df_pilotos[['driverId','nome_completo', 'code']]
    df_equipes = df_equipes[['constructorId','nome_equipe', 'cores']]

    # Dando Merge
    df_juntando_tudo = pd.merge(df_races, df_juntando, on="raceId")
    df_juntando_tudo = pd.merge(df_juntando_tudo, df_status, on="statusId")
    df_juntando_tudo = pd.merge(df_juntando_tudo, df_equipes, on="constructorId")
    df_juntando_tudo = pd.merge(df_juntando_tudo, df_pilotos, on="driverId")

    # Filtrando Dados apenas dos anos que Lewis Hamilton participou da temporada
    df_juntando_tudo = df_juntando_tudo[df_juntando_tudo['ano'] >= 2007]

    df_juntando_tudo['posicao_final'] = pd.to_numeric(df_juntando_tudo['posicao_final'], errors='coerce')
    df_juntando_tudo['posicao_grid'] = pd.to_numeric(df_juntando_tudo['posicao_grid'], errors='coerce')

    df_juntando_tudo['ganho_posicao'] = df_juntando_tudo['posicao_grid'] - df_juntando_tudo['posicao_final']

    # Organizando ids
    df_juntando_tudo = organizar_ids(df_juntando_tudo)

    return df_juntando_tudo


def df_especifico() -> pd.DataFrame:
    """Função para fazer o DataFrame especifico"""
    # Chamando a função das merge das tabelas
    df_merge = merge_tabelas()

    # Filtrando pelo código
    df_merge = df_merge[df_merge['code'] == 'HAM']

    # Criando colunas
    df_merge['vitorias'] = df_merge['posicao_final'] == 1 

    return df_merge



