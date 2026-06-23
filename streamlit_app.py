import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    '''<div style="text-align:center; margin-top:0.5rem; margin-bottom:1rem; font-size:4rem; color:#000000; font-weight:bold;">
        <span class="tooltip-container" style="margin-right:0.5rem;">★
            <span class="tooltip-text">Die Nachweisgrenze (englisch limit of detection, LOD) bezeichnet den extremen Wert eines Messverfahrens, bis zu dem die Messgröße gerade noch zuverlässig nachgewiesen werden kann.<br><a href="https://de.wikipedia.org/wiki/Nachweisgrenze" target="_blank" rel="noopener noreferrer" style="color:#fff; text-decoration:underline;">Quelle</a></span>
        </span>
        LOD Rechner
        <span class="tooltip-container" style="margin-left:0.5rem;">★
            <span class="tooltip-text">Die Nachweisgrenze (englisch limit of detection, LOD) bezeichnet den extremen Wert eines Messverfahrens, bis zu dem die Messgröße gerade noch zuverlässig nachgewiesen werden kann.<br><a href="https://de.wikipedia.org/wiki/Nachweisgrenze" target="_blank" rel="noopener noreferrer" style="color:#fff; text-decoration:underline;">Quelle</a></span>
        </span>
    </div>''',
    unsafe_allow_html=True
)

st.markdown('## Daten hochladen', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    file_type = st.selectbox(
        'Dateityp wählen',
        ['CSV', 'XLSX', 'TXT']
    )

with col2:
    uploaded_file = st.file_uploader(
        'Datei hochladen',
        type=['csv', 'xlsx', 'txt']
    )

if uploaded_file is not None:
    st.success(f'✓ {uploaded_file.name} ({file_type})')
    terminal1_content = (
        '<div class="terminal-heading">Standartabweichung des Blindwerts bestimmen</div>'
        '<div class="terminal-formula">$$s_{blank} = \sqrt{\frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n - 1}}$$</div>'
        '<div class="terminal-result-box">Zwischenergebnis: s_{blank} wird aus den Blindwertdaten berechnet.</div>'
    )
    terminal2_content = (
        '<div class="terminal-heading">Kalibriergerade bestimmen</div>'
        '<div class="terminal-formula">$$m = \frac{n\sum_{i=1}^{n} x_i y_i - \sum_{i=1}^{n} x_i \sum_{i=1}^{n} y_i}{n\sum_{i=1}^{n} x_i^2 - (\sum_{i=1}^{n} x_i)^2}\\[6pt]c = \bar{y} - m\bar{x}$$</div>'
        '<div class="terminal-result-box">Zwischenergebnis: Steigung m und Achsenabschnitt c werden ermittelt.</div>'
    )
    terminal3_content = (
        '<div class="terminal-heading">LOD Berechnen</div>'
        '<div class="terminal-formula">$$LOD = 3.3 \frac{s_{blank}}{m}$$</div>'
        '<div class="terminal-result-box">Zwischenergebnis: LOD wird aus s_{blank} und m berechnet.</div>'
    )
else:
    st.info('Bitte eine Datei hochladen, damit die drei Berechnungsschritte in den Terminalfeldern ausgeführt werden können.')
    terminal1_content = (
        '<div class="terminal-heading">Standartabweichung des Blindwerts bestimmen</div>'
        '<div class="terminal-formula">$$s_{blank} = \sqrt{\frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n - 1}}$$</div>'
        '<div class="terminal-result-box">Zwischenergebnis: keine Daten geladen.</div>'
    )
    terminal2_content = (
        '<div class="terminal-heading">Kalibriergerade bestimmen</div>'
        '<div class="terminal-formula">$$m = \frac{n\sum_{i=1}^{n} x_i y_i - \sum_{i=1}^{n} x_i \sum_{i=1}^{n} y_i}{n\sum_{i=1}^{n} x_i^2 - (\sum_{i=1}^{n} x_i)^2}\\[6pt]c = \bar{y} - m\bar{x}$$</div>'
        '<div class="terminal-result-box">Zwischenergebnis: keine Daten geladen.</div>'
    )
    terminal3_content = (
        '<div class="terminal-heading">LOD Berechnen</div>'
        '<div class="terminal-formula">$$LOD = 3.3 \frac{s_{blank}}{m}$$</div>'
        '<div class="terminal-result-box">Zwischenergebnis: keine Daten geladen.</div>'
    )

# Placeholder für die Pride Message
pride_message_placeholder = st.empty()

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

.tooltip-container {
    position: relative;
    display: inline-block;
    cursor: help;
}

.tooltip-text {
    visibility: hidden;
    background-color: #333;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 12px 15px;
    position: absolute;
    z-index: 1;
    top: 125%;
    left: 50%;
    transform: translateX(-50%);
    width: 250px;
    font-size: 1rem;
    line-height: 1.4;
    white-space: normal;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.tooltip-text::after {
    content: "";
    position: absolute;
    bottom: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: transparent transparent #333 transparent;
}

.tooltip-container:hover .tooltip-text {
    visibility: visible;
}

.terminal-heading {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 0.35rem;
}

.terminal-formula {
    font-size: 1.1rem;
    color: #222;
    line-height: 1.5;
    white-space: normal;
    margin-bottom: 0.75rem;
}

.terminal-result-box {
    background-color: rgba(255,255,255,0.85);
    border: 1px solid rgba(0,0,0,0.12);
    border-radius: 6px;
    padding: 10px 12px;
    margin-top: 10px;
    font-size: 0.95rem;
    color: #111;
}

/* Button-Text für file_uploader */
button[data-testid="baseButton-secondary"] {
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

# CSS für Button-Text-Anpassung (Alternative mit JavaScript)
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
        if (btn.textContent.includes('Browse files')) {
            btn.textContent = 'Data';
        }
    });
});
</script>
""", unsafe_allow_html=True)

# Terminal 1 - Hellpink
st.markdown(
    f'<div class="terminal-box terminal-pink"><div style="font-size:0.9rem; line-height:1.2;">{terminal1_content}</div></div>',
    unsafe_allow_html=True
)

# Terminal 2 - Helllila
st.markdown(
    f'<div class="terminal-box terminal-lilac"><div style="font-size:0.9rem; line-height:1.2;">{terminal2_content}</div></div>',
    unsafe_allow_html=True
)

# Terminal 3 - Hellblau
st.markdown(
    f'<div class="terminal-box terminal-blue"><div style="font-size:0.9rem; line-height:1.2;">{terminal3_content}</div></div>',
    unsafe_allow_html=True
)
