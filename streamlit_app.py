from html import escape
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from lod_utils import calculate_lod, prepare_measurement_data

st.set_page_config(layout="wide")

st.markdown(
    '''<div style="text-align:center; margin-top:0.5rem; margin-bottom:1rem; font-size:4rem; color:#000000; font-weight:bold;">
        <span class="tooltip-container" style="margin-right:0.5rem;">★
            <span class="tooltip-text">Die Nachweisgrenze (englisch limit of detection, LOD) bezeichnet den extremen Wert eines Messverfahrens, bis zu dem die Messgröße gerade noch zuverlässig nachgewiesen werden kann.<br><a href="https://de.wikipedia.org/wiki/Nachweisgrenze" target="_blank" rel="noopener noreferrer" style="color:#fff; text-decoration:underline;">Quelle</a></span>
        </span>
        Nachweisgrenze-Berechner
        <span class="tooltip-container" style="margin-left:0.5rem;">★
            <span class="tooltip-text">Die Nachweisgrenze (englisch limit of detection, LOD) bezeichnet den extremen Wert eines Messverfahrens, bis zu dem die Messgröße gerade noch zuverlässig nachgewiesen werden kann.<br><a href="https://de.wikipedia.org/wiki/Nachweisgrenze" target="_blank" rel="noopener noreferrer" style="color:#fff; text-decoration:underline;">Quelle</a></span>
        </span>
    </div>''',
    unsafe_allow_html=True
)

st.markdown('## Daten hochladen', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

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

with col3:
    use_sample_csv = st.button('Beispiel-Daten laden (CSV)', use_container_width=True)
    use_sample_txt = st.button('Beispiel-Daten laden (TXT)', use_container_width=True)
    clear_results = st.button('Clear', use_container_width=True)


if clear_results:
    st.session_state.pop('last_result', None)
    st.session_state.pop('last_source', None)
    st.session_state.pop('last_preview', None)
    st.session_state.pop('last_lod_value', None)


def render_terminal_box(box_class, heading, result_text, formulas, latex=False, render_formula_as_image=False):
    def _latex_to_image(latex_str):
        try:
            import matplotlib.pyplot as plt
        except Exception:
            return None

        fig = plt.figure()
        # render mathtext (matplotlib's subset of LaTeX)
        fig.text(0.5, 0.5, f"${latex_str}$", ha='center', va='center', fontsize=20)
        plt.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)
        return buf

    if latex:
        st.markdown(
            f"""
            <div class='terminal-box {box_class}'>
                <div class='terminal-heading'>{escape(heading)}</div>
            """,
            unsafe_allow_html=True,
        )
        for formula in formulas:
            if render_formula_as_image:
                img = _latex_to_image(formula)
                if img is not None:
                    st.image(img)
                    continue
            try:
                st.latex(formula)
            except Exception:
                # fallback: show escaped text
                st.markdown(f"<div class='terminal-formula'>{escape(formula)}</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
                <div class='terminal-result-box'>{escape(result_text)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        formula_markup = "".join(
            f"<div class='terminal-formula'>{escape(formula)}</div>"
            for formula in formulas
        )
        st.markdown(
            f"""
            <div class='terminal-box {box_class}'>
                <div class='terminal-heading'>{escape(heading)}</div>
                {formula_markup}
                <div class='terminal-result-box'>{escape(result_text)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def process_data_frame(data_frame, source_name):
    if data_frame.empty:
        raise ValueError('Die Datei enthält keine Zeilen.')

    data_frame.columns = [col.strip().lower() for col in data_frame.columns]
    expected_columns = {'measurement_type', 'concentration', 'signal'}
    missing_columns = expected_columns.difference(data_frame.columns)
    if missing_columns:
        raise ValueError(f'Fehlende Spalten: {sorted(missing_columns)}')

    data_frame['measurement_type'] = data_frame['measurement_type'].astype(str).str.strip().str.lower()
    data_frame['concentration'] = pd.to_numeric(data_frame['concentration'], errors='coerce')
    data_frame['signal'] = pd.to_numeric(data_frame['signal'], errors='coerce')
    data_frame = data_frame.dropna(subset=['measurement_type', 'signal'])

    records = data_frame.to_dict(orient='records')
    blank_signals, calibration = prepare_measurement_data(records)
    lod_value = calculate_lod(blank_signals, calibration)

    blank_mean = sum(blank_signals) / len(blank_signals)
    blank_sd = pd.Series(blank_signals).std(ddof=1) if len(blank_signals) > 1 else 0.0

    x_values = [x for x, _ in calibration]
    y_values = [y for _, y in calibration]
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in calibration)
    denominator = sum((x - x_mean) ** 2 for x, _ in calibration)
    slope = numerator / denominator if denominator else 0.0

    terminal1_content = (
        f"{source_name}: Blindwerte: {len(blank_signals)} · Mittelwert: {blank_mean:.4f} · "
        f"Standardabweichung: {blank_sd:.4f}"
    )
    terminal2_content = (
        f"{source_name}: Kalibrierpunkte: {len(calibration)} · Steigung m: {slope:.4f}"
    )
    terminal3_content = f"{source_name}: LOD: {lod_value:.6f}"

    return data_frame, terminal1_content, terminal2_content, terminal3_content, lod_value


if use_sample_csv:
    sample_path = Path(__file__).with_name('sample_lod_data.csv')
    sample_bytes = sample_path.read_bytes()
    data_frame = pd.read_csv(BytesIO(sample_bytes))
    data_frame, terminal1_content, terminal2_content, terminal3_content, lod_value = process_data_frame(data_frame, sample_path.name)
    st.success(f'✓ Beispiel-Datei geladen: {sample_path.name}')
    st.subheader('Vorschau der eingelesenen Daten')
    st.dataframe(data_frame, use_container_width=True)
    st.caption('Erkannte Blindwerte und Kalibrierpunkte werden aus den Spalten measurement_type, concentration und signal berechnet.')
    st.session_state.last_result = data_frame
    st.session_state.last_source = sample_path.name
    st.session_state.last_preview = data_frame.copy()
    st.session_state.last_lod_value = lod_value
elif use_sample_txt:
    sample_path = Path(__file__).with_name('sample_lod_data.txt')
    sample_bytes = sample_path.read_bytes()
    data_frame = pd.read_csv(BytesIO(sample_bytes), sep='\t')
    data_frame, terminal1_content, terminal2_content, terminal3_content, lod_value = process_data_frame(data_frame, sample_path.name)
    st.success(f'✓ Beispiel-Datei geladen: {sample_path.name}')
    st.subheader('Vorschau der eingelesenen Daten')
    st.dataframe(data_frame, use_container_width=True)
    st.caption('Erkannte Blindwerte und Kalibrierpunkte werden aus den Spalten measurement_type, concentration und signal berechnet.')
    st.session_state.last_result = data_frame
    st.session_state.last_source = sample_path.name
    st.session_state.last_preview = data_frame.copy()
    st.session_state.last_lod_value = lod_value
elif uploaded_file is not None:
    st.success(f'✓ {uploaded_file.name} ({file_type})')

    try:
        if file_type == 'CSV':
            data_frame = pd.read_csv(uploaded_file)
        elif file_type == 'XLSX':
            data_frame = pd.read_excel(uploaded_file)
        else:
            data_frame = pd.read_csv(uploaded_file, sep='\t')

        data_frame, terminal1_content, terminal2_content, terminal3_content, lod_value = process_data_frame(data_frame, uploaded_file.name)

        st.subheader('Vorschau der eingelesenen Daten')
        st.dataframe(data_frame, use_container_width=True)
        st.caption('Erkannte Blindwerte und Kalibrierpunkte werden aus den Spalten measurement_type, concentration und signal berechnet.')
        st.session_state.last_result = data_frame
        st.session_state.last_source = uploaded_file.name
        st.session_state.last_preview = data_frame.copy()
        st.session_state.last_lod_value = lod_value
    except Exception as exc:
        st.error(f'Fehler beim Einlesen der Datei: {exc}')
        terminal1_content = 'Fehler: Bitte prüfen Sie das Format.'
        terminal2_content = 'Fehler: Bitte prüfen Sie das Format.'
        terminal3_content = 'Fehler: Bitte prüfen Sie das Format.'
        lod_value = None
else:
    st.info('Bitte eine Datei hochladen oder einen der Beispiel-Buttons nutzen, damit die drei Berechnungsschritte in den Terminalfeldern ausgeführt werden können.')
    terminal1_content = 'Zwischenergebnis: keine Daten geladen.'
    terminal2_content = 'Zwischenergebnis: keine Daten geladen.'
    terminal3_content = 'Zwischenergebnis: keine Daten geladen.'
    lod_value = st.session_state.get('last_lod_value')

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
    background-color: #f0f0f0; /* Light gray */
    border: 2px solid #a0a0a0; /* Gray */
    color: #333;
}

.terminal-lilac {
    background-color: #e0e0e0; /* Slightly darker light gray */
    border: 2px solid #909090; /* Darker gray */
    color: #333;
}

.terminal-blue {
    background-color: #d0d0d0; /* Even darker light gray */
    border: 2px solid #808080; /* Dark gray */
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
    margin-top: 0.2rem;
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

.lod-display {
    background-color: #f8f8f8; /* Very light gray */
    border: 2px solid #cccccc; /* Light gray */
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-top: 1.5rem;
    text-align: center;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.lod-display-title {
    font-size: 1.4rem;
    font-weight: bold;
    margin-bottom: 0.75rem;
    color: #333;
}

.lod-display-value {
    font-size: 2.6rem;
    font-weight: bold;
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

render_terminal_box(
    'terminal-pink',
    'Standardabweichung des Blindwerts bestimmen',
    terminal1_content,
    [r'''s_{blank} = \sqrt{\frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n - 1}}'''],
    latex=True,
    render_formula_as_image=True,
)

render_terminal_box(
    'terminal-lilac',
    'Kalibriergerade bestimmen',
    terminal2_content,
    [
        r'''
        m =
        \frac{
        n\sum_{i=1}^{n} x_i y_i
        -
        \sum_{i=1}^{n} x_i \sum_{i=1}^{n} y_i
        }{
        n\sum_{i=1}^{n} x_i^2
        -
        \left(\sum_{i=1}^{n} x_i\right)^2
        }
        ''',
        r'''c = \bar{y} - m\bar{x}'''
    ],
    latex=True,
)

render_terminal_box(
    'terminal-blue',
    'LOD Berechnen',
    terminal3_content,
    [r'''LOD = 3.3 \frac{s_{blank}}{m}'''],
    latex=True,
)

lod_display_value = f"{lod_value:.6f}" if lod_value is not None else '—'
st.markdown(
    f"""
    <div class='lod-display'>
        <div class='lod-display-title'>Der LOD beträgt:</div>
        <div class='lod-display-value'>{lod_display_value}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
