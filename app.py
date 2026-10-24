"""Res-Q · punto de entrada de la plataforma interactiva.

Ejecutar:  streamlit run app.py
"""
import streamlit as st

from src.ui import data, state, theme
from src.ui.components import navbar
from src.ui.views import landing, macro_peru, micro_piura, result

st.set_page_config(page_title="Res-Q | COER Piura", page_icon="🛰️", layout="wide")
theme.inyectar_css()
state.init()

red = data.cargar_red()
navbar.render(red)

VISTAS = {
    "landing": landing,
    "macro": macro_peru,
    "micro": micro_piura,
    "result": result,
}
VISTAS[st.session_state.vista].render(red)
