import streamlit as st
import random
from datetime import datetime

# =====================
# HEADER
# =====================
st.markdown(
    """
    <div class="conteudo">
        <h1 class="titulo sobre-titulo">👋 Olá, eu sou a Alice!</h1>
        <p class="sobre-subtitulo">Apaixonada por dados, Fórmula 1 e mundos imaginários</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# =====================
# SOBRE MIM
# =====================
st.markdown(
    """
    <div class="conteudo">
        <h2 class="titulo-2">✨ Sobre Mim</h2>
    </div>
    <div class="paragrafo">
        <p class="caption">
            “Ultimately, every human is their own writer.” — Han Sooyoung
        </p>
        <p class="text">
        Sou a <b>Alice</b>, uma pessoa em constante aprendizado.<br>
        Acredito que cada dia é uma oportunidade de evolução, seja explorando dados ou descobrindo novas histórias.
        </p>
        <p class="text">
        Minha paixão por <b>Fórmula 1</b> me inspira a enxergar o mundo dos dados de forma estratégica: assim como uma equipe analisa a <i>telemetria</i> para decidir o momento certo de um <i>pit stop</i>,
        acredito que os dados são o <b>combustível essencial</b> para transformar informação em decisão.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================
# HOBBIES
# =====================
st.markdown("""
           <div class="conteudo">
                <h2 class="conteudo2">📚 Hobbies</h2>
            </div>
            """, unsafe_allow_html=True)

with st.expander("🎬 Anime, Séries e Filmes"):
    st.metric("Títulos assistidos", "150+")
    st.write("Adoro explorar universos narrativos, de animes emocionantes até séries cheias de plot twists.")
    st.info("✨ Favoritos: One Piece, 1917 e Duna.")

with st.expander("📖 Ficção Científica, Novels e Mangás"):
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Livros lidos", "50+")
    with col2:
        st.metric("Mangás acompanhados", "10+")
    st.write("A ficção científica me inspira a imaginar futuros possíveis e refletir sobre tecnologia e humanidade.")
    st.success("🌌 Autores favoritos: Isaac Asimov, Sing Shong e Eiichiro Oda.")

with st.expander("🎮 Video Games"):
    st.metric("Jogos favoritos", "15+")
    st.write("Gosto de mergulhar em mundos virtuais, seja em aventuras imersivas ou RPGs.")
    st.warning("🔥 Destaques recentes: OMORI, Persona 5 e Genshin Impact.")
    if st.button("Clique para ver uma frase gamer 🎮"):
        frases = [
            # Mudar aqui
            "“It’s dangerous to go alone! Take this.” — The Legend of Zelda",
            "“The cake is a lie.” — Portal",
            "“A man chooses; a slave obeys.” — Bioshock",
            "“Would you kindly?” — Bioshock",
            "“War never changes.” — Fallout",
            "“Do a barrel roll!” — Star Fox 64",
            "“Stay awhile and listen.” — Diablo II",
            "“Hope is what makes us strong. It is why we are here…” — God of War 3",
            "“Don’t be sorry. Be better.” — God of War",
            "“I am the very model of a scientist Salarian.” — Mass Effect 2",
            "“I used to be an adventurer like you, then I took an arrow to the knee.” — Skyrim",
            "“The world could always use more heroes.” — Overwatch",
            "“A hero need not speak. When he is gone, the world will speak for him.” — Halo 3"
        ]

        st.caption(random.choice(frases))

with st.expander("🏎️ Fórmula 1"):
    st.write("A Fórmula 1 é mais do que um esporte: é estratégia, dados e emoção em alta velocidade.")
    st.info("⭐ Pilotos que admiro: Lewis Hamilton e Ayrton Senna")
    st.caption("‘No racing, no life.’")

st.divider()

# =====================
# CURIOSIDADES ALEATÓRIAS
# =====================
col1, col2 = st.columns(2)
with col1:

        st.markdown("<h2>🎲 Curiosidades Aleatórias</h2>", unsafe_allow_html=True)
        if st.button("Me surpreenda! ✨", use_container_width=True):
            curiosidades = [
                "Já assisti mais de 100 animes e ainda tenho lista pendente infinita 📺",
                "Sou capaz de maratonar uma série inteira em um único final de semana ☕",
                "Acredito que dados são como pneus na F1: escolha certa faz toda a diferença 🏎️",
                "Se pudesse, viajaria no tempo só para assistir corridas históricas dos anos 80 🕰️",
            ]
            st.success(random.choice(curiosidades))


# =====================
# CONTATO
# =====================
with col2:
    st.markdown(
        """
        <h2>📬 Contato</h2>
        <p>Adoro conversar sobre <b>dados, tecnologia, Fórmula 1 e cultura pop</b>.</p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<a href="https://www.linkedin.com/in/alice-santos-bulhões" target="_blank"><button style="background-color:#0A66C2; color:white; padding:10px; border:none; border-radius:8px; cursor:pointer;">🔗 LinkedIn</button></a>', unsafe_allow_html=True)

    with col2:
        st.markdown('<a href="https://github.com/AliceSBulhoes" target="_blank"><button style="background-color:#333; color:white; padding:10px; border:none; border-radius:8px; cursor:pointer;">💻 GitHub</button></a>', unsafe_allow_html=True)

    with col3:
        st.markdown('<a href="mailto:alice.s.bulhoes@gmail.com"><button style="background-color:#D44638; color:white; padding:10px; border:none; border-radius:8px; cursor:pointer;">📧 Email</button></a>', unsafe_allow_html=True)


