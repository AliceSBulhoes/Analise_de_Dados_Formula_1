# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
# Importando funções auxiliares
from utils.get_info import *
from utils.api_wiki import get_wikipedia_summary

# ------------------------------
# Variáveis Globais
# ------------------------------
DATA_FRAME = {}
PILOTO = ""
    
# ------------------------------
# Renderizando tudo
# ------------------------------
def conteudo() -> None:
    """Função para renderizar o conteúdo da página de Análise de Dados"""
    st.markdown(
        """
        <div class="titulo">
            <h1>Dashboard</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )



conteudo()
