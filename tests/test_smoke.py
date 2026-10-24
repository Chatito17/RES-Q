"""Prueba de humo: recorre las 4 vistas con AppTest (sin navegador)."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def _app():
    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    assert not at.exception, at.exception
    return at


def test_flujo_completo():
    at = _app()
    assert at.session_state.vista == "landing"

    at.button(key="btn_ingresar").click().run()
    assert not at.exception
    assert at.session_state.vista == "macro"

    at.button(key="btn_piura").click().run()
    assert not at.exception
    assert at.session_state.vista == "micro"

    resolver = next(b for b in at.sidebar.button if "Resolver" in b.label)
    resolver.click().run()
    assert not at.exception
    assert at.session_state.vista == "result"
    res = at.session_state.resultado
    assert res["p"] == 2
    assert sum(n["estado"] == "ganador" for n in res["nodos_oferta"]) == 1
    assert 0 <= res["cobertura_pct"] <= 100


def test_contrato_resultado_por_escenario():
    from src.ui import data

    red = data.cargar_red.__wrapped__()
    for esc in red["escenarios"]:
        for p in (1, 2, 3, 4):
            for t in (24, 48, 72):
                r = data._resolver_mock(red, esc, p, t)
                activos = [n for n in r["nodos_oferta"] if n["estado"] in ("ganador", "activo")]
                assert len(activos) == p
                assert {"clasico", "cuantico"} <= set(r["benchmark"])
