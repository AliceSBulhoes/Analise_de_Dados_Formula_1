# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from plotly.subplots import make_subplots
from scipy import stats
# Importando funções auxiliares
from utils.api_wiki import get_wikipedia_summary
from utils.get_info import *
from utils.prepracao_dados import *

# ------------------------------
# Variáveis Globais
# ------------------------------
DATA_FRAME = {}
PILOTO = "Lewis Hamilton"
REGULAMENTOS = [2014, 2022]


# ------------------------------
# Função Utilitária
# ------------------------------
def get_rgba(color_name, alpha=0.2):
    """Converte nome de cor ou hex em rgba transparente"""
    rgb = mcolors.to_rgb(color_name)  # retorna valores entre 0–1
    return f"rgba({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)},{alpha})"


def get_mapa_cores(df):
    # Garantir que "cores" vire tupla (para ser hashable)
    df_tmp = df.copy()
    df_tmp["cores"] = df_tmp["cores"].apply(
        lambda x: tuple(x) if isinstance(x, list) else (x,)
    )

    # Criar dicionários
    mapa_barras = (
        df_tmp[["nome_equipe", "cores"]]
        .drop_duplicates()
        .set_index("nome_equipe")["cores"]
        .apply(lambda x: x[0] if len(x) > 0 else "#808080")
        .to_dict()
    )

    mapa_linhas = (
        df_tmp[["nome_equipe", "cores"]]
        .drop_duplicates()
        .set_index("nome_equipe")["cores"]
        .apply(lambda x: x[1] if len(x) > 1 else "#000000")
        .to_dict()
    )

    return mapa_barras, mapa_linhas


def filtrar_periodo_companheiro(df_ham, df_companheiro, nome_companheiro):
    # filtra apenas o companheiro na Mercedes
    df_temp = df_companheiro[
        (df_companheiro['nome_completo'] == nome_companheiro) 
        & (df_companheiro['nome_equipe'] == 'Mercedes')
    ]
    
    # anos em que esse companheiro REALMENTE estava na Mercedes
    anos_comuns = df_temp['ano'].unique()
    
    # Hamilton apenas nesses anos
    df_ham_filtrado = df_ham[
        (df_ham['ano'].isin(anos_comuns)) 
        & (df_ham['nome_equipe'] == 'Mercedes')
    ]
    
    return df_ham_filtrado, df_temp


def filtrar_periodo_russell(df_ham, df_companheiro):
    """
    Retorna apenas os anos em que Hamilton e Russell foram companheiros na Mercedes (2022 em diante).
    """
    df_russell = df_companheiro[
        (df_companheiro['nome_completo'] == 'George Russell')
        & (df_companheiro['nome_equipe'] == 'Mercedes')
        & (df_companheiro['ano'] >= 2022)  # Russell só entrou em 2022
    ]
    
    anos_validos = df_russell['ano'].unique()
    
    df_ham_filtrado = df_ham[
        (df_ham['ano'].isin(anos_validos))
        & (df_ham['nome_equipe'] == 'Mercedes')
    ]
    
    return df_ham_filtrado, df_russell


def analise_intervalo_confianca(df_ham, df_comp):
    """Calcula intervalo de confiança e teste t unilateral"""
    # Remover valores NaN das colunas de posição final
    ham_positions = df_ham["posicao_final"].dropna()
    comp_positions = df_comp["posicao_final"].dropna()
    
    # Verificar se temos dados suficientes após remover NaN
    if len(ham_positions) < 2 or len(comp_positions) < 2:
        return {
            "media_ham": np.nan, "ic_ham": (np.nan, np.nan),
            "media_tm": np.nan, "ic_tm": (np.nan, np.nan),
            "t_stat": np.nan, "p_val": np.nan
        }
    
    # Médias
    media_ham = ham_positions.mean()
    media_tm = comp_positions.mean()

    # IC 95% Hamilton
    sem_ham = stats.sem(ham_positions)
    ic_ham = stats.t.interval(0.95, len(ham_positions)-1, loc=media_ham, scale=sem_ham)

    # IC 95% Companheiro
    sem_tm = stats.sem(comp_positions)
    ic_tm = stats.t.interval(0.95, len(comp_positions)-1, loc=media_tm, scale=sem_tm)

    # Teste t unilateral: Hamilton < Companheiro (melhor posição = menor número)
    if ham_positions.std() == 0 and comp_positions.std() == 0:
        t_stat, p_val = np.nan, np.nan
    else:
        try:
            t_stat, p_val = stats.ttest_ind(ham_positions, comp_positions, 
                                          equal_var=False, alternative='less')
        except:
            t_stat, p_val = np.nan, np.nan

    return {
        "media_ham": media_ham, "ic_ham": ic_ham,
        "media_tm": media_tm, "ic_tm": ic_tm,
        "t_stat": t_stat, "p_val": p_val
    }

# ===============================
# Gráficos
# ===============================
def grafico_densidade_interativo(df):
    import plotly.graph_objects as go
    import numpy as np
    from scipy.stats import gaussian_kde
    import streamlit as st

    # Se "cores" for lista, pega a primeira cor
    df = df.copy()
    df["cores"] = df["cores"].apply(lambda x: x[0] if isinstance(x, list) else x)

    fig = go.Figure()

    for equipe, grupo in df.groupby("nome_equipe"):
        valores = grupo["posicao_final"].dropna()
        if len(valores) == 0:
            continue

        x_vals = np.linspace(valores.min(), valores.max(), 200)
        kde = gaussian_kde(valores)
        densidade = kde(x_vals)

        cor = grupo["cores"].iloc[0]

        # =======================
        # Curva de densidade
        # =======================
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=densidade,
            mode="lines",
            line=dict(color=cor, width=2),
            name=f"Densidade {equipe}"
        ))

        # =======================
        # Estatísticas
        # =======================
        media = valores.mean()
        mediana = np.median(valores)
        moda_idx = np.argmax(densidade)  # índice do pico da curva
        moda = x_vals[moda_idx]

        # Linha da média
        fig.add_vline(
            x=media,
            line=dict(color=cor, dash="dot", width=1.5),
            annotation_text=f"Média: {media:.1f}",
            annotation_position="top"
        )


        # Linha da moda (pico KDE)
        fig.add_vline(
            x=moda,
            line=dict(color=cor, dash="dash", width=1.5),
            annotation_text=f"Pico: {moda:.1f}",
            annotation_position="bottom"
        )

    # =======================
    # Layout final
    # =======================
    fig.update_layout(
        title="Distribuição de Posições por Equipe",
        xaxis_title="Posição Final",
        yaxis_title="Densidade",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def medidas_centrais_grafico(resumo_hamilton: pd.DataFrame) -> None:
    fig = go.Figure()

    # Reusar os mapas de cor
    mapa_barras, mapa_linhas = get_mapa_cores(DATA_FRAME['df_dados_LH'])

    for equipe in resumo_hamilton["nome_equipe"].unique():
        df_equipe = resumo_hamilton[resumo_hamilton["nome_equipe"] == equipe]
        cor = mapa_barras.get(equipe, "#808080")  # cor principal

        # Linha da média
        fig.add_trace(go.Scatter(
            x=df_equipe["ano"],
            y=df_equipe["mean"],
            mode="lines+markers",
            name=f"Média",
            line=dict(color=cor, width=3),
            marker=dict(size=8, color=cor)
        ))

        # Linha da mediana (tracejada)
        fig.add_trace(go.Scatter(
            x=df_equipe["ano"],
            y=df_equipe["median"],
            mode="lines+markers",
            name=f"Mediana",
            line=dict(color=cor, width=2, dash="dot"),
            marker=dict(symbol="diamond", size=7, color=cor)
        ))

        # Faixa de desvio padrão com transparência
        fig.add_trace(go.Scatter(
            x=pd.concat([df_equipe["ano"], df_equipe["ano"][::-1]]),
            y=pd.concat([df_equipe["mean"] + df_equipe["std"], 
                        (df_equipe["mean"] - df_equipe["std"])[::-1]]),
            fill="toself",
            fillcolor=get_rgba(cor, 0.2),
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            name=f"±1 Desvio Padrão ({equipe})"
        ))

    # ===============================
    # Linhas dos regulamentos da F1
    # ===============================
    regulamentos = {
        2009: "Mudança Aerodinâmica",
        2014: "Era Híbrida",
        2017: "Carros Largos",
        2022: "Efeito Solo"
    }

    for ano, desc in regulamentos.items():
        fig.add_vline(
            x=ano,
            line=dict(color="white", dash="dash"),
            annotation=dict(
                text=f"{ano}\n{desc}",
                showarrow=False,
                yanchor="bottom",
                xanchor="left",
                font=dict(size=10, color="white")
            )
        )

    # Layout
    fig.update_layout(
        title="📈 Evolução da Posição Média e Mediana do Hamilton por Ano",
        xaxis_title="Ano",
        yaxis_title="Posição Final",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            orientation="h",   # horizontal
            yanchor="top",     # ancorar no topo
            y=-0.2,            # jogar pra baixo do gráfico
            xanchor="center",  # centralizar
            x=0.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def grafico_boxplot(df_hamilton, df_teammate, teammate_name, teammate_color="blue"):
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df_hamilton["posicao_final"], 
        name="Lewis Hamilton", marker=dict(color="gray")
    ))
    fig.add_trace(go.Box(
        y=df_teammate["posicao_final"], 
        name=teammate_name, marker=dict(color=teammate_color)
    ))

    fig.update_layout(
        title=f"Distribuição das Posições: Hamilton vs {teammate_name}",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)


def grafico_comparacao_com_ic(df_ham, df_comp, nome_companheiro):
    """Cria gráfico de linha com intervalos de confiança"""
    # Agrupar por ano e calcular média e IC
    ham_por_ano = df_ham.groupby('ano')['posicao_final'].agg(['mean', 'count', 'std']).reset_index()
    comp_por_ano = df_comp.groupby('ano')['posicao_final'].agg(['mean', 'count', 'std']).reset_index()
    
    # Calcular intervalo de confiança para cada ano
    ham_por_ano['ic_superior'] = ham_por_ano['mean'] + (1.96 * ham_por_ano['std'] / np.sqrt(ham_por_ano['count']))
    ham_por_ano['ic_inferior'] = ham_por_ano['mean'] - (1.96 * ham_por_ano['std'] / np.sqrt(ham_por_ano['count']))
    
    comp_por_ano['ic_superior'] = comp_por_ano['mean'] + (1.96 * comp_por_ano['std'] / np.sqrt(comp_por_ano['count']))
    comp_por_ano['ic_inferior'] = comp_por_ano['mean'] - (1.96 * comp_por_ano['std'] / np.sqrt(comp_por_ano['count']))
    
    # Criar gráfico
    fig = go.Figure()
    
    # Lewis Hamilton - linha principal
    fig.add_trace(go.Scatter(
        x=ham_por_ano['ano'],
        y=ham_por_ano['mean'],
        mode='lines+markers',
        name='Lewis Hamilton',
        line=dict(color="#606060", width=3),
        marker=dict(size=8, color='#606060')
    ))
    
    # Lewis Hamilton - área do IC
    fig.add_trace(go.Scatter(
        x=ham_por_ano['ano'].tolist() + ham_por_ano['ano'].tolist()[::-1],
        y=ham_por_ano['ic_superior'].tolist() + ham_por_ano['ic_inferior'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(51, 50, 50, 0.44)',
        line=dict(color='rgba(255,255,255,0)'),
        name='IC 95% Hamilton',
        showlegend=True
    ))
    
    # Companheiro - linha principal
    fig.add_trace(go.Scatter(
        x=comp_por_ano['ano'],
        y=comp_por_ano['mean'],
        mode='lines+markers',
        name=nome_companheiro,
        line=dict(color='#00D2BE', width=3),
        marker=dict(size=8, color='#00D2BE')
    ))
    
    # Companheiro - área do IC
    fig.add_trace(go.Scatter(
        x=comp_por_ano['ano'].tolist() + comp_por_ano['ano'].tolist()[::-1],
        y=comp_por_ano['ic_superior'].tolist() + comp_por_ano['ic_inferior'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0, 210, 189, 0.44)',
        line=dict(color='rgba(255,255,255,0)'),
        name=f'IC 95% {nome_companheiro}',
        showlegend=True
    ))
    
    # Atualizar layout
    fig.update_layout(
        title=f'Comparação de Posições Médias com IC 95%<br>Hamilton vs {nome_companheiro}',
        xaxis_title='Ano',
        yaxis_title='Posição Média Final',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        height=500,
        template='plotly_white'
    )
    
    return fig


# ------------------------------
# Contexto
# ------------------------------
def contexto_conteudo() -> None:
    """Função para renderizar o contexto do conteúdo"""    

    # ---- Contexto Formula 1 ----
    col1, col2 = st.columns([1, 1], vertical_alignment="center")

    with col1:
        st.markdown(
            """
                <div class="conteudo">
                    <h2 class="titulo-2">Contexto</h2>
                    <div class="paragrafo">
                        <p class="text">A <strong>Formula 1</strong> é considerada, por muitos, o ápice do automobilismo mundial: a vitrine máxima onde talento, ousadia e disciplina se encontram em um espetáculo que mistura velocidade, tecnologia e emoção. Para a maioria dos pilotos, desde os primeiros passos nas <i>categorias de base</i> até os sonhos de infância, chegar à <strong>Formula 1</strong> já é uma conquista quase inimaginável. Poucos conseguem superar todas as barreiras financeiras, físicas e mentais para finalmente se sentar no <i>cockpit</i> de um carro da categoria, competindo lado a lado com alguns dos maiores nomes da história do esporte.</p>
                        <p class="text">No entanto, estar presente no <i>grid</i> é apenas o início de um caminho árduo. Vencer na <strong>Formula 1</strong> exige não apenas habilidade inata, mas também uma combinação rara de estratégia, preparo físico impecável, confiança e, muitas vezes, estar no lugar certo na hora certa. Ainda mais raro é transformar vitórias isoladas em consistência ao longo de uma temporada inteira, alcançando o tão sonhado título mundial. Esse feito é reservado a uma minoria absoluta, um grupo seleto de pilotos que se eterniza nos livros da categoria.</p>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.image(
            "https://cdn.britannica.com/66/258266-050-BD8FC43A/Max-Verstappen-Grand-Prix-of-Singapore.jpg",
            use_container_width=True,
        )

    st.divider()

    # ---- Sobre Lewis Hamilton ----
    df_pilotos = get_info_pilotos()
    df_piloto = df_pilotos[df_pilotos['nome_completo'] == PILOTO]
    info_wiki = get_wikipedia_summary(df_piloto['wiki_url_piloto'].iloc[0])

    col3, col4 = st.columns([1, 2], vertical_alignment="center")

    with col3:
        st.image(info_wiki['image'], use_container_width=True)

    with col4:
        st.markdown(
            """
                <div class="conteudo">
                    <h2 class="titulo-2">Sobre Lewis Hamilton</h2>
                    <div class="paragrafo">
                        <p class="text"><strong>Lewis Hamilton</strong> é um dos nomes mais marcantes da história da Formula 1. Nascido em Stevenage, Inglaterra, começou sua trajetória no <i>kart</i> ainda muito jovem e rapidamente se destacou pela combinação de talento natural e determinação. Ao longo dos anos construiu uma carreira que o levou do sonho de criança ao patamar mais alto do automobilismo mundial, tornando-se não apenas campeão, mas também uma figura de grande impacto dentro e fora das pistas. Sua trajetória é marcada por conquistas expressivas, recordes impressionantes e uma presença que ultrapassa o universo esportivo, consolidando-o como um dos grandes ícones da era moderna do esporte a motor.</p>
                        <p class="text">Nesta análise, revisitaremos cada temporada do heptacampeão até 2024, último ano de sua longa passagem pela <strong>Mercedes</strong>, equipe com a qual conquistou seis de seus títulos. A questão que guia nossa investigação é clara: Hamilton é realmente tão bom quanto parece ou foi apenas o carro, como muitas pessoas podem pensar?</p>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.divider()


# ------------------------------
# Dados Disponíveis
# ------------------------------
def dados_conteudo() -> None:
    """Função para renderizar a página de dados disponíveis"""
    st.markdown(
        """
            <div class="conteudo">
                <h2 class="titulo-2">Dados Disponíveis</h2>
                <h3 class="titulo-3">Fonte</h3>
                <div class="paragrafo">
                    <p class="text">
                        Os dados desta análise foram retirados do 
                        <a href="https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020/data">Kaggle</a>. 
                        As informações estão divididas em 14 arquivos, de forma normalizada. 
                        Por isso é importante definir bem as perguntas que queremos responder, 
                        já que, dependendo delas, será necessário transformar essas tabelas em 
                        um único dataset para análise.
                    </p>
                </div>
                <hr>
                <h3 class="titulo-3">Perguntas</h3>
                <div class="paragrafo">
                    <p class="text">
                        Como estamos analisando a <strong>Formula 1</strong> e focando em um piloto específico, 
                        algumas perguntas guiam nosso estudo:
                    </p>
                    <ol>
                        <li>Quais são as métricas médias do piloto no geral? Elas mudam ao longo dos anos?</li>
                        <li>O desempenho dele evoluiu de forma consistente? E atualmente, continua em crescimento?</li>
                        <li>Com as mudanças de regulamento, houve quedas ou saltos de desempenho?</li>
                        <li>Comparado aos companheiros de equipe, ele se destacou?</li>
                        <li>Houve algum período de dominância? Essa dominância veio mais do carro ou do piloto?</li>
                    </ol>
                    <p class="text">Nosso foco principal é a quinta pergunta: <strong>o que significa ser dominante?</strong> Para chegar a essa resposta, começaremos explorando as outras questões e, ao final, verificaremos se é possível afirmar ou não essa dominância. É provável que seja necessária uma análise mais ampla e detalhada, mas por enquanto, sabendo qual é nosso objetivo, o próximo passo é a <strong>preparação de dados</strong>!</p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------
# Preparação de Dados
# ------------------------------
def preparacao_conteudo() -> None:
    """Função para renderizar o conteúdo da página de Tratamento de Dados"""
    st.markdown(
        """
            <div class="conteudo">
                <h2 class="titulo-2">Preparação de Dados</h2>
                <div class="paragrafo">
                    <p class="text">
                        No mundo real, os dados geralmente são armazenados em bancos de dados normalizados,
                        o que nem sempre é adequado para análises diretas. 
                        Neste segmento, vamos observar como as tabelas estão distribuídas, 
                        identificar os indicadores e atributos necessários para a análise
                        e construir novos DataFrames unindo as tabelas de interesse. 
                        Além disso, avaliaremos a possibilidade de criar colunas adicionais
                        que possam auxiliar em análises futuras.
                    </p>
                </div>
                <hr>
                <h3 class="titulo-3">Visualizar DataFrames</h3>
                <div class="paragrafo">
                    <p class="text">
                        Como mencionado anteriormente, agora entraremos na parte de visualização dos DataFrames. 
                        É importante lembrar que, para analisarmos o desempenho do piloto, 
                        o foco principal são as corridas. 
                        Com isso em mente, vamos explorar os DataFrames a seguir:
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )



    func_get_dataframe = {
        'Piloto': get_info_pilotos,
        'Equipe': get_info_time,
        'Corridas': get_info_corrida,
        'Tempo de Volta': get_lap_time,
        'Status': get_status_race,
        'Classificação dos Pilotos': get_drivers_standing,
        'Temporadas': get_seasons,
        'Pit Stops': get_pit_stops,
        'Resultados das Sprints': get_sprints_results,
        'Classificação das Equipes': get_time_standing,
        'Resultados das Corridas': get_race_results,
        'Circuitos': get_circuits,
        'Qualificações': get_qualifying
    }

    # Selectbox (apenas um por vez)
    df_exibir = st.selectbox(
        "Selecione o DataFrame para visualizar:", 
        list(func_get_dataframe.keys())
    )

    # Condicional para exibir o selecionado
    if df_exibir:  
        st.subheader(f"📊 {df_exibir}")
        df = func_get_dataframe[df_exibir]()  # executa a função que retorna o dataframe
        st.dataframe(df)

    st.markdown(
        """
            <div class="conteudo">
                <hr>
                <div class="paragrafo">
                    <h3 class="titulo-3">DataFrame para Análise</h3>
                    <p class="text">
                        As tabelas <strong>Resultados das Sprints</strong> e 
                        <strong>Resultados das Corridas</strong> apresentam a mesma estrutura de colunas. 
                        Por isso, podemos <strong>concatená-las</strong> em um único DataFrame, 
                        obtendo uma visão consolidada do desempenho dos pilotos e do total de pontos 
                        acumulados ao longo dos anos.
                        Embora as <strong>Sprints</strong> sejam provas mais curtas, 
                        e muitas vezes questionadas pelos próprios pilotos, 
                        seus pontos também são relevantes para a análise e, portanto, serão considerados.
                        Além disso, vamos incluir o <strong>ano</strong> de cada corrida e o 
                        <strong>status final</strong> do piloto, permitindo identificar eventuais DNF 
                        (<i>Did Not Finish</i>) em sua carreira. Isso facilitará a filtragem dos períodos 
                        em que Lewis Hamilton esteve ativo na Formula 1.
                        Por fim, construiremos dois DataFrames: 
                        um exclusivo para <strong>Lewis Hamilton</strong> e outro abrangendo 
                        <strong>todos os pilotos</strong>, de modo a possibilitar comparações diretas 
                        com o heptacampeão.
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    DATA_FRAME['df_dados_corridas'] = merge_tabelas()
    DATA_FRAME['df_dados_LH'] = df_especifico()
    

    with col1:
        st.markdown("""
            <div class="conteudo">
                <h3 class="titulo-3" style="text-align: center;">Todas as Corridas (2007-2024)</h3>
            </div>
        """, unsafe_allow_html=True)

        st.dataframe(DATA_FRAME['df_dados_corridas'])

    with col2:
        st.markdown("""
            <div class="conteudo">
                <h3 class="titulo-3" style="text-align: center;">Lewis Hamilton Resultados</h3>
            </div>
        """, unsafe_allow_html=True)

        st.dataframe(DATA_FRAME['df_dados_LH'])

    st.markdown(
        """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                        Nestas tabelas estão reunidos os dados que servirão de base para a análise. 
                        A tabela <strong>Todas as Corridas</strong> consolida informações das tabelas de 
                        <i>Resultados das Sprints</i>, <i>Resultados das Corridas</i>, <i>Corridas</i>, 
                        <i>Status</i>, <i>Equipes</i> e <i>Pilotos</i>. 
                        Além disso, acrescentamos a coluna <i>"ganho_posicao"</i>, que indica 
                        quantas posições o piloto conquistou ao longo da prova em relação ao grid de largada. <br><br>
                        Já a tabela Lewis Hamilton Resultados mantém a mesma estrutura, mas inclui novas colunas: "vitorias", indicando quantas vezes o piloto terminou em primeiro lugar; "podios", registrando as ocasiões em que ficou entre os três primeiros; e "pole_position", que mostra quantas vezes conquistou a primeira posição no grid de largada durante a qualificação. Essa métrica é fundamental 
                        para compreender sua performance ao longo da carreira, já que a vitória 
                        é um dos principais indicadores de domínio na Formula 1. <br><br>
                        Com essas informações, o próximo passo é verificar se existem valores nulos, 
                        garantindo que nossa análise seja consistente e confiável.
                    </p>
                </div>
                <hr>
                <h2 class="titulo-2">Tratamento de Dados</h2>
                <div class="paragrafo">
                    <p class="text">
                        No processo de tratamento, é importante destacar que nem todo valor nulo 
                        representa uma inconsistência. Em alguns casos, a ausência de informação 
                        também pode trazer insights relevantes. <br><br>
                        Nesta seção, vamos verificar a quantidade de valores nulos em cada coluna dos DataFrames.
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
            <div class="conteudo">
                <h3 class="titulo-3" style="text-align: center;">🔎 Valores Nulos por Coluna <br>(Todas as Corridas)</h3>
            </div>
        """, unsafe_allow_html=True)

        st.dataframe(DATA_FRAME['df_dados_corridas'].isnull().sum().reset_index().rename(columns={"index": "Coluna", 0: "Nulos"}))
    
    with col4:
        st.markdown("""
            <div class="conteudo">
                <h3 class="titulo-3" style="text-align: center;">🔎 Valores Nulos por Coluna <br> (Lewis Hamilton Resultados)</h3>
            </div>
        """, unsafe_allow_html=True)

        st.dataframe(DATA_FRAME['df_dados_LH'].isnull().sum().reset_index().rename(columns={"index": "Coluna", 0: "Nulos"}))

    st.markdown(
        """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                        A análise dos valores ausentes revela que as colunas 
                        <i>"ganho_posicao"</i> e <i>"posicao_final"</i> apresentam 
                        exatamente a mesma quantidade de registros nulos. 
                        Isso não é coincidência: na Formula 1, quando um piloto 
                        <strong>não conclui a corrida (DNF - Did Not Finish)</strong>, 
                        não há como registrar sua posição final ou o ganho de posições. 
                        Assim, a ausência desses dados reflete a realidade das provas, 
                        e não uma falha no conjunto.
                        <br><br>
                        O mesmo padrão ocorre com as colunas 
                        <i>"tempo_volta_ultima"</i> e <i>"ms_volta_ultima"</i>. 
                        Elas ficam em branco justamente quando Hamilton abandona a corrida 
                        ou termina com <strong>+1 volta</strong> em relação ao líder, 
                        situação em que não existe um tempo válido de última volta. 
                        Já os campos <i>"volta_rapida"</i> e <i>"volta_rapida_tempo"</i> 
                        só aparecem nulos em casos em que o piloto não completou nenhuma volta, 
                        como no GP da Espanha de 2016, quando um acidente com seu companheiro 
                        de equipe, Nico Rosberg, causou seu abandono logo na primeira curva.
                        <br><br>
                        Portanto, os valores nulos estão diretamente associados 
                        às condições reais das corridas e não comprometem a integridade da base. 
                        Antes de avançar, entretanto, é essencial verificar a existência 
                        de <strong>linhas duplicadas</strong>, evitando que registros 
                        repetidos distorçam nossa análise.
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )


    # ------ Duplicatas ------
    cols_hashable = [
        col for col in DATA_FRAME['df_dados_corridas'].columns
        if pd.api.types.is_hashable(DATA_FRAME['df_dados_corridas'][col].dropna().iloc[0])
    ]

    duplicatas_corridas = DATA_FRAME['df_dados_corridas'].duplicated(subset=cols_hashable).sum()
    duplicatas_lh = DATA_FRAME['df_dados_LH'].duplicated(subset=cols_hashable).sum()

    col5, col6 = st.columns(2)

    with col5:
        st.markdown("""
            <div class="conteudo">
                <h3 class="titulo-3" style="text-align: center;">📌 Duplicatas <br>(Todas as Corridas)</h3>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1]) 
        with col2:
            st.metric("🔁 Duplicatas", duplicatas_corridas, border=True)

    with col6:
        st.markdown("""
            <div class="conteudo">
                <h3 class="titulo-3" style="text-align: center;">📌 Duplicatas <br>(Lewis Hamilton Resultados)</h3>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])  

        with col2:
            st.metric("🔁 Duplicatas",duplicatas_lh, border=True)

    st.markdown(
        """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                        A verificação mostra que não há registros duplicados nos DataFrames, 
                        o que reforça a consistência do tratamento inicial realizado. 
                        Com uma base confiável e livre de ruídos, podemos avançar para a 
                        <strong>classificação das variáveis</strong> e a escolha das 
                        visualizações mais adequadas para extrair insights relevantes.
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------
# Classificação das Variáveis
# ------------------------------
def classificacao_conteudo() -> None:
    """Renderiza a classificação variável por variável, com justificativa"""
    st.markdown(
        """
            <div class="conteudo">
                <h2 class="titulo-2">Classificação das Variáveis</h2>
                <div class="paragrafo">
                    <p class="text">
                        Agora vamos classificar <strong>cada variável do dataset</strong> individualmente.  
                        Para cada coluna, será apresentada sua categoria (qualitativa nominal, ordinal, 
                        quantitativa discreta ou contínua) acompanhada de uma <strong>justificativa</strong> 
                        explicando o porquê da classificação.  
                        Isso ajuda a entender como elas podem ser usadas em análises e quais 
                        técnicas estatísticas fazem sentido aplicar.
                    </p>
                </div>
                <hr>
                <h3 class="titulo-3">📋 Variáveis e seus Tipos</h3>
            </div>
        """, unsafe_allow_html=True
    )

    # Lista de variáveis com justificativas individuais
    variaveis = [
        # IDs (chaves técnicas, não usadas em análise estatística direta)
        ("raceId", "ID / Código", "Identificador único da corrida. Não tem significado numérico, apenas relacional."),
        ("driverId", "ID / Código", "Identificador único do piloto, usado para integrar informações entre tabelas."),
        ("constructorId", "ID / Código", "Identificador único da equipe. Função de chave estrangeira."),
        ("statusId", "ID / Código", "Identificador numérico do status da corrida. Sem interpretação estatística."),
        ("circuitId", "ID / Código", "Identificador único do circuito, valor técnico para referência."),
        ("resultId", "ID / Código", "Identificador único do resultado. Usado apenas para indexação."),

        # Variáveis Qualitativas Nominais 
        ("code", "Qualitativa Nominal", "Código de três letras do piloto (ex: HAM, VER). É apenas um rótulo."),
        ("nome_completo", "Qualitativa Nominal", "Nome completo do piloto, sem qualquer ordem implícita."),
        ("nome_equipe", "Qualitativa Nominal", "Nome da equipe (Mercedes, Ferrari). Não existe hierarquia."),
        ("name_circuit", "Qualitativa Nominal", "Nome do circuito (ex: Monza, Interlagos). Categoria descritiva."),
        ("status_race", "Qualitativa Nominal", "Situação final (Finished, DNF, Accident). Categorias distintas, sem ordem."),
        ("tipo_corrida", "Qualitativa Nominal", "Tipo da corrida (Sprint ou Principal). Classificação binária sem hierarquia."),
        ("cores", "Qualitativa Nominal", "Cor associada à equipe. Apenas descritivo, sem significado numérico."),

        # Variáveis Quantitativas Discretas 
        ("posicao_grid", "Quantitativa Discreta", "Posição de largada, número inteiro. Usado em cálculos como ganho de posição."),
        ("posicao_final", "Quantitativa Discreta", "Posição final da corrida. Valores inteiros (1º, 2º, 3º), não admite frações."),
        ("positionOrder", "Quantitativa Discreta", "Ordem oficial registrada pela FIA. Contagem inteira de posição."),
        ("ano", "Quantitativa Discreta", "Ano da corrida. É uma contagem inteira e não assume valores intermediários."),
        ("numero_do_piloto", "Quantitativa Discreta", "Número fixo do carro do piloto. É inteiro e não fracionável."),
        ("laps", "Quantitativa Discreta", "Número de voltas completadas. É uma contagem natural (1, 2, 3...)."),
        ("pontos", "Quantitativa Discreta", "Pontos obtidos segundo regulamento. Valores definidos e inteiros."),
        ("ganho_posicao", "Quantitativa Discreta", "Diferença entre posições de largada e chegada. Valor inteiro (positivo ou negativo)."),
        ("vitorias", "Quantitativa Discreta", "Um booleano em 0/1 representa se Hamilton venceu (1) ou não (0) uma corrida. É considerado quantitativa discreta por assumir apenas dois valores inteiros possíveis e permitir cálculos estatísticos."),
        ("podios", "Quantitativa Discreta", "Um booleano em 0/1 representa se Hamilton ficou no pódio (1) ou não (0) em uma corrida. É considerado quantitativa discreta por assumir apenas dois valores inteiros possíveis e permitir cálculos estatísticos."),
        ("pole_position", "Quantitativa Discreta", "Um booleano em 0/1 representa se Hamilton pegou a primeira posição do grid d largada (1) ou não (0) em uma corrida. É considerado quantitativa discreta por assumir apenas dois valores inteiros possíveis e permitir cálculos estatísticos."),
        ("rodada", "Quantitativa Discreta", "Contagem dos GP's de um ano. É uma variável de contagem inteira"),

        # Variáveis Quantitativas Contínuas 
        ("tempo_volta", "Quantitativa Contínua", "Tempo de volta medido em escala contínua. Entre dois tempos sempre existe outro."),
        ("ms_volta", "Quantitativa Contínua", "Tempo de volta registrado em milissegundos. Representa medida contínua."),
        ("volta_rapida_tempo", "Quantitativa Contínua", "Tempo da volta mais rápida, grandeza contínua com precisão infinita."),
        ("data_corrida", "Quantitativa Contínua", "A data da corrida pode ser representada numericamente (como dias ou segundos em relação a uma origem no tempo). Dessa forma, assume valores em uma escala contínua e permite comparações e cálculos de intervalos entre corridas.")

    ]


    # Criar dataframe com justificativas
    df_variaveis = pd.DataFrame(variaveis, columns=["Variável", "Tipo", "Justificativa"])

    st.dataframe(df_variaveis, use_container_width=True)

    st.markdown(
        """
            <div class="conteudo">
                <hr>
                <div class="paragrafo">
                    <p class="text">
                        Após a classificação detalhada das variáveis, temos uma visão clara de seus 
                        papéis dentro do conjunto de dados. Essa organização é essencial para orientar 
                        a escolha das técnicas estatísticas e das visualizações mais adequadas. 
                        Com essa base sólida, podemos avançar com maior segurança para a etapa de 
                        <strong>análise exploratória</strong>, extraindo padrões, relações e insights 
                        relevantes sobre o desempenho dos pilotos e equipes na Formula 1.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True
    )


# ------------------------------
# Análise dos Dados
# ------------------------------
def analise_conteudo() -> None:
    """Função para renderizar a análise exploratória"""
    st.markdown(
        """
            <div class="conteudo">
                <h2 class="titulo-2">Análise dos Dados</h2>
                <div class="paragrafo">
                    <p class="text">
                        Com intuito de analisar a carreira de <strong>Lewis Hamilton</strong> na <i>Formula 1</i>, 
                        o primeiro passo será observar sua consistência ao longo das temporadas, 
                        avaliando medidas como <strong>médias</strong>, <strong>medianas</strong> 
                        e <strong>desvios-padrão</strong> de seus resultados, 
                        além de métricas gerais como <i>vitórias</i>, <i>pódios</i>, 
                        <i>poles</i> e <i>pontos</i>. 
                    </p>
                    <p class="text">
                        Em seguida, a análise será segmentada entre os anos de <strong>McLaren</strong> 
                        e de <strong>Mercedes</strong>, permitindo comparar a distribuição de seus 
                        desempenhos em cada equipe. 
                    </p>
                    <p class="text">
                        Por fim, Hamilton será comparado aos seus <strong>companheiros de equipe</strong>, 
                        especialmente na <strong>Mercedes</strong>, onde além da visualização gráfica 
                        serão aplicados <i>intervalos de confiança</i> e <i>testes de hipótese</i>, 
                        a fim de verificar se, em média, seus resultados foram estatisticamente 
                        superiores aos dos colegas de time. 
                    </p>
                </div>
                <hr>
                <h3 class="titulo-3">Panorama Geral da Carreira</h2>
                <div class="paragrafo">
                    <p class="text">
                        O primeiro passo para a análise é observar o panorama geral da carreira de Lewis Hamilton. Para isso, é importante levantar informações básicas que ajudam a dimensionar sua trajetória, como o número total de vitórias conquistadas, a quantidade de pódios alcançados, quantas vezes ele largou na pole position e, por fim, o total de campeonatos mundiais que o piloto acumula ao longo da sua trajetória na Formula 1.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True
    )

    df_piloto = DATA_FRAME['df_dados_LH']

    # Layout com duas colunas principais
    imagemCol, metricasCol = st.columns([0.4, 0.6], vertical_alignment="center")

    with imagemCol:
        st.image(os.path.abspath('assets/img/hamilton.png'), use_container_width=True)

    with metricasCol:

        resumo_ano = df_piloto.groupby("ano").agg(
            vitorias=("vitorias", "sum"),
            poles=("pole_position", "sum"),
            podios=("podios", "sum"),
        ).reset_index().sort_values("ano")

        total_temporadas = resumo_ano["ano"].nunique()
        total_vitorias = int(resumo_ano["vitorias"].sum())
        total_poles = int(resumo_ano["poles"].sum())
        total_podios = int(resumo_ano["podios"].sum())
        total_titulos = 7
        total_corridas_terminadas = DATA_FRAME['df_dados_LH'][DATA_FRAME['df_dados_LH']["posicao_final"].notnull()].shape[0]

        # Organizar métricas em 2 linhas de 2 colunas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏁 Temporadas", total_temporadas, border=True)
        with col2:
            st.metric("🥇 Vitórias", total_vitorias, border=True)

        col3, col4 = st.columns(2)
        with col3:
            st.metric("🎯 Poles", total_poles, border=True)
        with col4:
            st.metric("🏆 Pódios", total_podios, border=True)

        col5, col6 = st.columns(2)
        with col5:
            st.metric("👑 Títulos do Campeonato", total_titulos, border=True)
        with col6:
            st.metric("🚦 Corridas Terminadas", total_corridas_terminadas, border=True)


    st.markdown(
        """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                        Ao analisarmos os números de Lewis Hamilton, rapidamente fica claro o tamanho do impacto que ele exerce dentro da Formula 1. Poucos pilotos na história conseguiram alcançar um patamar tão elevado e consistente. Para termos uma noção mais concreta dessa dimensão, basta lembrar que Ayrton Senna , considerado por muitos o maior nome da categoria , conquistou 41 vitórias ao longo de sua carreira. É verdade que, na época, havia um número menor de corridas por temporada, o que ajuda a explicar parcialmente essa diferença. No entanto, mesmo em um comparativo mais recente e equilibrado, Michael Schumacher, que divide com Hamilton o topo da lista de títulos mundiais, acumulou 95 vitórias ao longo de sua trajetória. Ainda assim, Hamilton conseguiu superar essa marca, deixando em evidência a grandiosidade de seu desempenho e reforçando sua posição como um dos maiores, senão o maior, da história da Formula 1.
                    </p>
                    <p class="text">
                        Outro ponto impressionante são os <b>206 pódios</b> conquistados, lembrando que esse número inclui também suas vitórias.
                        Se retirarmos os 105 triunfos do total, obtemos a proporção de aproximadamente <b>49% de vitórias</b> sobre os pódios. Ou seja, praticamente metade das vezes em que subiu ao pódio, foi no lugar mais alto. 
                        Em comparação, Schumacher apresenta cerca de <b>41%</b>, um número altíssimo, mas ainda abaixo do britânico.
                    </p>
                    <p class="text">
                        Nas poles, Hamilton também impressiona. Curiosamente, o número de poles coincide com o total de vitórias.
                        Claro, isso não significa que todas as poles viraram vitórias. 
                        Um exemplo claro foi em 2016, quando mesmo largando na frente, acabou colidindo com seu companheiro de equipe já na primeira curva.
                    </p>
                    <p class="text">
                        No total, Hamilton <b>terminou 344 corridas</b>. Dessas, em <b>206</b> ele esteve no pódio, o que representa cerca de <b>40%</b>.
                        Em outras palavras: a cada 10 corridas que completou, em 4 ele aparecia entre os três primeiros, uma consistência inacreditável.
                    </p>
                    <p class="text">
                        É importante destacar que esses números são acumulados da carreira inteira.
                        Para entender melhor como Hamilton construiu essa trajetória, precisamos olhar sua evolução ao longo das temporadas:
                        será que ele sempre foi consistente desde o início, demonstrando talento natural,
                        ou essa performance foi resultado de um processo de amadurecimento aliado ao carro e à equipe?
                        Com isso em mente, faremos um gráfico médio da posição que ele ficou ao longo da temporada e comparar com a média de outros pilotos que correram na mesma época 
                    </p>
                    <p class="text">
                        Com isso em mente, o próximo passo da análise será observar algumas medidas estatísticas que ajudam a traduzir numericamente o desempenho de Hamilton ao longo de sua carreira. Para cada temporada, iremos calcular métricas como a média, que mostra um panorama geral de seus resultados; a mediana e a moda, que ajudam a identificar padrões de consistência; além do desvio padrão e da variância, que indicam o quanto suas performances variaram ao longo do tempo. Dessa forma, será possível entender não apenas os números absolutos, mas também como eles se distribuem, revelando a evolução e a regularidade do piloto temporada após temporada.
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )


    resumo_hamilton = DATA_FRAME['df_dados_LH'].groupby(["ano", "nome_equipe"]).agg(
        mean=("posicao_final", "mean"),
        median=("posicao_final", "median"),
        std=("posicao_final", "std"),
        var=("posicao_final", "var"),
        moda=("posicao_final", lambda x: x.mode().iloc[0] if not x.mode().empty else None),
    ).reset_index()

    col1, col2 = st.columns([0.4,0.6], vertical_alignment='center')

    with col1:
        st.markdown(
            """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                        Como podemos observar no gráfico ao lado, logo em seu ano de estreia, 
                        <strong>Lewis Hamilton</strong> se destacou com <strong>médias</strong> e 
                        <strong>medianas</strong> muito baixas para um novato na <i>Formula 1</i>. 
                        Vale ressaltar que, naquele ano, ele quebrou o <strong>recorde de pontos de um estreante</strong>, 
                        um feito que já evidenciava seu talento.
                    </p>
                    <p class="text">
                        Entretanto, com a entrada de um <strong>novo regulamento</strong>, percebe-se uma 
                        piora no desempenho, tanto na <strong>média</strong> quanto na <strong>mediana</strong>. 
                        Isso se deve principalmente ao <i>carro</i>: a <strong>McLaren</strong> focou tanto na disputa de 2008 
                        (quando Hamilton foi <strong>campeão mundial</strong>) que acabou negligenciando o desenvolvimento para a temporada seguinte. 
                        Essa queda trouxe aprendizados e o carro evoluiu ao longo das corridas. 
                        Ainda assim, insatisfeito com a estagnação, Hamilton migrou para a <strong>Mercedes</strong>.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:
        medidas_centrais_grafico(resumo_hamilton)

    st.markdown(
        """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                        Na nova escuderia, o cenário mudou. Com o início da <strong>era híbrida</strong>, seu talento ficou ainda mais evidente: 
                        as <strong>médias</strong> e <strong>medianas</strong> se mantiveram constantemente <strong>abaixo do 3º lugar</strong>, 
                        marcando um período de <strong>domínio</strong> de Hamilton e da <strong>Mercedes</strong>.
                    </p>
                    <p class="text">
                        O ponto de virada veio em <strong>2021</strong>, na histórica batalha contra <strong>Max Verstappen</strong>. 
                        A <strong>Red Bull</strong> alcançou a Mercedes em desenvolvimento e a disputa foi acirrada até a última corrida, 
                        quando Hamilton acabou derrotado.
                    </p>
                    <p class="text">
                        Já a partir de <strong>2022</strong>, com o regulamento do <strong>efeito solo</strong>, a Mercedes enfrentou 
                        sérios problemas de projeto. Hamilton também parecia não se adaptar bem ao novo conceito, refletindo em maior 
                        <strong>instabilidade</strong> e em um <strong>desvio padrão</strong> mais evidente nas posições. 
                        Apesar de alguma melhora em <strong>2023</strong>, as <strong>medianas</strong> e as <strong>médias</strong> passaram a seguir 
                        uma tendência de <strong>crescimento</strong>, indicando resultados menos consistentes em relação ao auge da carreira.
                    </p>
                    <p class="text">
                        Após entendermos a evolução de <strong>Hamilton</strong> ao longo dos anos e os impactos 
                        dos diferentes <strong>regulamentos</strong> em seu desempenho, é importante observar também 
                        a <strong>diferença entre suas passagens na McLaren e na Mercedes</strong>. 
                        Para isso, elaboramos uma <i>distribuição das posições finais</i> separada por equipe, 
                        o que permite visualizar de forma clara tanto seu desenvolvimento quanto a confirmação 
                        dos pontos discutidos anteriormente.
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )


    grafico_densidade_interativo(DATA_FRAME['df_dados_LH'])

    st.markdown(
        """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                    Como podemos observar acima, gráfico de <strong>distribuição de posições</strong> evidencia de forma clara a diferença entre as fases de Hamilton na 
                    <strong>McLaren</strong> e na <strong>Mercedes</strong>. Enquanto na <strong>Mercedes</strong> sua curva é mais concentrada 
                    nos primeiros lugares, com <i>pico</i> próximo da <strong>1ª posição</strong> e <i>média</i> de <strong>3.5</strong>, 
                    já na <strong>McLaren</strong> a distribuição aparece mais espalhada, com <i>pico</i> em torno da <strong>2ª posição</strong> 
                    e <i>média</i> de <strong>4.6</strong>. Isso mostra que, nos anos de <strong>Mercedes</strong>, Hamilton teve uma consistência 
                    muito maior em lutar por <strong>vitórias</strong> e <strong>pódios</strong>, enquanto na <strong>McLaren</strong>, apesar de 
                    competitivo, os resultados foram mais variáveis. 
                    </p>
                    <p class="text">
                    Ainda assim, é importante destacar que, mesmo sem um <i>carro dominante</i>, Hamilton já apresentava desempenhos de alto nível. 
                    Seu <strong>título de 2008</strong> é um exemplo disso: conquistado principalmente pelo talento e esforço, em uma temporada 
                    marcada pela polêmica do <i>“Cingapuragate”</i>, que poderia ter mudado o rumo do campeonato em favor de <strong>Felipe Massa</strong>. 
                    Na última corrida, porém, Hamilton garantiu o título com uma <strong>ultrapassagem decisiva</strong> na volta final, mesmo com Massa 
                    vencendo a prova. 
                    </p>
                    <p class="text">
                    Retomando o ponto central, vemos que a <i>era de dominância</i> da <strong>Mercedes</strong> foi determinante para que Hamilton 
                    conquistasse <strong>6 de seus 7 títulos mundiais</strong>. No entanto, isso levanta uma questão importante: se a equipe era tão 
                    dominante, por que apenas <strong>Hamilton</strong> conseguiu transformar essa superioridade em <strong>títulos</strong>, enquanto 
                    seus <i>companheiros de equipe</i> não tiveram o mesmo sucesso? Para responder a isso, precisamos analisar também o desempenho 
                    dos <strong>companheiros de equipe</strong> de Hamilton, o que será o próximo passo da nossa análise. 
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    # ------- Comparação -------

    df_companheiro = DATA_FRAME['df_dados_corridas'].copy()
    df_companheiro = df_companheiro[df_companheiro['nome_equipe'] == 'Mercedes']
    df_companheiro = df_companheiro[df_companheiro['ano'] >= 2013]
    df_companheiro = df_companheiro[df_companheiro['code'] != 'HAM'] 
    df_companheiro['vitorias'] = df_companheiro['posicao_final'] == 1

    lista_companheiros = df_companheiro['nome_completo'].unique()

    st.markdown(
        """
            <div class="conteudo">
                <hr>
                <h3 class="titulo-3">Comparação com Companheiros de Equipe</h3>
                <div class="paragrafo">
                    <p class="text">
                    Para entender melhor o domínio de <strong>Lewis Hamilton</strong>, é essencial compará-lo com seus 
                    <strong>companheiros de equipe</strong>, especialmente durante sua trajetória na <i>Mercedes</i>. 
                    </p>
                    <p class="text">
                    Nesta análise, será possível selecionar o <strong>companheiro de equipe</strong> desejado e visualizar suas 
                    <strong>estatísticas de posição final</strong> em termos de <i>média</i>. Também será considerado o 
                    <strong>intervalo de confiança</strong>, que indica o grau de consistência dos resultados. 
                    Quanto menor for esse intervalo, maior a regularidade do piloto, já que suas posições tenderam a se concentrar 
                    dentro dessa faixa, com poucas ocorrências fora dela. 
                    </p>
                    <p class="text">
                    Para aprofundar a comparação, será realizado um <strong>teste de hipótese</strong>, com o objetivo de verificar 
                    se <strong>Hamilton</strong>, em média, foi estatisticamente superior aos seus <i>companheiros</i> no quesito 
                    <strong>posição final</strong>. Para isso, aplicaremos o <i>teste de duas médias para populações independentes</i>. 
                    </p>
                    <p class="text">
                    Fique à vontade para escolher qual <strong>companheiro de equipe</strong> deseja analisar e observar como 
                    as estatísticas se comportam em relação ao desempenho de <strong>Lewis Hamilton</strong>. 
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    companheiro = st.selectbox("Selecione o Companheiro: ", lista_companheiros)

    # Hamilton (filtrado só Mercedes)
    df_ham = DATA_FRAME['df_dados_LH'].copy()
    df_ham = df_ham[df_ham['nome_equipe'] == 'Mercedes']

    # Na seção de comparação com companheiros, substitua a parte do teste por:
    if companheiro == 'Nico Rosberg':

        boxCol, textCol = st.columns(2, vertical_alignment='center')

        with boxCol:
            df_ham_filtrado, df_rosberg = filtrar_periodo_companheiro(df_ham, df_companheiro, "Nico Rosberg")
            grafico_boxplot(df_ham_filtrado, df_rosberg, "Nico Rosberg", teammate_color="#00D2BE")
        
        with textCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                A famosa rivalidade interna da <strong>Mercedes</strong>, conhecida como <i>"Brocedes"</i>, marcou a época em que 
                                <strong>Lewis Hamilton</strong> e <strong>Nico Rosberg</strong> foram companheiros de equipe. 
                                No <i>boxplot</i> ao lado, podemos observar que <strong>Hamilton</strong> apresentou maior consistência, 
                                já que o tamanho de sua <i>caixa</i> é menor, indicando uma dispersão de resultados mais baixa em comparação a 
                                <strong>Rosberg</strong>. 
                            </p>
                            <p class="text">
                                Isso sugere que Hamilton esteve com mais frequência entre os <strong>top 3</strong>. A distância interquartil foi de 
                                <strong>2</strong> para Hamilton e <strong>3</strong> para Rosberg, uma diferença relativamente pequena, mas ainda assim 
                                significativa, refletindo o alto nível de competitividade e o poder do carro da <strong>Mercedes</strong> naquela época. 
                            </p>
                            <p class="text">
                                Além disso, vale destacar que <strong>Rosberg</strong> apresentou <i>outliers</i> mais elevados que os de Hamilton, 
                                o que indica que em algumas corridas seu desempenho ficou bem abaixo da média, enquanto Hamilton manteve maior regularidade. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )

        textIcCol, icCol = st.columns(2, vertical_alignment='center')

        with textIcCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                Outro jeito de avaliarmos se o que vimos no <i>boxplot</i> se confirma é por meio do 
                                <strong>intervalo de confiança</strong> das posições finais de cada piloto ao longo das temporadas. 
                                No gráfico ao lado, observamos que, na maior parte dos anos, <strong>Rosberg</strong> apresentou uma 
                                <i>média</i> de posição final pior que <strong>Hamilton</strong>. Além disso, o 
                                <strong>intervalo de confiança</strong> de Rosberg tende a ser mais amplo, indicando maior variação 
                                de desempenho, enquanto o de Hamilton é mais estreito, refletindo maior consistência. 
                            </p>
                            <p class="text">
                                É importante lembrar que o <strong>intervalo de confiança</strong> de 95% não garante o valor exato 
                                da média, mas sim a faixa onde há alta probabilidade de o valor real da média populacional se encontrar. 
                                Ainda assim, a disputa foi bastante equilibrada, especialmente em <strong>2016</strong>, quando a 
                                rivalidade atingiu seu ápice. 
                            </p>
                            <p class="text">
                                Porém, apenas a análise de intervalos não é suficiente para afirmar com certeza se 
                                <strong>Hamilton</strong> foi estatisticamente melhor que <strong>Rosberg</strong>. 
                                Para isso, será necessário aplicar um <strong>teste de hipótese</strong>. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )

        
        with icCol:
            # Gráfico de linha com IC
            fig_line_ic = grafico_comparacao_com_ic(df_ham_filtrado, df_rosberg, "Nico Rosberg")
            st.plotly_chart(fig_line_ic, use_container_width=True)
        
        testHipCol, textTestCol = st.columns([0.48,0.52], vertical_alignment='top')

        with testHipCol:
            # Teste de hipótese separado
            resultado = analise_intervalo_confianca(df_ham_filtrado, df_rosberg)

            st.markdown("### 🧪 Teste de Hipótese")

            st.markdown("**H₀ (Hipótese Nula):**")
            st.latex(r"\mu_{\text{Hamilton}} \geq \mu_{\text{Rosberg}}")
            st.markdown("> A posição média de **Hamilton** é igual ou **pior** que a do companheiro de equipe.")

            st.markdown("**H₁ (Hipótese Alternativa):**")
            st.latex(r"\mu_{\text{Hamilton}} < \mu_{\text{Rosberg}}")
            st.markdown("> A posição média de **Hamilton** é **melhor** que a do companheiro de equipe.")

            # Exibir resultados
            col1, col2, col3 = st.columns(3)
            with col1:
                # Para Lewis Hamilton
                st.metric(
                    "Lewis Hamilton", 
                    f"{resultado['media_ham']:.2f}",
                    f"IC 95%: [{resultado['ic_ham'][0]:.2f}, {resultado['ic_ham'][1]:.2f}]"
                )
            with col2:
                # Para Nico Rosberg  
                st.metric(
                    "Nico Rosberg",
                    f"{resultado['media_tm']:.2f}",
                    f"IC 95%: [{resultado['ic_tm'][0]:.2f}, {resultado['ic_tm'][1]:.2f}]"
                )
            with col3:
                st.metric("Diferença", f"{resultado['media_ham'] - resultado['media_tm']:.2f}")
            
            st.metric("Valor p", f"{resultado['p_val']:.4f}")
            if resultado['p_val'] < 0.05:
                st.success("Diferença estatisticamente significativa (p < 0.05)")
            else:
                st.warning("Diferença não estatisticamente significativa (p ≥ 0.05)")

        with textTestCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                Ao lado, temos os resultados do <strong>teste de hipótese</strong>, que busca avaliar se a 
                                <i>média da posição final</i> de <strong>Lewis Hamilton</strong> pode ser considerada 
                                estatisticamente melhor do que a de <strong>Nico Rosberg</strong>. Para isso, definimos o 
                                <i>nível de significância</i> em 5% (α = 0,05), ou seja, aceitamos correr um risco de até 5% 
                                de concluir que Hamilton é melhor quando, na verdade, não seria. 
                            </p>
                            <p class="text">
                                O resultado encontrado foi um <strong>p-valor de 0,0628</strong>. Em termos estatísticos, 
                                esse valor representa a probabilidade de observarmos uma diferença tão extrema (ou maior) entre 
                                Hamilton e Rosberg <i>caso a hipótese nula seja verdadeira</i>,  isto é, se não houver realmente 
                                diferença entre as médias. Como esse valor é <i>maior</i> que o nosso nível de significância de 5%, 
                                <strong>não podemos rejeitar H₀</strong> com segurança, o que significa que não há evidências 
                                estatísticas suficientes para afirmar que Hamilton teve, de forma consistente, uma média melhor 
                                que a de Rosberg.
                            </p>
                            <p class="text">
                                Entretanto, é interessante observar que o p-valor ficou muito próximo do limite adotado. 
                                Se ampliássemos ligeiramente a significância para 7% (α = 0,07), já seria possível rejeitar H₀, 
                                indicando que Hamilton teria sim uma vantagem estatisticamente significativa. 
                                Esse detalhe mostra como a interpretação de testes estatísticos deve ser feita com cuidado: 
                                a <i>significância estatística</i> não é um valor absoluto e rígido, mas sim um critério 
                                convencional para reduzir riscos de erro.
                            </p>
                            <p class="text">
                                Por fim, para fins desta análise exploratória, e considerando a proximidade do resultado com o 
                                limiar de decisão, adotaremos uma interpretação prática: a tendência sugere que Hamilton, de fato, 
                                apresentou uma média de desempenho superior ao Rosberg. Contudo, destacamos que estatisticamente 
                                essa conclusão ainda deve ser vista com cautela, pois não houve suporte suficiente ao nível de 
                                5% de significância. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )


    # Repetir o mesmo padrão para os outros companheiros
    elif companheiro == 'Valtteri Bottas':
        boxCol, textCol = st.columns(2, vertical_alignment='center')
        
        with boxCol:          
            df_ham_filtrado, df_bottas = filtrar_periodo_companheiro(df_ham, df_companheiro, "Valtteri Bottas")
            grafico_boxplot(df_ham_filtrado, df_bottas, "Valtteri Bottas", teammate_color="#00D2BE")
        
        with textCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                           <p class="text">
                                Após <strong>Nico Rosberg</strong>, foi a vez de <strong>Valtteri Bottas</strong> assumir o posto de 
                                <strong>companheiro de equipe</strong> de <strong>Lewis Hamilton</strong>. 
                                Hamilton chegava de uma temporada desafiadora, onde havia perdido o título para <strong>Rosberg</strong>, 
                                mas, já <i>tricampeão mundial</i> em <strong>2017</strong>, mostrou que a derrota não abalou sua 
                                <i>consistência</i> dentro da pista. O <i>boxplot</i> ao lado ilustra bem essa diferença: 
                                enquanto <strong>Bottas</strong> ainda buscava se adaptar à equipe, seus resultados apresentavam 
                                maior <i>dispersão</i> e valores mais altos, refletindo a dificuldade em manter o mesmo nível de 
                                <i>regularidade</i>. 
                                <strong>Hamilton</strong>, por outro lado, manteve uma <i>caixa</i> menor e mais baixa, sinal de que 
                                continuava entregando desempenhos sólidos e constantemente em posições de destaque. 
                                A <i>amplitude interquartil</i> reforça essa leitura: <strong>2</strong> para <strong>Hamilton</strong> 
                                contra <strong>3</strong> para <strong>Bottas</strong>, um indicativo claro de que os resultados do britânico 
                                oscilaram menos. 
                                Além disso, <strong>Bottas</strong> apresentou <i>outliers</i> mais elevados, representando provas em que seu 
                                desempenho caiu de forma significativa, algo menos frequente em <strong>Hamilton</strong>. 
                                Esses elementos, quando observados em conjunto, deixam evidente que <strong>Bottas</strong> teve um início de 
                                trajetória bem mais turbulento ao lado de um companheiro já consolidado no topo do <i>grid</i>.
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )
       
        textIcCol, icCol = st.columns(2, vertical_alignment='center')

        with textIcCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                Mas apenas o <i>boxplot</i> não é suficiente para afirmar se <strong>Lewis Hamilton</strong> realmente foi superior a 
                                <strong>Valtteri Bottas</strong> no quesito <strong>posição final</strong>. 
                                Para aprofundar a análise, foi feita uma <i>comparação de médias</i> acompanhada de seus respectivos 
                                <strong>intervalos de confiança</strong>, que permitem avaliar não apenas a posição média, mas também a 
                                <i>consistência</i> de cada piloto ao longo das temporadas. 
                                Ao lado, observamos que ambos começaram próximos, mas com o passar dos anos o <strong>intervalo de confiança</strong> 
                                de <strong>Bottas</strong> se tornou cada vez maior, refletindo uma <i>dispersão</i> crescente nos resultados, enquanto o de 
                                <strong>Hamilton</strong> se manteve relativamente estável, com sua média consistentemente menor que a de Bottas. 
                                Esse aumento de variabilidade, especialmente nos dois últimos anos, sugere que o <i>carro</i> da equipe já não estava 
                                tão dominante quanto antes. Ainda assim, <strong>Hamilton</strong> conseguiu manter sua <i>regularidade</i>, evidenciando que 
                                mesmo em condições menos favoráveis ele permanecia competitivo. 
                                Se o carro tivesse continuado extremamente dominante, esperaríamos ver ambos os pilotos sustentando médias mais baixas 
                                de posição final, como na época da dupla <strong>Hamilton–Rosberg</strong>. 
                                Diante disso, torna-se necessário aplicar um <strong>teste de hipótese</strong> a um nível de significância de 
                                <strong>5%</strong>, a fim de verificar estatisticamente se a vantagem de <strong>Hamilton</strong> sobre 
                                <strong>Bottas</strong> é de fato significativa. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )

        with icCol:
            # Gráfico de linha com IC
            fig_line_ic = grafico_comparacao_com_ic(df_ham_filtrado, df_bottas, "Valtteri Bottas")
            st.plotly_chart(fig_line_ic, use_container_width=True)
        
        testHipCol, textTestCol = st.columns([0.48,0.52], vertical_alignment='top')

        with testHipCol:

            # Teste de hipótese
            resultado = analise_intervalo_confianca(df_ham_filtrado, df_bottas)
            
            st.markdown("### 🧪 Teste de Hipótese")

            st.markdown("**H₀ (Hipótese Nula):**")
            st.latex(r"\mu_{\text{Hamilton}} \geq \mu_{\text{Bottas}}")
            st.markdown("> A posição média de **Hamilton** é igual ou **pior** que a do companheiro de equipe.")

            st.markdown("**H₁ (Hipótese Alternativa):**")
            st.latex(r"\mu_{\text{Hamilton}} < \mu_{\text{Bottas}}")
            st.markdown("> A posição média de **Hamilton** é **melhor** que a do companheiro de equipe.")

            # Exibir resultados
            col1, col2, col3 = st.columns(3)
            with col1:
                # Para Lewis Hamilton
                st.metric(
                    "Lewis Hamilton", 
                    f"{resultado['media_ham']:.2f}",
                    f"IC 95%: [{resultado['ic_ham'][0]:.2f}, {resultado['ic_ham'][1]:.2f}]"
                )
            with col2:
                # Para Valtteri Bottas  
                st.metric(
                    "Valtteri Bottas",
                    f"{resultado['media_tm']:.2f}",
                    f"IC 95%: [{resultado['ic_tm'][0]:.2f}, {resultado['ic_tm'][1]:.2f}]"
                )
            with col3:
                st.metric("Diferença", f"{resultado['media_ham'] - resultado['media_tm']:.2f}")
            
            st.metric("Valor p", f"{resultado['p_val']:.4f}")
            if resultado['p_val'] < 0.05:
                st.success("Diferença estatisticamente significativa (p < 0.05)")
            else:
                st.warning("Diferença não estatisticamente significativa (p ≥ 0.05)")

        with textTestCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                Ao lado, temos os resultados do <strong>teste de hipótese</strong> que compara a 
                                <i>média da posição final</i> de <strong>Lewis Hamilton</strong> com a de 
                                <strong>Valtteri Bottas</strong>. Novamente, adotamos um <i>nível de significância</i> 
                                de 5% (α = 0,05), o que significa aceitar um risco de até 5% de concluir que Hamilton 
                                é melhor quando, na realidade, não seria. 
                            </p>
                            <p class="text">
                                O resultado obtido foi um <strong>p-valor de 0,0003</strong>. Esse valor é extremamente 
                                baixo e indica que a probabilidade de observarmos uma diferença tão acentuada entre os 
                                dois pilotos <i>caso a hipótese nula fosse verdadeira</i> é de apenas 0,03%. 
                                Em termos estatísticos, isso representa uma evidência <strong>fortíssima</strong> contra H₀. 
                            </p>
                            <p class="text">
                                Como o <strong>p-valor</strong> é muito menor que o nosso nível de significância (0,0003 &lt; 0,05), 
                                <strong>rejeitamos H₀ com segurança</strong> e concluímos que <strong>Lewis Hamilton</strong> 
                                teve, de forma consistente, uma <i>média de posição final</i> melhor do que a de 
                                <strong>Valtteri Bottas</strong>. 
                            </p>
                            <p class="text">
                                Diferente do caso de <strong>Nico Rosberg</strong>, onde o resultado ficou na fronteira da decisão, 
                                aqui não há margem para dúvida: a evidência estatística é clara e robusta. 
                                Isso reforça a interpretação feita nos <i>boxplots</i> e nos <strong>intervalos de confiança</strong>, 
                                de que <strong>Hamilton</strong> manteve sua regularidade e dominância em relação ao seu 
                                companheiro de equipe ao longo dos anos. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )


    elif companheiro == 'George Russell':
        boxCol, textCol = st.columns(2, vertical_alignment='center')

        with boxCol:          
            df_ham_filtrado, df_russell = filtrar_periodo_russell(df_ham, df_companheiro)
            grafico_boxplot(df_ham_filtrado, df_russell, "George Russell", teammate_color="#6CD3BF")

        with textCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                O <i>boxplot</i> comparativo entre <strong>Lewis Hamilton</strong> e <strong>George Russell</strong> 
                                evidencia diferenças relevantes no comportamento de seus resultados desde que passaram a ser companheiros 
                                de equipe. A <i>caixa</i> de <strong>Russell</strong> é visivelmente menor, o que indica uma 
                                <strong>maior consistência</strong> em suas posições finais. Isso mostra que, mesmo sem liderar 
                                constantemente sobre Hamilton, Russell manteve desempenhos próximos entre si, com pouca variação. 
                            </p>
                            <p class="text">
                                Já <strong>Hamilton</strong>, embora em várias ocasiões tenha alcançado médias mais favoráveis, 
                                apresentou maior dispersão, alternando entre corridas de alto desempenho e outras aquém do esperado. 
                                Em resumo, Hamilton alcança picos mais altos, enquanto Russell se destaca pela estabilidade. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )

        textIcCol, icCol = st.columns([0.4,0.6], vertical_alignment='center')

        with textIcCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                A análise das <strong>médias com intervalo de confiança de 95%</strong> reforça o equilíbrio entre os dois pilotos. 
                                Curiosamente, <strong>Hamilton</strong> aparece com resultados médios ligeiramente piores em relação a <strong>Russell</strong>, 
                                terminando em posições finais um pouco mais altas. Esse comportamento pode refletir o impacto das mudanças de regulamento, 
                                que exigiram maior adaptação de Hamilton, enquanto Russell pareceu ajustar-se de forma mais natural. 
                            </p>
                            <p class="text">
                                Nos <strong>intervalos de confiança</strong>, observa-se que Hamilton mantém uma amplitude relativamente menor, 
                                sinalizando maior controle em seus desempenhos, enquanto Russell se destaca pela consistência ao longo das temporadas, 
                                reforçando sua rápida adaptação e a disputa interna pelo posto de <i>primeiro piloto</i> da Mercedes. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )

        with icCol:
            fig_line_ic = grafico_comparacao_com_ic(df_ham_filtrado, df_russell, "George Russell")
            st.plotly_chart(fig_line_ic, use_container_width=True)

        testHipCol, textTestCol = st.columns([0.48,0.52], vertical_alignment='top')

        with testHipCol:

            resultado = analise_intervalo_confianca(df_ham_filtrado, df_russell)
            
            st.markdown("### 🧪 Teste de Hipótese")

            st.markdown("**H₀ (Hipótese Nula):**")
            st.latex(r"\mu_{\text{Hamilton}} \geq \mu_{\text{Russell}}")
            st.markdown("> A posição média de **Hamilton** é igual ou **pior** que a do companheiro de equipe.")

            st.markdown("**H₁ (Hipótese Alternativa):**")
            st.latex(r"\mu_{\text{Hamilton}} < \mu_{\text{Russell}}")
            st.markdown("> A posição média de **Hamilton** é **melhor** que a do companheiro de equipe.")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Lewis Hamilton", 
                    f"{resultado['media_ham']:.2f}",
                    f"IC 95%: [{resultado['ic_ham'][0]:.2f}, {resultado['ic_ham'][1]:.2f}]"
                )
            with col2:
                st.metric(
                    "George Russell",
                    f"{resultado['media_tm']:.2f}",
                    f"IC 95%: [{resultado['ic_tm'][0]:.2f}, {resultado['ic_tm'][1]:.2f}]"
                )
            with col3:
                st.metric("Diferença", f"{resultado['media_ham'] - resultado['media_tm']:.2f}")
            
            st.metric("Valor p", f"{resultado['p_val']:.4f}")
            if resultado['p_val'] < 0.05:
                st.success("Diferença estatisticamente significativa (p < 0.05)")
            else:
                st.warning("Diferença não estatisticamente significativa (p ≥ 0.05)")

        with textTestCol:
            st.markdown(
                """
                    <div class="conteudo">
                        <div class="paragrafo">
                            <p class="text">
                                Para avaliar de forma objetiva se a diferença entre os desempenhos médios de <strong>Hamilton</strong> 
                                e <strong>Russell</strong> é estatisticamente significativa, foi realizado um <strong>teste de hipótese</strong> 
                                com nível de significância de 5% (α = 0,05). 
                            </p>
                            <p class="text">
                                O resultado encontrado foi um <strong>p-valor de 0,6255</strong>. Esse valor, muito acima do limite de 5%, 
                                mostra que <i>não podemos rejeitar a hipótese nula (H₀)</i>. Na prática, significa que não há evidências suficientes 
                                para afirmar que Hamilton apresenta, em média, um desempenho superior ao de Russell. 
                            </p>
                            <p class="text">
                                O p-valor elevado sugere que as diferenças observadas podem ser atribuídas a <strong>variações aleatórias</strong> 
                                de corrida para corrida, e não a uma vantagem estatisticamente clara de um piloto sobre o outro. 
                            </p>
                            <p class="text">
                                Portanto, embora os gráficos indiquem nuances interessantes, Hamilton com médias um pouco melhores 
                                e Russell com maior consistência, a análise estatística confirma que tais distinções não atingem 
                                <strong>significância estatística</strong>, devendo ser interpretadas com cautela. 
                            </p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        """
            <div class="conteudo">
                <div class="paragrafo">
                    <p class="text">
                        Em resumo, a análise comparativa entre Hamilton e seus companheiros de equipe evidencia um padrão claro: mesmo em contextos distintos de regulamento e competitividade do carro, Hamilton mostrou uma consistência estatística superior, com médias geralmente melhores ou pelo menos tão boas quanto as de seus pares. Bottas aparece como o adversário em que a diferença foi mais nítida, enquanto contra Rosberg e Russell a disputa se mostrou mais equilibrada, refletindo momentos de adaptação ou maior competitividade interna. Esses resultados reforçam que, apesar das variações, Hamilton manteve um desempenho sólido e competitivo em diferentes fases da sua
                    </p>
                </div>
                <hr>
            </div>
        """, unsafe_allow_html=True
    )


# ------------------------------
# Conclusão
# ------------------------------
def conclusao_conteudo() -> None:
    """Função Renderiza a conclusão"""
    st.markdown(
        """
            <div class="conteudo">
                <h2 class="titulo-2">Conclusão</h2>
                <div class="paragrafo">
                    <p class="text">
                        As métricas médias de <strong>Lewis Hamilton</strong> revelam um piloto que se manteve quase sempre entre as primeiras posições, com alto nível de consistência ao longo das temporadas (1). Seu desempenho apresentou uma trajetória de evolução contínua, principalmente nos primeiros anos de carreira, alcançando o auge entre 2014 e 2020; no entanto, mais recentemente, houve sinais de queda relacionados às condições técnicas, embora ele siga em patamar competitivo (2). As mudanças de regulamento tiveram impacto direto, sobretudo após 2022, resultando em quedas perceptíveis no rendimento médio, o que demonstra o peso das alterações técnicas sobre seu desempenho (3).
                    </p>
                    <p class="text">
                        Quando comparado aos seus companheiros de equipe, Hamilton mostrou-se superior a <strong>Bottas</strong> em constância, disputou de forma mais equilibrada com <strong>Rosberg</strong> e, mais recente, enfrentou uma rivalidade crescente com <strong>Russell</strong>, mas ainda preserva vantagens importantes em termos de regularidade e controle (4). O período entre 2014 e 2020 pode ser classificado como de <i>dominância clara</i>, em que a superioridade da Mercedes desempenhou papel central; ainda assim, a forma como Hamilton converteu essa vantagem em títulos e recordes reforça que a dominância foi também fruto de sua habilidade individual (5).
                    </p>
                    <p class="text">
                        Assim, a análise evidencia que Hamilton construiu uma carreira marcada por consistência, capacidade de evolução e adaptação a diferentes cenários, confirmando-se como um dos pilotos mais dominantes da <strong>Formula 1</strong>, mesmo diante das oscilações mais recentes. Ainda assim, seria necessário aprofundar a investigação em métricas como <strong>vitórias</strong>, <strong>pódios</strong> e <strong>pole positions</strong> para enriquecer a compreensão completa do seu impacto competitivo.
                    </p>
                </div>
                <hr>
            </div>
        """, unsafe_allow_html=True
    )



# ------------------------------
# Renderizando tudo
# ------------------------------
def conteudo() -> None:
    """Função para renderizar o conteúdo da página de Análise de Dados"""
    st.markdown(
        """
        <div class="conteudo">
            <h1>Análise de Dados</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    contextTab, dadosTab, prepTab, classificacaoTab, analiseTab, conclusaoTab = st.tabs(
        [
            ":material/contextual_token: Contexto",
            ":material/table: Dados Disponíveis",
            ":material/healing: Preparação",
            ":material/search_insights: Classificação de Variáveis",
            ":material/analytics: Análise",
            ":material/pin_end: Conclusão"
        ]
    )
    
    with contextTab:
        contexto_conteudo()
    with dadosTab:
        dados_conteudo()
    with prepTab:
        preparacao_conteudo()
    with classificacaoTab:
        classificacao_conteudo()
    with analiseTab:
        analise_conteudo()
    with conclusaoTab:
        conclusao_conteudo()


conteudo()
