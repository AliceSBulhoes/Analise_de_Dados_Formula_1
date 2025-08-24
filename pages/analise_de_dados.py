# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
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
                        Com intuito de analisar a carreira de Lewis Hamilton na Formula 1, o primeiro passo será observar sua consistência ao longo das temporadas, avaliando medidas como médias, medianas e desvios-padrão de seus resultados, além de métricas gerais como vitórias, pódios, poles e pontos. Em seguida, a análise será segmentada entre os anos de McLaren e de Mercedes, permitindo comparar a distribuição de seus desempenhos em cada equipe e identificar diferenças estatísticas relevantes. Também será investigado o impacto das mudanças de regulamento, utilizando intervalos de confiança e análise de dispersão para compreender como essas transições afetaram seu rendimento. Por fim, Hamilton será comparado aos seus companheiros de equipe, especialmente na Mercedes, aplicando testes de hipótese para verificar se, em média, seus resultados foram significativamente superiores aos dos colegas de time.
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


conteudo()
