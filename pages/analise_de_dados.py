# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
# Importando funções auxiliares
from utils.data_fetch import *
from utils.api_wiki import get_wikipedia_summary

# ------------------------------
# Variáveis Globais
# ------------------------------
DATA_FRAME = {}
PILOTO = ""

# ------------------------------
# Selecionar o Piloto
# ------------------------------
def selecionar_piloto() -> None:
    """Função para selecionar o piloto a ser analisado"""
    # Lista de pilotos disponíveis
    pilotos = ["Lewis Hamilton"]

    # Carregar os dados dos pilotos
    PILOTO = st.sidebar.selectbox("Escolha um piloto:", pilotos)
    piloto_name = PILOTO.split()

    # Coletar o DataFrame do piloto selecionado
    df_corridas = get_corridas_piloto(piloto_name[0], piloto_name[1])

    # Verificar se o DataFrame está vazio
    if df_corridas.empty:
        st.warning("Nenhum dado encontrado para o piloto selecionado.")
        return

    # Adicionar o DataFrame ao dicionário global
    DATA_FRAME["df_corridas"] = df_corridas
    DATA_FRAME["df_piloto_info"] = get_piloto_info(piloto_name[0], piloto_name[1])
    

# ------------------------------
# Contexto
# ------------------------------
def contexto_conteudo() -> None:
    """Função para renderizar o contexto do conteúdo"""    
    col1, col2 = st.columns([1, 1], vertical_alignment='center')

    with col1:
        st.markdown(
            """
                <div class="content">
                    <h2>Contexto</h2>
                    <div class="contexto">
                        <p>A <strong>Fórmula 1</strong> é a categoria mais prestigiada do automobilismo mundial. Muitos pilotos sonham em competir nesse nível, mas apenas alguns conseguem transformar esse objetivo em realidade. Dentre esses, poucos alcançam o título de campeão mundial.</p>
                        <p>Esta análise tem como foco investigar se apenas o talento é suficiente para conquistar o topo ou se outros fatores, como esforço e contexto, também são determinantes.</p>
                        <p>Ao navegar por este dashboard, é possível acompanhar a evolução dos pilotos ao longo das temporadas e observar como diferentes elementos influenciam o desempenho nas pistas. Fatores como a equipe, o carro utilizado e as condições da corrida são peças importantes desse quebra-cabeça competitivo.</p>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.image(
            "https://f1saopaulo.com.br/wp-content/uploads/2024/01/Sem-Titulo-1-1.png",
            use_container_width=True,
        )

# ------------------------------
# Renderizando tudo
# ------------------------------
def conteudo() -> None:
    """Função para renderizar o conteúdo da página de Análise de Dados"""
    st.markdown(
        """
        <div class="titulo">
            <h1>Análise de Dados</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    contexto_conteudo()
    sobre_piloto()



selecionar_piloto()
conteudo()
