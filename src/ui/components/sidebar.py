import streamlit as st

from src.ui import state


def render(red: dict):
    """Panel lateral con los 3 controles de la especificación. Devuelve nada;
    si se pulsa 'Resolver' dispara la resolución (con el panel bloqueado)."""
    ss = st.session_state
    bloqueado = ss.resolviendo
    ids = list(red["escenarios"])

    with st.sidebar:
        st.markdown("### Parámetros")
        ss.escenario = st.selectbox(
            "Escenario hidrológico",
            ids,
            index=ids.index(ss.escenario),
            format_func=lambda i: red["escenarios"][i]["nombre"],
            disabled=bloqueado,
        )
        ss.p = st.slider(
            "Límite de almacenes (p-centros)", 1, 4, int(ss.p), disabled=bloqueado
        )
        ss.tmax = st.radio(
            "Ventana crítica de respuesta (Tmax)",
            [24, 48, 72],
            index=[24, 48, 72].index(ss.tmax),
            format_func=lambda h: f"{h} h",
            horizontal=True,
            disabled=bloqueado,
        )
        st.divider()
        if bloqueado:
            st.button("Procesando…", disabled=True)
        elif st.button("Resolver red logística", type="primary"):
            state.solicitar_resolucion()
