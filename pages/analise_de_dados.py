# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objects as go
# Importando funções auxiliares
from utils.api_wiki import get_wikipedia_summary
from utils.get_info import *
from utils.prepracao_dados import *

# ------------------------------
# Variáveis Globais
# ------------------------------
DATA_FRAME = {}
PILOTO = "Lewis Hamilton"

def get_rgba(color_name, alpha=0.2):
    """Converte nome de cor ou hex em rgba transparente"""
    rgb = mcolors.to_rgb(color_name)  # retorna valores entre 0–1
    return f"rgba({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)},{alpha})"

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
                        Já a tabela <strong>Lewis Hamilton Resultados</strong> mantém a mesma estrutura, 
                        mas adiciona a coluna <i>"vitorias"</i>, permitindo identificar 
                        quantas vezes o piloto terminou em primeiro lugar. Essa métrica é fundamental 
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
                        A análise dos valores nulos mostra que as colunas <i>"ganho_posicao"</i> e 
                        <i>"posicao_final"</i> apresentam a mesma quantidade de registros ausentes. 
                        Isso pode parecer uma coincidência à primeira vista, mas faz sentido dentro 
                        do contexto da Formula 1.                  
                        Nem todos os pilotos concluem a corrida: acidentes, falhas mecânicas ou 
                        outros problemas podem levar ao <strong>DNF (Did Not Finish)</strong>. 
                        Nesses casos, a ausência de informação não representa uma inconsistência, 
                        mas sim o reflexo da realidade da prova. <br><br>
                        Portanto, podemos considerar que a base de dados já passou por um tratamento 
                        inicial adequado.
                        Entretanto, antes de prosseguir, é fundamental verificar se ainda existem 
                        <strong>linhas duplicadas</strong>, garantindo que nossa análise não seja 
                        enviesada por registros repetidos.
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
                        A verificação de duplicatas mostra que não há registros repetidos nos DataFrames. 
                        Esse resultado confirma que o processo de preparação inicial dos dados foi consistente, 
                        garantindo maior confiabilidade para as próximas etapas.
                        Com essa base validada, podemos avançar para a 
                        <strong>classificação das variáveis</strong> e a definição das visualizações 
                        mais adequadas para a análise.
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
        ("vitorias", "Quantitativa Discreta", "Um booleano em 0/1 representa se Hamilton venceu (1) ou não venceu (0) uma corrida. É considerado quantitativa discreta por assumir apenas dois valores inteiros possíveis e permitir cálculos estatísticos, como soma e média."),
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
                <h2 class="titulo-2">Análise dos Dados</h2>]
                <div class="paragrafo">
                    <p class="text">
                        Com o intuito de fazermos uma análise dos dados que possuimos sobre o Lewis Hamilton e sua carreira, o primeiro passo é verificar a sua consistência ao longo das suas temporadas. Vale ressaltar que 
                    </p>
                </div>
                <h3 class="titulo-3">📈 Consistência e Evolução</h2>
                <div class="paragrafo">
                    <p class="text">
                        Aqui analisamos a evolução de Lewis Hamilton ao longo das temporadas,
                        observando medidas centrais (média, mediana, moda) e também medidas
                        de dispersão (desvio padrão). Isso nos ajuda a avaliar a regularidade
                        do piloto em diferentes fases da carreira.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True
    )

    # Exemplo: calcular métricas por temporada
    resumo_hamilton = (
        DATA_FRAME['df_dados_LH']
        .groupby("ano")["posicao_final"]
        .agg(["mean","median","std"])
        .reset_index()
    )

    # 🔹 Adiciona colunas de equipe e cor
    resumo_hamilton["time"] = resumo_hamilton["ano"].apply(
        lambda x: "McLaren" if x <= 2012 else "Mercedes"
    )
    resumo_hamilton["cores"] = resumo_hamilton["time"].map({
        "McLaren": "orange",
        "Mercedes": "silver"
    })

    col1, col2 = st.columns([0.3,0.7], vertical_alignment='center')

    with col1:
        st.dataframe(resumo_hamilton)

    with col2:
        # Gráfico interativo
        fig = go.Figure()

        for equipe in resumo_hamilton["time"].unique():
            df_equipe = resumo_hamilton[resumo_hamilton["time"] == equipe]
            cor = df_equipe["cores"].iloc[0]

            # Linha da média
            fig.add_trace(go.Scatter(
                x=df_equipe["ano"],
                y=df_equipe["mean"],
                mode="lines+markers",
                name=f"Média ({equipe})",
                line=dict(color=cor, width=3),
                marker=dict(size=8, color=cor)
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

        # Layout
        fig.update_layout(
            title="📈 Evolução da Posição Média do Hamilton por Ano",
            xaxis_title="Ano",
            yaxis_title="Posição Final (média)",
            template="plotly_white",
            hovermode="x unified",
            legend=dict(bordercolor="gray", borderwidth=0.5)
        )

        st.plotly_chart(fig, use_container_width=True)


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
