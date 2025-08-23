import streamlit as st
import os

# =====================
# Dicionário de Tecnologias
# =====================
TECNOLOGIAS = {
    "Python": "🐍 Python",
    "SQL": "💾 SQL",
}

# =====================
# Função: Mostrar Certificados em Cards
# =====================
def mostrar_certificados(certificados):
    st.markdown(
        """
        <div class="conteudo">
            <h1 class="titulo sobre-titulo">📜 Minha Jornada de Certificados</h1>
            <p class="subtitulo sobre-subtitulo">Filtre por tecnologia para ver os cursos relacionados 🚀</p>
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
        cols = st.columns(2)  # 3 cards por linha

        for idx, cert in enumerate(certificados_filtrados):
            with cols[idx % 2]:
                with st.container(border=True):
                    st.subheader(cert['titulo'])
                    st.write(f"🏫 **Instituição:** {cert['instituicao']}")
                    lista_tec = ", ".join([TECNOLOGIAS[t] for t in cert["tecnologias"]])
                    st.write(f"🔧 **Tecnologias:** {lista_tec}")
                    if cert['imagem']:
                        st.image(cert["imagem"], caption=cert["titulo"], use_container_width=True)
                    st.link_button("🔗 Ver Certificado", cert["link"], use_container_width=True)
                    
    else:
        st.info("Nenhum certificado encontrado para as tecnologias selecionadas.")


# =====================
# Exemplo de uso
# =====================
certificados = [
    {
        "titulo": "Python",
        "instituicao": "FIAP",
        "link": "https://on.fiap.com.br/pluginfile.php/1/local_nanocourses/certificado_nanocourse/114536/b81b9571057f832a17116778992a703b/certificado.png",
        "tecnologias": ["Python"],
        "imagem": "https://on.fiap.com.br/pluginfile.php/1/local_nanocourses/certificado_nanocourse/114536/b81b9571057f832a17116778992a703b/certificado.png"
    },
    {
        "titulo": "Python: análise de dados com SQL",
        "instituicao": "ALURA",
        "link": "https://cursos.alura.com.br/certificate/3b5ff2ca-d960-4c69-84a2-83f884ae31e9?lang",
        "tecnologias": ["Python", "SQL"],
        "imagem": os.path.abspath("assets/img/python_e_sql.png")
    }
]

mostrar_certificados(certificados)
