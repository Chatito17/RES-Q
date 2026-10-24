import streamlit as st
from streamlit_folium import st_folium

from src.ui import state
from src.ui.components import benchmark, map_view, sidebar, winner_card


def render(red: dict):
    ss = st.session_state
    if ss.resultado is None:
        state.ir_a("micro")
        return

    sidebar.render(red)
    res = ss.resultado

    st.markdown(f"## Resultado · {res['escenario_nombre']}")
    col_mapa, col_ficha = st.columns([2, 1])
    with col_mapa:
        st_folium(
            map_view.mapa_piura(red, resultado=res),
            height=540,
            use_container_width=True,
            returned_objects=[],
            key=f"mapa_res_{res['job_id']}",
        )
    with col_ficha:
        winner_card.render(res)

    st.markdown("### Benchmark comparativo")
    benchmark.render(res)

    if st.button("Volver al escenario", key="btn_volver"):
        state.ir_a("micro")

    state.resolver_si_pendiente()
