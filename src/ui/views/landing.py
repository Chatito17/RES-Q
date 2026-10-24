import streamlit as st

from src.ui import state


def render(red: dict):
    p = red["proyecto"]
    st.markdown(
        f"""
        <div class="rq-hero">
          <h1>Res<span>-Q</span></h1>
          <p style="font-size:1.15rem">{p['subtitulo']}</p>
          <p class="rq-muted">{p['descripcion']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(
            f"""
            <div class="rq-card">
              <h4>Ficha del proyecto</h4>
              <p><b>Cliente simulado:</b> {p['cliente']}</p>
              <p><b>Integrantes:</b> {' · '.join(p['equipo'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.write("")
        if st.button("Ingresar a la plataforma", key="btn_ingresar", type="primary"):
            state.ir_a("macro")
