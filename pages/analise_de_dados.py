# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Importando funções auxiliares
from utils.api_wiki import get_wikipedia_summary
from utils.tratamento_dados import *

# ------------------------------
# Variáveis Globais
# ------------------------------
DATA_FRAME = {}
PILOTO = "Lewis Hamilton"
    
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
                    <p class="text">Nosso foco principal é a quinta pergunta: <strong>o que significa ser dominante?</strong> Para chegar a essa resposta, começaremos explorando as outras questões e, ao final, verificaremos se é possível afirmar ou não essa dominância. É provável que seja necessária uma análise mais ampla e detalhada, mas por enquanto, sabendo qual é nosso objetivo, o próximo passo é o <strong>tratamento de dados</strong>!</p>
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
                <div class="paragrafo">
                    <h3 class="titulo-3">DataFrame para Análise</h3>
                    <p class="text">
                        Como podemos observar acima, as tabelas <strong>Resultados das Sprints</strong> 
                        e <strong>Resultados das Corridas</strong> possuem as mesmas colunas. 
                        Portanto, podemos concatená-las em um único DataFrame para obter um panorama 
                        geral dos anos e do total de pontos, afinal, ambas podem ser consideradas corridas. 
                        A diferença é que as <strong>Sprints</strong> são corridas mais curtas e, 
                        apesar de muitos pilotos não apreciarem esse formato, seus pontos ainda são relevantes 
                        para a análise. <br><br>
                        Além disso, é importante incluir o ano em que cada corrida aconteceu, 
                        facilitando a filtragem dos períodos em que Lewis Hamilton esteve ativo na Fórmula 1. 
                        Com isso em mente, vamos construir esse DataFrame:
                    </p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
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
    
    contextTab, dadosTab, prepTab, apresentacaoTab, analiseTab, conclusaoTab = st.tabs(
        [
            ":material/contextual_token: Contexto",
            ":material/table: Dados Disponíveis",
            ":material/healing: Preparação",
            ":material/search_insights: Apresentação",
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


conteudo()
