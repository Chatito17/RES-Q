"""Mapas Folium: vista macro (Perú), micro (Piura) y resultado."""
import folium
from branca.element import MacroElement
from jinja2 import Template

from src.ui import theme

# OpenStreetMap no requiere API key; el filtro CSS invierte los tiles para el tema oscuro.
# (Los tiles públicos de OSM son para demos; en producción usar un proveedor propio.)
TILES = "OpenStreetMap"
ESTILO_OSCURO = (
    "<style>.leaflet-tile-pane{filter:invert(1) hue-rotate(180deg) brightness(.85) contrast(.9) saturate(.6);}"
    ".leaflet-container{background:#0D0E15;}</style>"
)


def _oscurecer(m: folium.Map) -> folium.Map:
    m.get_root().header.add_child(folium.Element(ESTILO_OSCURO))
    return m


class VolarA(MacroElement):
    """Animación Leaflet flyTo (acercamiento fluido de Perú a Piura)."""

    _template = Template(
        """{% macro script(this, kwargs) %}
        {{ this._parent.get_name() }}.flyTo([{{ this.lat }}, {{ this.lon }}], {{ this.zoom }},
            {duration: 2.6});
        {% endmacro %}"""
    )

    def __init__(self, lat, lon, zoom):
        super().__init__()
        self._name = "VolarA"
        self.lat, self.lon, self.zoom = lat, lon, zoom


def mapa_peru(red: dict) -> folium.Map:
    m = _oscurecer(folium.Map(location=[-9.2, -75.0], zoom_start=5, tiles=TILES, control_scale=True))
    for r in red["regiones"]:
        color = theme.ACENTO if r["disponible"] else "#4A4E69"
        folium.CircleMarker(
            [r["lat"], r["lon"]],
            radius=11 if r["disponible"] else 7,
            color=color, fill=True, fill_color=color, fill_opacity=0.85,
            tooltip=r["nombre"] + ("" if r["disponible"] else " (no disponible)"),
        ).add_to(m)
    return m


def _halo(lat, lon, nombre):
    html = f"""
    <style>
      @keyframes rqpulse {{ 0% {{ transform: scale(.6); opacity:.9 }} 100% {{ transform: scale(2.6); opacity:0 }} }}
      .rq-h {{ position:relative; width:26px; height:26px; }}
      .rq-h .core {{ position:absolute; inset:7px; background:{theme.GANADOR}; border-radius:50%;
                     box-shadow:0 0 12px {theme.GANADOR}; }}
      .rq-h .ring {{ position:absolute; inset:0; border:2px solid {theme.GANADOR}; border-radius:50%;
                     animation: rqpulse 1.8s ease-out infinite; }}
    </style>
    <div class="rq-h"><div class="ring"></div><div class="core"></div></div>"""
    return folium.Marker(
        [lat, lon],
        icon=folium.DivIcon(html=html, icon_size=(26, 26), icon_anchor=(13, 13)),
        tooltip=f"CENTRO GANADOR: {nombre}",
    )


def mapa_piura(red: dict, resultado: dict | None = None, volar: bool = False) -> folium.Map:
    """Sin resultado: nodos oferta (cian), demanda (rojo) y vías interrumpidas (discontinuas).
    Con resultado: centro ganador con halo y líneas continuas hacia los distritos asignados."""
    if volar:
        m = _oscurecer(folium.Map(location=[-9.2, -75.0], zoom_start=5, tiles=TILES, control_scale=True))
        VolarA(-5.15, -80.30, 9).add_to(m)
    else:
        m = _oscurecer(folium.Map(location=[-5.15, -80.30], zoom_start=9, tiles=TILES, control_scale=True))

    if resultado is None:
        escenario = red["escenarios"][__import__("streamlit").session_state.escenario]
        oferta = red["nodos_oferta"]
        demanda = red["nodos_demanda"]
        cortados = {tuple(a) for a in escenario["arcos_interrumpidos"]}
        arcos = [{"origen": o, "destino": d, "interrumpido": (o, d) in cortados, "activo": False} for o, d in red["arcos"]]
        estados = {n["id"]: "candidato" for n in oferta}
    else:
        oferta, demanda, arcos = resultado["nodos_oferta"], resultado["nodos_demanda"], resultado["arcos"]
        estados = {n["id"]: n["estado"] for n in oferta}

    pos = {n["id"]: (n["lat"], n["lon"]) for n in oferta + demanda}

    for a in arcos:
        if a["interrumpido"]:
            folium.PolyLine([pos[a["origen"]], pos[a["destino"]]], color=theme.DEMANDA,
                            weight=2, dash_array="6 8", opacity=0.8,
                            tooltip="Vía interrumpida").add_to(m)
        elif a["activo"]:
            folium.PolyLine([pos[a["origen"]], pos[a["destino"]]], color=theme.GANADOR,
                            weight=3.5, opacity=0.95).add_to(m)

    for d in demanda:
        extra = ""
        if resultado is not None:
            extra = f" · {d['tiempo_h']} h" if d.get("tiempo_h") else " · SIN COBERTURA"
        folium.CircleMarker(
            [d["lat"], d["lon"]], radius=7, color=theme.DEMANDA, fill=True,
            fill_color=theme.DEMANDA, fill_opacity=0.8,
            tooltip=f"{d['nombre']} · {d['poblacion']:,} hab.{extra}",
        ).add_to(m)

    for n in oferta:
        est = estados[n["id"]]
        if est == "ganador":
            _halo(n["lat"], n["lon"], n["nombre"]).add_to(m)
            continue
        color = theme.GANADOR if est == "activo" else theme.OFERTA
        folium.CircleMarker(
            [n["lat"], n["lon"]], radius=9, color=color, fill=True,
            fill_color=color, fill_opacity=0.9 if est == "activo" else 0.6,
            tooltip=f"{n['nombre']} · {n['capacidad_t']} t",
        ).add_to(m)
    return m
