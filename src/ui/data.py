"""Capa de datos de la UI.

La UI NO importa Qiskit ni llama a IBM. Solo consume un contrato JSON.

- Backend real: escribe un archivo por combinación en el directorio indicado por
  la variable de entorno RESQ_RESULTS_DIR, con nombre ``{escenario}_p{p}_t{tmax}.json``
  (ej. ``alto_piura_p2_t72.json``) respetando el contrato de ``_resolver_mock``.
- Sin backend: se genera un resultado de DEMOSTRACIÓN (``es_mock = true``).
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[2]
RUTA_RED = RAIZ / "data" / "mock_network.json"

FACTOR_VIA = 1.35   # distancia por carretera ≈ 1.35 × línea recta
H_POR_KM = 0.6      # horas logísticas por km con acceso degradado (supuesto de demo)


@st.cache_data
def cargar_red() -> dict:
    return json.loads(RUTA_RED.read_text(encoding="utf-8"))


def _km(a: dict, b: dict) -> float:
    r = 6371.0
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dphi = p2 - p1
    dl = math.radians(b["lon"] - a["lon"])
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h)) * FACTOR_VIA


def resolver(escenario_id: str, p: int, tmax_h: int) -> dict:
    """Devuelve el resultado del backend si existe; si no, un resultado de demo."""
    carpeta = os.environ.get("RESQ_RESULTS_DIR")
    if carpeta:
        ruta = Path(carpeta) / f"{escenario_id}_p{p}_t{tmax_h}.json"
        if ruta.exists():
            return json.loads(ruta.read_text(encoding="utf-8"))
    return _resolver_mock(cargar_red(), escenario_id, p, tmax_h)


def _resolver_mock(red: dict, escenario_id: str, p: int, tmax_h: int) -> dict:
    esc = red["escenarios"][escenario_id]
    oferta = {n["id"]: n for n in red["nodos_oferta"]}
    cortados = {tuple(a) for a in esc["arcos_interrumpidos"]}
    elegidos = esc["ranking_oferta"][:p]

    demanda_out, pob_asignada, cubiertos_por = [], {o: 0 for o in elegidos}, {o: [] for o in elegidos}
    arcos_activos = set()
    costo, pob_total, pob_cubierta = 0.0, 0, 0

    for d in red["nodos_demanda"]:
        pob_total += d["poblacion"]
        mejor = None
        for o_id, d_id in red["arcos"]:
            if d_id != d["id"] or o_id not in elegidos or (o_id, d_id) in cortados:
                continue
            horas = _km(oferta[o_id], d) * H_POR_KM
            if mejor is None or horas < mejor[1]:
                mejor = (o_id, horas)
        if mejor and mejor[1] <= tmax_h:
            o_id, horas = mejor
            pob_cubierta += d["poblacion"]
            pob_asignada[o_id] += d["poblacion"]
            cubiertos_por[o_id].append(d["nombre"])
            arcos_activos.add((o_id, d["id"]))
            costo += d["poblacion"] * horas / 1000
            demanda_out.append({**d, "asignado_a": o_id, "tiempo_h": round(horas, 1)})
        else:
            costo += d["poblacion"] * 0.05
            demanda_out.append({**d, "asignado_a": None, "tiempo_h": None})

    ganador = max(elegidos, key=lambda o: pob_asignada[o])
    oferta_out = []
    for n in red["nodos_oferta"]:
        estado = "candidato"
        if n["id"] in elegidos:
            estado = "ganador" if n["id"] == ganador else "activo"
        oferta_out.append({
            **n,
            "estado": estado,
            "poblacion_asignada": pob_asignada.get(n["id"], 0),
            "cobertura": cubiertos_por.get(n["id"], []),
            "ruta_resiliente": not any(o == n["id"] for o, _ in cortados),
        })

    arcos = [
        {"origen": o, "destino": d, "interrumpido": (o, d) in cortados, "activo": (o, d) in arcos_activos}
        for o, d in red["arcos"]
    ]
    costo = round(costo, 1)
    return {
        "es_mock": True,
        "job_id": f"mock-{escenario_id}-p{p}-t{tmax_h}",
        "escenario_id": escenario_id,
        "escenario_nombre": esc["nombre"],
        "p": p,
        "tmax_h": tmax_h,
        "cobertura_pct": round(100 * pob_cubierta / pob_total, 1),
        "nodos_oferta": oferta_out,
        "nodos_demanda": demanda_out,
        "arcos": arcos,
        "benchmark": {
            "clasico": {"metodo": "ILP / Branch & Bound", "tiempo_s": round(0.4 * 1.8 ** p, 2), "costo": costo},
            "cuantico": {
                "metodo": "QAOA (simulador Aer)",
                "tiempo_s": round(3.1 + 1.2 * p, 2),
                "costo": round(costo * (1 + 0.02 * p), 1),
                "energia": round(-costo / 10, 3),
            },
        },
    }
