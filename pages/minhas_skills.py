import streamlit as st

# =====================
# Função para exibir Skills estilo "Fórmula 1"
# =====================
def skill_card(nome, nivel):
    # Define níveis com ícones de F1
    if nivel >= 0.9:
        titulo, emoji, cor = "🏆 Campeão Mundial", "👑", "#FFD700"
    elif nivel >= 0.75:
        titulo, emoji, cor = "🥈 Piloto Titular", "🔥", "#E10600"  # Vermelho Ferrari
    elif nivel >= 0.5:
        titulo, emoji, cor = "🚥 Rookie", "⚡", "#1E90FF"  # Azul Mercedes
    else:
        titulo, emoji, cor = "🔧 Piloto de Testes", "🛠️", "#32CD32"  # Verde Aston Martin

    return f"""
    <div style="
        border: 3px solid {cor};
        border-radius: 20px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        background: rgba(255,255,255,0.05);
        box-shadow: 0px 0px 15px {cor}66;
        min-height: 38dvh;
        max-height: 80dvh;
        display: flex;
        flex-direction: column;
        align-content: center;
        justify-content: center;
        align-items: center;
    ">
        <h2 style="text-align: center">{emoji} {nome}</h2>
        <p style="font-size:18px;"><b>Status:</b> {titulo}</p>
        <div style="background:#222; border-radius:12px; height:20px; width:100%; margin:10px 0;">
            <div style="background:{cor}; height:20px; width:{int(nivel*100)}%; border-radius:12px;"></div>
        </div>
        <p style="font-size:16px;">🏁 Performance: {int(nivel*100)}%</p>
    </div>
    """

def mostrar_skills(skills, titulo, icone):
    st.markdown(f"""
    <div class="titulo">
        <h2 class="titulo2">{icone} {titulo}</h2>
    </div>
    """, unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (skill, nivel) in enumerate(skills.items()):
        with cols[i % 3]:
            st.markdown(skill_card(skill, nivel), unsafe_allow_html=True)

# =====================
# Dados (Hard e Soft Skills)
# =====================
hard_skills = {
    "Python": 0.95,
    "SQL": 0.85,
    "Power BI": 0.4,
    "Streamlit": 0.85,
    "Git/GitHub": 0.85,
    "Estatística": 0.9,
    "Inglês": 0.8,
    "Pacote Office": 0.7,
    "JavaScript": 0.9,
    "HTML/CSS": 0.99,
    "Java": 0.75,
    "Pandas": 0.95,
}

soft_skills = {
    "Comunicação": 0.85,
    "Trabalho em equipe": 0.95,
    "Resolução de problemas": 0.85,
    "Gestão do tempo": 0.8,
    "Pensamento crítico": 0.95,
    "Criatividade": 0.75,
    "Aprendizado contínuo": 0.95,
    "Capacidade analítica": 0.90,
    "Flexibilidade": 0.90
}

# =====================
# Layout final
# =====================
st.markdown(
    """
    <div class="conteudo">
        <h1 class="sobre-titulo">🏎️ Minhas Skills</h1>
        <p class="sobre-subtitulo">Soft e Hard Skills acelerando rumo ao título mundial 🏆</p>
    </div>
    """,
    unsafe_allow_html=True,
)

mostrar_skills(hard_skills, "Hard Skills", "💻")
st.divider()
mostrar_skills(soft_skills, "Soft Skills", "🌱")
