# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Importando funções auxiliares
from utils.dashboard_utils import *

# ------------------------------
# Variáveis Globais
# ------------------------------
DATA_FRAME = {}

# ------------------------------
# Renderizando tudo
# ------------------------------
def conteudo() -> None:
    """Função para renderizar o conteúdo da página de Dashboard"""

    st.markdown(
        """
        <div class="conteudo">
            <h1 style="text-align:center;">🏎️ Dashboard de Análise 📊</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Carregando dados
    df_pilotos = merge_tabelas()
    df_pilotos = df_pilotos.dropna(subset=['code'])
    lista_pilotos = df_pilotos['nome_completo'].unique()

    # Seleção do piloto
    piloto = st.selectbox("Selecione o Piloto:", lista_pilotos)

    if piloto:
        listas_anos = df_pilotos[df_pilotos['nome_completo'] == piloto]
        ano = st.selectbox("Selecione o ano:", sorted(listas_anos['ano'].unique()))
        # Filtra apenas o ano selecionado
        df_filtrado = listas_anos[listas_anos['ano'] == ano]

        # Verifica quantidade de registros
        qtde = len(df_filtrado)

        if qtde > 1:
            st.success(f"O ano {ano} possui {qtde} registros.")
        elif qtde == 1:
            st.info(f"O ano {ano} possui apenas 1 registro.")
        else:
            st.error(f"O ano {ano} não possui registros (possível bagunça!).")

        st.subheader(f"📌 Sobre {piloto}")

        st.markdown("### 🏁 Informações Rápidas")
        st.markdown(f"""
        - **Nacionalidade:** {df_pilotos[df_pilotos['nome_completo']==piloto]['nacionalidade_piloto'].iloc[0] if 'nacionalidade_piloto' in df_pilotos.columns else '❓'}
        - **Equipe:** {df_pilotos[df_pilotos['nome_completo']==piloto]['nome_equipe'].iloc[-1]}
        - **Número do Carro:** {df_pilotos[df_pilotos['nome_completo']==piloto]['numero_do_piloto'].iloc[-1]}
        - **Corridas Disputadas:** {len(df_pilotos[df_pilotos['nome_completo']==piloto])}
        - **Vitórias:** {df_pilotos[df_pilotos['nome_completo']==piloto]['posicao_final'].eq(1).sum()}
        - **Pódios:** {df_pilotos[df_pilotos['nome_completo']==piloto]['posicao_final'].le(3).sum()}
        """)

        st.divider()
        st.markdown(f"### 📊 Estatísticas de {ano}")

        # Filtrando dados do piloto no ano selecionado
        df_filtrado = listas_anos[listas_anos['ano'] == ano].copy()

        lista_cores = df_filtrado['cores'].iloc[0]

        # Criando coluna auxiliar para gráficos
        df_filtrado["posicao_plot"] = df_filtrado["posicao_final"].fillna(25)  # desqualificado vai para 25
        df_filtrado["status_corrida"] = df_filtrado["posicao_final"].apply(
            lambda x: "Desqualificado" if pd.isna(x) else "Terminou"
        )

        # ===== Gráfico 1 - Posições finais =====
        fig1 = px.line(
            df_filtrado,
            x="rodada",
            y="posicao_plot",
            markers=True,
            title=f"📈 Posições Finais de {piloto} em {ano}",
            labels={"rodada": "Corrida", "posicao_plot": "Posição Final"},
        )
        fig1.update_yaxes(autorange="reversed")

        # Marcar os desqualificados em vermelho
        df_desq = df_filtrado[df_filtrado["status_corrida"] == "Desqualificado"]
        if not df_desq.empty:
            fig1.add_scatter(
                x=df_desq["rodada"],
                y=df_desq["posicao_plot"],
                mode="markers",
                marker=dict(color="red", size=12, symbol="x"),
                name="Desqualificado",
            )

        st.plotly_chart(fig1, use_container_width=True)

        col1, col2 = st.columns(2, vertical_alignment='center')

        with col1:
            # ===== Gráfico 2 - Ganho de posições =====
            df_filtrado["ganho_plot"] = df_filtrado.apply(
                lambda row: row["ganho_posicao"] 
                if row["status_corrida"] == "Terminou" 
                else -10,  # valor negativo grande p/ DSQ
                axis=1
            )

            fig2 = px.bar(
                df_filtrado,
                x="rodada",
                y="ganho_plot",
                title=f"📊 Ganho de Posições de {piloto} em {ano}",
                labels={"rodada": "Corrida", "ganho_plot": "Posições Ganhadas"},
                color="status_corrida",
                color_discrete_map={"Terminou": "green", "Desqualificado": "red"},
            )

            # Deixar os DSQ bem destacados
            fig2.update_traces(marker_line_width=1.5, marker_line_color="black")

            # Linha de referência no 0
            fig2.add_hline(y=0, line_dash="dash", line_color="black")

            st.plotly_chart(fig2, use_container_width=True)


        with col2: 
            # ===== Gráfico 3 - Distribuição de posições finais =====
            df_hist = df_filtrado.copy()
            df_hist["posicao_final_hist"] = df_hist["posicao_final"].fillna("Desqualificado")

            fig3 = px.histogram(
                df_hist,
                x="posicao_final_hist",
                nbins=10,
                title=f"📊 Distribuição das Posições Finais ({ano})",
                labels={"posicao_final_hist": "Posição Final"},
                color_discrete_sequence=[lista_cores[0]]
            )
            st.plotly_chart(fig3, use_container_width=True)

        # ===== Tabela =====
        with st.expander("📋 Ver dados brutos"):
            st.dataframe(df_filtrado[["rodada", "ano", "posicao_final", "ganho_posicao", "status_corrida"]])

    else:
        st.warning("Selecione um piloto para visualizar o dashboard.")


conteudo()
