import streamlit as st

# =====================
# Dicionário de Tecnologias
# =====================
TECNOLOGIAS = {
    "Python": "🐍 Python",
    "SQL": "💾 SQL",
    "Power BI": "📊 Power BI",
    "Machine Learning": "🤖 Machine Learning",
    "Streamlit": "🚀 Streamlit"
}

# =====================
# Função: Mostrar Certificados em Cards
# =====================
def mostrar_certificados(certificados):
    st.markdown(
        """
        <div class="titulo-certificados">
            <h1>📜 Minha Jornada de Certificados</h1>
            <p>Filtre por tecnologia para ver os cursos relacionados 🚀</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Opções de tecnologias
    todas_tecnologias = list(TECNOLOGIAS.keys())

    # Multiselect com "Todas" como default
    tecnologias_escolhidas = st.multiselect(
        "🔧 Escolha as tecnologias:",
        todas_tecnologias,
    )

    # Lógica do filtro
    if "Todas" in tecnologias_escolhidas or not tecnologias_escolhidas:
        certificados_filtrados = certificados
    else:
        certificados_filtrados = [
            c for c in certificados 
            if any(t in tecnologias_escolhidas for t in c["tecnologias"])
        ]

    # Renderizar em formato de cards
    if certificados_filtrados:
        cols = st.columns(3)  # 3 cards por linha

        for idx, cert in enumerate(certificados_filtrados):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.subheader(cert['titulo'])
                    st.write(f"🏫 **Instituição:** {cert['instituicao']}")
                    lista_tec = ", ".join([TECNOLOGIAS[t] for t in cert["tecnologias"]])
                    st.write(f"🔧 **Tecnologias:** {lista_tec}")
                    if cert['imagem']:
                        st.image(cert["imagem"], caption=cert["titulo"], use_container_width=True)
                    st.link_button("🔗 Ver Certificado", cert["link"])
                    
    else:
        st.info("Nenhum certificado encontrado para as tecnologias selecionadas.")


# =====================
# Exemplo de uso
# =====================
certificados = [
    {
        "titulo": "Fundamentos de Python e SQL",
        "instituicao": "DataCamp",
        "link": "https://example.com/python-sql-certificado",
        "tecnologias": ["Python", "SQL"],
        "imagem": ""
    },
    {
        "titulo": "Análise de Dados com Power BI",
        "instituicao": "DIO",
        "link": "https://example.com/powerbi-certificado",
        "tecnologias": ["Power BI"],
        "imagem": ""
    },
    {
        "titulo": "Machine Learning Básico com Python",
        "instituicao": "Coursera",
        "link": "https://example.com/ml-certificado",
        "tecnologias": ["Python", "Machine Learning"],
        "imagem": ""
    },
    {
        "titulo": "Construindo Apps de Dados",
        "instituicao": "Streamlit Academy",
        "link": "https://example.com/streamlit-certificado",
        "tecnologias": ["Python", "Streamlit"],
        "imagem": ""
    }
]

mostrar_certificados(certificados)
