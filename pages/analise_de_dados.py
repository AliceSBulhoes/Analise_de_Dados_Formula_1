# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
# Importando funções auxiliares
from utils.tratamento_dados import *
from utils.api_wiki import get_wikipedia_summary

# ------------------------------
# Variáveis Globais
# ------------------------------
DATA_FRAME = {}
PILOTO = ""
    
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


conteudo()
