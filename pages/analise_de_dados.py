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

    # ---- Contexto Fórmula 1 ----
    col1, col2 = st.columns([1, 1], vertical_alignment="center")

    with col1:
        st.markdown(
            """
                <div class="conteudo">
                    <h2 class="titulo-2">Contexto</h2>
                    <div class="paragrafo">
                        <p class="text">A <strong>Fórmula 1</strong> é considerada, por muitos, o ápice do automobilismo mundial: a vitrine máxima onde talento, ousadia e disciplina se encontram em um espetáculo que mistura velocidade, tecnologia e emoção. Para a maioria dos pilotos, desde os primeiros passos nas <i>categorias de base</i> até os sonhos de infância, chegar à <strong>Fórmula 1</strong> já é uma conquista quase inimaginável. Poucos conseguem superar todas as barreiras financeiras, físicas e mentais para finalmente se sentar no <i>cockpit</i> de um carro da categoria, competindo lado a lado com alguns dos maiores nomes da história do esporte.</p>
                        <p class="text">No entanto, estar presente no <i>grid</i> é apenas o início de um caminho árduo. Vencer na Fórmula 1 exige não apenas habilidade inata, mas também uma combinação rara de estratégia, preparo físico impecável, confiança e, muitas vezes, estar no lugar certo na hora certa. Ainda mais raro é transformar vitórias isoladas em consistência ao longo de uma temporada inteira, alcançando o tão sonhado título mundial. Esse feito é reservado a uma minoria absoluta, um grupo seleto de pilotos que se eterniza nos livros da categoria.</p>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.image(
            "https://f1saopaulo.com.br/wp-content/uploads/2024/01/Sem-conteudo-1-1.png",
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
                    <h2 class="conteudo2">Sobre Lewis Hamilton</h2>
                    <div class="paragrafo">
                        <p class="text"><strong>Lewis Hamilton</strong> é um dos nomes mais marcantes da história da Fórmula 1. Nascido em Stevenage, Inglaterra, começou sua trajetória no <i>kart</i> ainda muito jovem e rapidamente se destacou pela combinação de talento natural e determinação. Ao longo dos anos construiu uma carreira que o levou do sonho de criança ao patamar mais alto do automobilismo mundial, tornando-se não apenas campeão, mas também uma figura de grande impacto dentro e fora das pistas. Sua trajetória é marcada por conquistas expressivas, recordes impressionantes e uma presença que ultrapassa o universo esportivo, consolidando-o como um dos grandes ícones da era moderna do esporte a motor.</p>
                        <p class="text">Nesta análise, revisitaremos cada temporada do heptacampeão até 2024, último ano de sua longa passagem pela <strong>Mercedes</strong>, equipe com a qual conquistou seis de seus títulos. A questão que guia nossa investigação é clara: Hamilton é realmente tão bom quanto parece ou foi apenas o carro, como muitas pessoas podem pensar?</p>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.divider()


def tratamento_conteudo() -> None:
    """Função para renderizar a página de tratamento"""
    st.markdown(
        """
            <div class="conteudo">
                <h2 class="titulo-2">Tratamento de Dados</h2>

                <div class="paragrafo">
                    <p class="text"><strong>Lewis Hamilton</strong> é um dos nomes mais marcantes da história da Fórmula 1. Nascido em Stevenage, Inglaterra, começou sua trajetória no <i>kart</i> ainda muito jovem e rapidamente se destacou pela combinação de talento natural e determinação. Ao longo dos anos construiu uma carreira que o levou do sonho de criança ao patamar mais alto do automobilismo mundial, tornando-se não apenas campeão, mas também uma figura de grande impacto dentro e fora das pistas. Sua trajetória é marcada por conquistas expressivas, recordes impressionantes e uma presença que ultrapassa o universo esportivo, consolidando-o como um dos grandes ícones da era moderna do esporte a motor.</p>
                    <p class="text">Nesta análise, revisitaremos cada temporada do heptacampeão até 2024, último ano de sua longa passagem pela <strong>Mercedes</strong>, equipe com a qual conquistou seis de seus títulos. A questão que guia nossa investigação é clara: Hamilton é realmente tão bom quanto parece ou foi apenas o carro, como muitas pessoas podem pensar?</p>
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
    
    contextTab, tratamentoTab, apresentacaoTab, analiseTab, conclusaoTab = st.tabs(
        [
            ":material/contextual_token: Contexto",
            ":material/healing: Tratamento",
            ":material/search_insights: Apresentação",
            ":material/analytics: Análise",
            ":material/pin_end: Conclusão"
        ]
    )
    
    with contextTab:
        contexto_conteudo()
    with tratamentoTab:
        tratamento_conteudo()


conteudo()
