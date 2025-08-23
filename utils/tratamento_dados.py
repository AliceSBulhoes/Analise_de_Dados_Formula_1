import pandas as pd
from datetime import datetime as dt
from utils.data_frames import *

# Variável global
EQUIPES_CORES = {
    'McLaren': ['#FF8700', '#47C7FC'],  # Laranja (Papaya) e Azul
    'BMW Sauber': ['#FFFFFF', '#0066CC', '#CC0000'],  # Branco, Azul BMW, Vermelho
    'Williams': ['#005AFF', '#FFFFFF'],  # Azul Williams e Branco
    'Renault': ['#FFD800', '#000000'],  # Amarelo e Preto
    'Toro Rosso': ['#00008B', '#CC0000'],  # Azul Escuro e Vermelho
    'Ferrari': ['#DC0000'],  # Vermelho Ferrari
    'Toyota': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Super Aguri': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Red Bull': ['#00008B', '#CC0000', '#FFD800'],  # Azul Escuro, Vermelho, Amarelo
    'Force India': ['#FF80C7', '#FF8000', '#FFFFFF'],  # Rosa, Laranja, Branco (2017)
    'Honda': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Spyker': ['#FF8000', '#C0C0C0'],  # Laranja e Prata
    'MF1': ['#CC0000', '#FFFFFF'],  # Vermelho e Branco
    'Spyker MF1': ['#FF8000', '#C0C0C0'],  # Laranja e Prata
    'Sauber': ['#FFFFFF', '#0066CC', '#CC0000'],  # Branco, Azul, Vermelho
    'BAR': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Jordan': ['#FFD800', '#000000'],  # Amarelo e Preto
    'Minardi': ['#000000', '#CC0000', '#FFFFFF'],  # Preto, Vermelho, Branco
    'Jaguar': ['#006400', '#000000'],  # Verde Jaguar e Preto
    'Prost': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Arrows': ['#FF8000', '#000000'],  # Laranja e Preto
    'Benetton': ['#006400', '#00008B', '#FFD800'],  # Verde, Azul, Amarelo
    'Brawn': ['#FFFFFF', '#FFD800', '#000000'],  # Branco, Amarelo, Preto (2009)
    'Stewart': ['#FFFFFF', '#CC0000', '#005AFF'],  # Branco, Vermelho, Azul
    'Tyrrell': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Lola': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Ligier': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Forti': ['#FFD800', '#005AFF'],  # Amarelo e Azul
    'Footwork': ['#000000', '#FFFFFF', '#FF80C7'],  # Preto, Branco, Rosa
    'Pacific': ['#00008B', '#FFFFFF'],  # Azul Escuro e Branco
    'Simtek': ['#000000', '#FFFFFF'],  # Preto e Branco
    'Team Lotus': ['#000000', '#FFD700'],  # Preto e Dourado
    'Larrousse': ['#FFD800', '#005AFF'],  # Amarelo e Azul
    'Brabham': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Dallara': ['#FFD800', '#005AFF'],  # Amarelo e Azul
    'Fondmetal': ['#FFD700', '#000000'],  # Dourado e Preto
    'March': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Andrea Moda': ['#000000', '#FFFFFF'],  # Preto e Branco
    'AGS': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Lambo': ['#FFD800', '#000000'],  # Amarelo e Preto
    'Leyton House': ['#00008B', '#FFFFFF'],  # Azul Escuro e Branco
    'Coloni': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Euro Brun': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Osella': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Onyx': ['#000000', '#FFFFFF'],  # Preto e Branco
    'Life': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Rial': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Zakspeed': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'RAM': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Alfa Romeo': ['#CC0000', '#FFFFFF'],  # Vermelho e Branco
    'Spirit': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Toleman': ['#000000', '#FFFFFF', '#FFD800'],  # Preto, Branco, Amarelo
    'ATS': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Theodore': ['#000000', '#FFD700'],  # Preto e Dourado
    'Fittipaldi': ['#FFD800', '#005AFF'],  # Amarelo e Azul
    'Ensign': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Shadow': ['#000000', '#FFFFFF'],  # Preto e Branco
    'Wolf': ['#000000', '#FFD700'],  # Preto e Dourado
    'Merzario': ['#CC0000', '#FFFFFF'],  # Vermelho e Branco
    'Kauhsen': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Rebaque': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Surtees': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Hesketh': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Martini': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'BRM': ['#006400', '#FFFFFF'],  # Verde BRM e Branco
    'Penske': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'LEC': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'McGuire': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Boro': ['#FF8000', '#FFFFFF'],  # Laranja e Branco
    'Apollon': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Kojima': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Parnelli': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Maki': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Embassy Hill': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Lyncar': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Trojan': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Amon': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Token': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Iso Marlboro': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Tecno': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Matra': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Politoys': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Connew': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Bellasi': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'De Tomaso': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Cooper': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Eagle': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'LDS': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Protos': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Shannon': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Scirocco': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'RE': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'BRP': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Porsche': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Derrington': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Gilby': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Stebro': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Emeryson': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'ENB': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'JBW': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Ferguson': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'MBM': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Behra-Porsche': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Maserati': ['#006400', '#000000'],  # Verde Maserati e Preto
    'Scarab': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Watson': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Epperly': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Phillips': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Lesovsky': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Trevis': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Meskowski': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Kurtis Kraft': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Kuzma': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Christensen': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Ewing': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Aston Martin': ['#006400', '#000000'],  # Verde Aston e Preto
    'Vanwall': ['#006400', '#FFFFFF'],  # Verde e Branco
    'Moore': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Dunn': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Elder': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Sutton': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Fry': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Tec-Mec': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Connaught': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Alta': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'OSCA': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Gordini': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Stevens': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Bugatti': ['#000000', '#FFFFFF'],  # Preto e Branco
    'Mercedes': ['#00D2BE', '#000000'],  # Azul Petróleo e Preto
    'Lancia': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'HWM': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Schroeder': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Pawl': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Pankratz': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Arzani-Volpini': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Nichels': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Bromme': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Klenk': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Simca': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Turner': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Del Roy': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Veritas': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'BMW': ['#FFFFFF', '#0066CC'],  # Branco e Azul BMW
    'EMW': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'AFM': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Frazer Nash': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Sherman': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Deidt': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'ERA': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Aston Butterworth': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Cisitalia': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Talbot-Lago': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Hall': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Marchese': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Langley': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Rae': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Olson': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Wetteroth': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Adams': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Snowberger': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'Milano': ['#FFFFFF', '#0066CC'],  # Branco e Azul
    'HRT': ['#000000', '#FF8000'],  # Preto e Laranja
    'Cooper-Maserati': ['#005AFF', '#006400'],  # Azul e Verde Maserati
    'Virgin': ['#000000', '#CC0000'],  # Preto e Vermelho
    'Cooper-OSCA': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Cooper-Borgward': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Cooper-Climax': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Cooper-Castellotti': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'Lotus-Climax': ['#000000', '#FFD700'],  # Preto e Dourado
    'Lotus-Maserati': ['#000000', '#006400'],  # Preto e Verde Maserati
    'De Tomaso-Osca': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'De Tomaso-Alfa Romeo': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho Alfa
    'Lotus-BRM': ['#000000', '#006400'],  # Preto e Verde BRM
    'Lotus-Borgward': ['#000000', '#005AFF'],  # Preto e Azul
    'Cooper-Alfa Romeo': ['#005AFF', '#CC0000'],  # Azul e Vermelho Alfa
    'De Tomaso-Ferrari': ['#FFFFFF', '#DC0000'],  # Branco e Vermelho Ferrari
    'Lotus-Ford': ['#000000', '#FFD700'],  # Preto e Dourado
    'Brabham-BRM': ['#FFFFFF', '#006400'],  # Branco e Verde BRM
    'Brabham-Ford': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Brabham-Climax': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'LDS-Climax': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'LDS-Alfa Romeo': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho Alfa
    'Cooper-Ford': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'McLaren-Ford': ['#FF8700', '#005AFF'],  # Laranja e Azul
    'McLaren-Serenissima': ['#FF8700', '#005AFF'],  # Laranja e Azul
    'Eagle-Climax': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Eagle-Weslake': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Brabham-Repco': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Cooper-Ferrari': ['#005AFF', '#DC0000'],  # Azul e Vermelho Ferrari
    'Cooper-ATS': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'McLaren-BRM': ['#FF8700', '#006400'],  # Laranja e Verde BRM
    'Cooper-BRM': ['#005AFF', '#006400'],  # Azul e Verde BRM
    'Matra-Ford': ['#005AFF', '#FFFFFF'],  # Azul e Branco
    'BRM-Ford': ['#006400', '#005AFF'],  # Verde BRM e Azul
    'McLaren-Alfa Romeo': ['#FF8700', '#CC0000'],  # Laranja e Vermelho Alfa
    'March-Alfa Romeo': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho Alfa
    'March-Ford': ['#FFFFFF', '#005AFF'],  # Branco e Azul
    'Lotus-Pratt &amp; Whitney': ['#000000', '#FFD700'],  # Preto e Dourado
    'Shadow-Ford': ['#000000', '#FFFFFF'],  # Preto e Branco
    'Shadow-Matra': ['#000000', '#FFFFFF'],  # Preto e Branco
    'Brabham-Alfa Romeo': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho Alfa
    'Lotus': ['#000000', '#FFD700'],  # Preto e Dourado
    'Marussia': ['#CC0000', '#000000'],  # Vermelho e Preto
    'Caterham': ['#006400', '#FFD800'],  # Verde e Amarelo
    'Lotus F1': ['#000000', '#FFD700'],  # Preto e Dourado
    'Manor Marussia': ['#CC0000', '#000000'],  # Vermelho e Preto
    'Haas F1 Team': ['#FFFFFF', '#CC0000'],  # Branco e Vermelho
    'Racing Point': ['#FF80C7', '#000000'],  # Rosa e Preto (2020)
    'AlphaTauri': ['#00008B', '#FFFFFF'],  # Azul Escuro e Branco
    'Alpine F1 Team': ['#005AFF', '#FF8000'],  # Azul e Rosa/Laranja
    'RB F1 Team': ['#00008B', '#FFFFFF'],  # Azul Escuro e Branco (Red Bull B-team)
}

# ------------------------------
# Pilotos
# ------------------------------
def get_info_pilotos() -> pd.DataFrame:
    """Função para conseguir informações sobre todos os pilotos"""
    df_pilotos = data_frames['drivers'].copy()

    # Calcula idade
    df_pilotos['dob'] = pd.to_datetime(df_pilotos['dob'])
    df_pilotos['idade'] = (dt.today() - df_pilotos['dob']).dt.days // 365

    # Nome completo
    df_pilotos['nome_completo'] = df_pilotos['forename'] + " " + df_pilotos['surname']

    # Remover colunas desnecessárias
    df_pilotos.drop(['driverRef', 'surname', 'forename'], axis=1, inplace=True)

    # Renomeando colunas
    colunas = {
        'driverId' : 'driverId',
        'number_driver' : 'numero_do_piloto',
        'code' : 'code',
        'dob' : 'data_aniversario',
        'nationality_driver' : 'nacionalidade_piloto',
        'url_driver' : 'wiki_url_piloto',
        'idade' : 'idade',
        'nome_completo' : 'nome_completo'
    }

    df_pilotos = df_pilotos.rename(columns=colunas)

    return df_pilotos


# ------------------------------
# Time
# ------------------------------
def get_info_time(cores_equipe: dict[list] = EQUIPES_CORES) -> pd.DataFrame:
    """Função para conseguir informações sobre todas as equipes"""
    df_equipes = data_frames['constructors'].copy()

    # Remove colunas desnecessárias
    df_equipes.drop(['constructorRef', 'url_circuit'], axis=1, inplace=True)

    # Renomeando colunas
    colunas = {
        'constructorId' : 'constructorId',
        'name_constructor' : 'nome_equipe',
        'nationality_constructor' : 'nacionalidade_equipe'
    }

    df_equipes = df_equipes.rename(columns=colunas)

    # Usando o método .map() para associar as cores às equipes
    df_equipes['cores'] = df_equipes['nome_equipe'].map(cores_equipe)  

    return df_equipes


# ------------------------------
# Tempo de Volta
# ------------------------------
def get_lap_time() -> pd.DataFrame:
    """Função para conseguir informações sobre os tempos de volta"""
    df_lap_time = data_frames['lap_times'].copy()

    # Renomeando colunas
    colunas = {
        'raceId' : 'raceId',
        'driverId' : 'driverId',
        'lap' : 'lap',
        'position' : 'posicao',
        'time' : 'lap_time',
        'milliseconds' : 'ms_lap_time',
    }

    df_lap_time = df_lap_time.rename(columns=colunas)

    return df_lap_time

# ------------------------------
# Status ao Final da Corrida
# ------------------------------
def get_status_race() -> pd.DataFrame:
    """Função para conseguir a informação sobre o status do piloto"""
    df_status_race = data_frames['status'].copy()

    # Renomeando colunas
    colunas = {
        'status' : 'status_race'
    }

    df_status_race = df_status_race.rename(columns=colunas)

    return df_status_race

# -------------------------------------
# Classificação dos Pilotos no Mundial
# --------------------------------------
def get_drivers_standing() -> pd.DataFrame:
    """Função para conseguir a informação sobre a classificação dos pilotos"""
    df_drivers_standing = data_frames['driver_standings'].copy()

    # Renomeando colunas
    colunas = {
        'points' : 'pontos',
        'position' : 'posicao_mundial',
        'win' : 'vitorias'
    }

    df_drivers_standing = df_drivers_standing.rename(columns=colunas)

    return df_drivers_standing


# -------------------------------------
# Temporadas
# --------------------------------------
def get_seasons() -> pd.DataFrame:
    """Função para conseguir a informação sobre as temporadas"""
    df_seasons = data_frames['seasons'].copy()

    # Renomeando colunas
    colunas = {
        'year' : 'ano',
        'url' : 'url_temporada',
    }

    df_seasons = df_seasons.rename(columns=colunas)

    return df_seasons


# -------------------------------------
# Paradas ou Pit Stops
# --------------------------------------
def get_pit_stops() -> pd.DataFrame:
    """Função para conseguir a informação sobre os PitStops"""
    df_pit_stops = data_frames['pit_stops'].copy()

    # Transformando unidades
    df_pit_stops['milliseconds'] = (df_pit_stops['milliseconds']) / 1000

    # Renomeando colunas
    colunas = {
        'stop' : 'qtd_paradas',
        'time' : 'time_pit_stop',
        'duration' : 'duracao_pit_stop',
        'milliseconds' : 'ms_pit_stop',
    }

    df_pit_stops = df_pit_stops.rename(columns=colunas)

    return df_pit_stops


# -------------------------------------
# Resultados da Sprint
# --------------------------------------
def get_sprints_results() -> pd.DataFrame:
    """Função para conseguir a informação sobre o resultado das sprints"""
    df_sprints_results = data_frames['sprint_results'].copy()

    # Renomeando colunas
    colunas = {
        'number' : 'numero_do_piloto',
        'grid' : 'posicao_grid',
        'position' : 'posicao_final',
        'points' : 'pontoss',
        'time' : 'tempo_volta',
        'milliseconds' : 'ms_volta',
        'fastestLap' : 'volta_rapida',
        'fastestLapTime' : 'volta_rapida_tempo',
    }

    df_sprints_results = df_sprints_results.rename(columns=colunas)

    # Tipo
    df_sprints_results['tipo_corrida'] = 'Sprint'

    return df_sprints_results


# -------------------------------------
# Classificação das Time
# --------------------------------------
def get_time_standing() -> pd.DataFrame:
    """Função para conseguir a informação sobre a classificação dos times"""
    df_time_standing = data_frames['constructor_standings'].copy()

    # Renomeando colunas
    colunas = {
        'points' : 'pontos_time',
        'position' : 'posicao_mundial_time',
        'wins' : 'vitorias_time',
    }

    df_time_standing = df_time_standing.rename(columns=colunas)

    return df_time_standing


# -------------------------------------
# Resultados das Corridas
# --------------------------------------
def get_race_results() -> pd.DataFrame:
    """Função para conseguir a informação sobre os resultados das corridas"""
    df_race_results = data_frames['results'].copy()
    
    # Remove colunas desnecessárias
    df_race_results.drop(['rank', 'fastestLapSpeed'], axis=1, inplace=True)

    # Renomeando colunas
    colunas = {
        'number_driver_season' : 'numero_do_piloto',
        'grid' : 'posicao_grid',
        'position' : 'posicao_final',
        'points' : 'pontos',
        'time' : 'tempo_volta',
        'milliseconds' : 'ms_volta',
        'fastestLap' : 'volta_rapida',
        'fastestLapTime' : 'volta_rapida_tempo',
    }

    df_race_results = df_race_results.rename(columns=colunas)

    # Tipo de Corrida
    df_race_results['tipo_corrida'] = 'Corrida_Principal'

    return df_race_results


# -------------------------------------
# Circuitos
# --------------------------------------
def get_circuits() -> pd.DataFrame:
    """Função para conseguir a informação sobre os circuitos"""
    df_circuit = data_frames['circuits'].copy()
    
    # Remove colunas desnecessárias
    df_circuit.drop(['circuitRef', 'alt'], axis=1, inplace=True)

    # Renomeando colunas
    colunas = {
        'name_circuit' : 'nome_circuito',
        'location' : 'cidade',
        'country' : 'pais',
        'lng' : 'long',
        'url' : 'url_circuito',
    }

    df_circuit = df_circuit.rename(columns=colunas)

    return df_circuit


# -------------------------------------
# Qualificação
# --------------------------------------
def get_qualifying() -> pd.DataFrame:
    """Função para conseguir a informação sobre das qualificações"""
    df_qualifying = data_frames['qualifying'].copy()

    # Renomeando colunas
    colunas = {
        'number_driver_season' : 'numero_do_piloto',
        'position' : 'posicao_grid',
    }

    df_qualifying = df_qualifying.rename(columns=colunas)

    return df_qualifying

# df = get_qualifying()
# print(df)
