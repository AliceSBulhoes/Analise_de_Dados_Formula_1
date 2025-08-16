import streamlit as st
import os

def navbar() -> None:
    """Função para renderizar a barra de navegação"""

    st.logo(os.path.abspath("assets/img/formula_1_logo.png"))

    # Dicionário com as páginas
    pages = {
        "": [
            st.Page("pages/sobre.py", title="Sobre"),
            st.Page("pages/minhas_skills.py", title="Minhas Skills"),
            st.Page("pages/analise_de_dados.py", title="Análise de Dados"),
        ]
    }

    # Rodando a barra de navegação
    pg = st.navigation(pages)
    pg.run()


def carregando_estilos() -> None:
    """Função para carregar os estilos do CSS"""

    # Carregando o CSS
    with open("style/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def config() -> None:
    """Função para configurar o Streamlit"""

    # Configurações do Streamlit
    st.set_page_config(
        page_title="Data Science",
        page_icon=":material/bid_landscape:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

# Executando as funções
config()
carregando_estilos()
navbar()  