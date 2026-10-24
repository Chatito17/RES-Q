import streamlit as st
from streamlit_folium import st_folium

from src.ui import state, theme
from src.ui.components import map_view, sidebar


def render(red: dict):
    ss = st.session_state
    sidebar.render(red)

    esc = red["escenarios"][ss.escenario]
    st.markdown(f"## Piura · {esc['nombre']}")
    st.markdown(
        f"""
        <div class="rq-leyenda">
          <span><i class="rq-dot" style="background:{theme.OFERTA}"></i>Almacén candidato</span>
          <span><i class="rq-dot" style="background:{theme.DEMANDA}"></i>Distrito afectado</span>
          <span><i class="rq-dot" style="background:{theme.DEMANDA}"></i>- - - Vía interrumpida</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    volar = ss.fly_pending
    ss.fly_pending = False
    st_folium(
        map_view.mapa_piura(red, resultado=None, volar=volar),
        height=560,
        use_container_width=True,
        returned_objects=[],
        key=f"mapa_micro_{ss.escenario}",
    )
    st.caption("Ajuste los parámetros del panel lateral y pulse «Resolver red logística».")

    state.resolver_si_pendiente()
