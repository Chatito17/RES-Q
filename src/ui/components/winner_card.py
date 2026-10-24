import streamlit as st


def render(resultado: dict):
    ganador = next(n for n in resultado["nodos_oferta"] if n["estado"] == "ganador")
    cobertura = ", ".join(ganador["cobertura"]) or "—"
    ruta = (
        "Acceso vial resiliente habilitado"
        if ganador["ruta_resiliente"]
        else "Acceso parcialmente interrumpido: usar rutas alternas"
    )
    with st.expander("Punto elegido · Selección óptima", expanded=True):
        st.markdown(
            f"""
            <div class="rq-card ganador">
              <div class="rq-muted">NODO HABILITADO</div>
              <h4 style="color:#00FF66">{ganador['nombre']}</h4>
              <p><b>Capacidad asignada:</b> {ganador['capacidad_t']} toneladas de ayuda humanitaria</p>
              <p><b>Cobertura directa:</b> {cobertura}</p>
              <p><b>Condición de ruta:</b> {ruta}</p>
              <p class="rq-muted">Cobertura total de la red: {resultado['cobertura_pct']} % de la población
              en ≤ {resultado['tmax_h']} h con {resultado['p']} centro(s).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
