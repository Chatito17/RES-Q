"""Máquina de estados determinista: landing -> macro -> micro -> result."""
import time

import streamlit as st

from src.ui import data

DEFAULTS = {
    "vista": "landing",
    "region": None,
    "escenario": "alto_piura",
    "p": 2,
    "tmax": 72,
    "resolviendo": False,
    "resultado": None,
    "fly_pending": False,
}


def init():
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)


def ir_a(vista: str):
    st.session_state.vista = vista
    st.rerun()


def solicitar_resolucion():
    st.session_state.resolviendo = True
    st.rerun()


def resolver_si_pendiente():
    """Estado de carga global: se ejecuta con el sidebar ya bloqueado."""
    ss = st.session_state
    if not ss.resolviendo:
        return
    with st.status("Resolviendo red logística…", expanded=True) as estado:
        st.write("Construyendo modelo de optimización (QUBO)…")
        time.sleep(0.5)
        st.write("Ejecutando solver clásico y algoritmo variacional…")
        time.sleep(0.8)
        ss.resultado = data.resolver(ss.escenario, ss.p, ss.tmax)
        estado.update(label="Resolución completada", state="complete")
    ss.resolviendo = False
    ss.vista = "result"
    st.rerun()
