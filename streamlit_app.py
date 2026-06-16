import streamlit as st

st.set_page_config(layout="wide")

st.title("Nachweisgrenze Berechnung")

# Custom CSS für die Terminals
st.markdown("""
<style>
.terminal-box {
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 1cm;
    min-height: 150px;
    font-family: 'Courier New', monospace;
}

.terminal-pink {
    background-color: #FFB6D9;
    border: 2px solid #FF69B4;
    color: #333;
}

.terminal-lilac {
    background-color: #E6D7F0;
    border: 2px solid #DA70D6;
    color: #333;
}

.terminal-blue {
    background-color: #B3D9FF;
    border: 2px solid #4DA6FF;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# Terminal 1 - Hellpink
st.markdown('<h3 style="margin-top: 0;">Standartabweichung des Blindwerts bestimmen</h3>', unsafe_allow_html=True)
st.markdown(
    '<div class="terminal-box terminal-pink"></div>',
    unsafe_allow_html=True
)

# Terminal 2 - Helllila
st.markdown(
    '<div class="terminal-box terminal-lilac">Formel 2: Bestimmungsgrenze</div>',
    unsafe_allow_html=True
)

# Terminal 3 - Hellblau
st.markdown(
    '<div class="terminal-box terminal-blue">Formel 3: Messgenauigkeit</div>',
    unsafe_allow_html=True
)
