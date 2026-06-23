import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    '<h1 style="text-align:center; color:#000000; font-size:4rem; margin-top:0.5rem; margin-bottom:1rem;">LOD Rechner</h1>',
    unsafe_allow_html=True
)

# Placeholder für die Pride Message
pride_message_placeholder = st.empty()

st.markdown(
    '''
    <div id="typewriter" style="text-align:center; font-size:4rem; font-weight:bold; color:#000000; margin-bottom:0.8rem;"></div>
    <script>
    const typeText = "LOD Rechner";
    const typeEl = document.getElementById("typewriter");
    function startTyping() {
        typeEl.textContent = "";
        let i = 0;
        function typeNext() {
            if (i < typeText.length) {
                typeEl.textContent += typeText.charAt(i);
                i += 1;
                setTimeout(typeNext, 120);
            } else {
                setTimeout(startTyping, 1200);
            }
        }
        typeNext();
    }
    startTyping();
    </script>
    ''',
    unsafe_allow_html=True
)

# Custom CSS für die Terminals und globale Schrift
st.markdown("""
<style>
body, div, section, span, p, label, button, input, select, textarea, h1, h2, h3, h4, h5, h6 {
    font-family: 'Courier New', monospace !important;
}

#typewriter {
    font-family: 'Courier New', monospace !important;
}

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
st.markdown(
    '<div class="terminal-box terminal-pink"><div style="font-size:0.9rem; line-height:1.2;">Standartabweichung des Blindwerts bestimmen</div></div>',
    unsafe_allow_html=True
)

# Terminal 2 - Helllila
st.markdown(
    '<div class="terminal-box terminal-lilac"><div style="font-size:0.9rem; line-height:1.2;">Kalibriergerade bestimmen</div></div>',
    unsafe_allow_html=True
)

# Terminal 3 - Hellblau
st.markdown(
    '<div class="terminal-box terminal-blue"><div style="font-size:0.9rem; line-height:1.2;">LOD Berechnen</div></div>',
    unsafe_allow_html=True
)
