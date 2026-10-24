"""Tema Dark Executive / Quantum Tech de Res-Q."""
import streamlit as st

FONDO = "#0D0E15"
SUPERFICIE = "#161824"
ACENTO = "#8A3FFC"
GANADOR = "#00FF66"
OFERTA = "#00E5FF"
DEMANDA = "#FF4D4D"
TEXTO = "#E6E8F0"
TEXTO_SUAVE = "#9AA0B4"

CSS = f"""
<style>
.stApp {{ background: {FONDO}; }}
[data-testid="stSidebar"] {{ background: {SUPERFICIE}; border-right: 1px solid #23263A; }}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 1.2rem; }}

.stButton > button {{
    width: 100%;
    background: {ACENTO};
    color: white;
    border: 0;
    border-radius: 10px;
    padding: .6rem 1rem;
    font-weight: 600;
}}
.stButton > button:hover {{ background: #9d5cff; color: white; }}
.stButton > button:disabled {{ background: #2A2D44; color: #6B7090; }}

.rq-nav {{
    display: flex; align-items: center; justify-content: space-between;
    background: {SUPERFICIE}; border: 1px solid #23263A; border-radius: 14px;
    padding: .7rem 1.1rem; margin-bottom: 1rem;
}}
.rq-brand {{ font-size: 1.35rem; font-weight: 800; letter-spacing: .5px; color: {TEXTO}; }}
.rq-brand span {{ color: {ACENTO}; }}
.rq-sub {{ color: {TEXTO_SUAVE}; font-size: .85rem; margin-left: .8rem; }}
.rq-pill {{
    display: inline-block; padding: .2rem .65rem; border-radius: 999px;
    font-size: .75rem; font-weight: 600; margin-left: .4rem;
    border: 1px solid #2E3250; color: {TEXTO_SUAVE};
}}
.rq-pill.ok {{ color: {GANADOR}; border-color: #0B5A2E; }}
.rq-pill.warn {{ color: #FFB020; border-color: #6B4A08; }}

.rq-card {{
    background: {SUPERFICIE}; border: 1px solid #23263A; border-radius: 14px;
    padding: 1.1rem 1.2rem; height: 100%;
}}
.rq-card h4 {{ margin: 0 0 .5rem 0; color: {TEXTO}; }}
.rq-kpi {{ font-size: 1.8rem; font-weight: 800; color: {TEXTO}; }}
.rq-kpi small {{ font-size: .8rem; font-weight: 500; color: {TEXTO_SUAVE}; }}
.rq-muted {{ color: {TEXTO_SUAVE}; font-size: .85rem; }}
.rq-card.clasico {{ border-top: 3px solid #FFB020; }}
.rq-card.cuantico {{ border-top: 3px solid {ACENTO}; }}
.rq-card.ganador {{ border: 1px solid {GANADOR}; box-shadow: 0 0 18px rgba(0,255,102,.18); }}

.rq-hero {{
    background: linear-gradient(135deg, #161824 0%, #1E1540 100%);
    border: 1px solid #2B2350; border-radius: 18px; padding: 2.2rem 2rem; margin-bottom: 1rem;
}}
.rq-hero h1 {{ font-size: 2.6rem; margin: 0; color: {TEXTO}; }}
.rq-hero h1 span {{ color: {ACENTO}; }}
.rq-leyenda span {{ margin-right: 1.1rem; font-size: .85rem; color: {TEXTO_SUAVE}; }}
.rq-dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:.35rem; }}
</style>
"""


def inyectar_css():
    st.markdown(CSS, unsafe_allow_html=True)
