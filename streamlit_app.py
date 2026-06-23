import streamlit as st

st.set_page_config(layout="wide")

# Pride Button in der Session State initialisieren
if "show_pride_message" not in st.session_state:
    st.session_state.show_pride_message = False

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

# Custom CSS für die Terminals und Pride Button
st.markdown("""
<style>
body, div, section, span, p, label, button, input, select, textarea, h1, h2, h3, h4, h5, h6 {
    font-family: 'Courier New', monospace !important;
}

#typewriter {
    font-family: 'Courier New', monospace !important;
}

.pride-button-container {
    position: fixed;
    top: 100px;
    right: 20px;
    z-index: 999;
}

.pride-button {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    background: linear-gradient(to bottom, 
        #FF0000 0%, 
        #FF7F00 16.66%, 
        #FFFF00 33.33%, 
        #00FF00 50%, 
        #0000FF 66.66%, 
        #4B0082 83.33%, 
        #9400D3 100%);
    cursor: pointer;
    font-size: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: transform 0.2s;
}

.pride-button:hover {
    transform: scale(1.1);
}

.pride-button:active {
    transform: scale(0.95);
}

.pride-message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(0,0,0,0.9);
    color: white;
    padding: 30px 60px;
    border-radius: 20px;
    font-size: 36px;
    font-weight: bold;
    z-index: 1000;
    animation: fadeInOut 2s ease-in-out;
    width: 100%;
    text-align: center;
    pointer-events: none;
}

@keyframes fadeInOut {
    0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
    10% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    90% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
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

# Pride Button HTML mit JavaScript
st.markdown("""
<div class="pride-button-container">
    <button class="pride-button" onclick="showPrideMessage()">🏳️‍🌈</button>
</div>

<script>
function showPrideMessage() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'pride-message';
    msgDiv.textContent = 'Happy Pride';
    
    // Zur Hauptseite hinzufügen
    const mainContent = document.querySelector('[data-testid="stMainBlockContainer"]');
    if (mainContent) {
        mainContent.appendChild(msgDiv);
    } else {
        document.body.appendChild(msgDiv);
    }
    
    setTimeout(() => {
        msgDiv.remove();
    }, 2000);
}
</script>
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
