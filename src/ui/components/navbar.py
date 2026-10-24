import streamlit as st


def render(red: dict):
    ss = st.session_state
    res = ss.get("resultado")
    job = res["job_id"] if res else "—"
    es_mock = res["es_mock"] if res else red.get("es_mock", False)
    demo = '<span class="rq-pill warn">DATOS DE DEMOSTRACIÓN</span>' if es_mock else ""
    st.markdown(
        f"""
        <div class="rq-nav">
          <div>
            <span class="rq-brand">Res<span>-Q</span></span>
            <span class="rq-sub">COER Piura · Soporte a decisiones logísticas</span>
          </div>
          <div>
            {demo}
            <span class="rq-pill ok">● Servicio disponible</span>
            <span class="rq-pill">Job ID: {job}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
