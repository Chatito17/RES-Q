import streamlit as st
from streamlit_folium import st_folium

from src.ui import state
from src.ui.components import map_view


def _entrar_a_piura():
    st.session_state.region = "piura"
    st.session_state.fly_pending = True
    state.ir_a("micro")


def render(red: dict):
    st.markdown("## Alcance nacional")
    st.caption("Seleccione la región de estudio. Por ahora solo Piura está habilitada.")

    col_mapa, col_info = st.columns([3, 1])
    with col_mapa:
        salida = st_folium(
            map_view.mapa_peru(red),
            height=520,
            use_container_width=True,
            returned_objects=["last_object_clicked_tooltip"],
            key="mapa_peru",
        )
    with col_info:
        st.markdown(
            """
            <div class="rq-card">
              <h4>Región piloto</h4>
              <p><b>Piura</b></p>
              <p class="rq-muted">Escenarios: Alto Piura, Bajo Piura y quebradas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Enfocar Piura", key="btn_piura", type="primary"):
            _entrar_a_piura()

    click = (salida or {}).get("last_object_clicked_tooltip")
    if click and click.strip().lower() == "piura":
        _entrar_a_piura()
