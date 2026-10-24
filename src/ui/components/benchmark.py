import streamlit as st


def render(resultado: dict):
    b = resultado["benchmark"]
    c, q = b["clasico"], b["cuantico"]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="rq-card clasico">
              <h4>Algoritmo clásico</h4>
              <div class="rq-muted">{c['metodo']}</div>
              <div class="rq-kpi">{c['tiempo_s']} <small>s de cómputo</small></div>
              <p>Costo logístico: <b>{c['costo']}</b></p>
              <p class="rq-muted">El costo exacto crece de forma exponencial con el número de
              candidatos. Las heurísticas (Greedy / SA) pueden estancarse en mínimos locales.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="rq-card cuantico">
              <h4>Algoritmo variacional</h4>
              <div class="rq-muted">{q['metodo']}</div>
              <div class="rq-kpi">{q['tiempo_s']} <small>s de resolución</small></div>
              <p>Costo logístico: <b>{q['costo']}</b> · Energía de convergencia: <b>{q['energia']}</b></p>
              <p class="rq-muted">Job ID: {resultado['job_id']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
