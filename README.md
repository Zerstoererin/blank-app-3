# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
### Notes about this fork

- UI title changed to "Nachweisgrenze-Berechner" and terminal boxes use monospace styling.
- Mathematical formulas (Standardabweichung, Kalibriergerade, LOD) are rendered with Streamlit's LaTeX support (`st.latex`).
- Sample data files: `sample_lod_data.csv`, `sample_lod_data.txt` (use the buttons in the app to load them).

### Tests

Run the unit tests with:

```
$ pytest -q
```
