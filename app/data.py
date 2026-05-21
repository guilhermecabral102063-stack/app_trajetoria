"""
data.py — Carrega STATELOGs BlueSky e expõe variáveis para o app Taipy.

Exporta:
  TRAJS            : lista de dicts com dados de trajetória
  traj_labels      : lista de strings para o selector
  selected_traj_idx: int (0 por padrão)
  make_map_fig(traj)    -> plotly.graph_objects.Figure
  make_profile_fig(traj) -> plotly.graph_objects.Figure
"""

import math
import pathlib

import plotly.graph_objects as go

# ── Constantes ────────────────────────────────────────────────────────────────
TLOF_LAT  = -23.231441
TLOF_LON  = -45.862719
GATE_KM   = 20.0
STEP_S    = 5.0
FT_TO_M   = 0.3048

# ── Localização dos logs ───────────────────────────────────────────────────────
_EASA_OUT = pathlib.Path(
    r"C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\EASA\Outputs"
)
_FAA_OUT = pathlib.Path(
    r"C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\FAA\output"
)

_LOG_SPECS = [
    (_EASA_OUT / "STATELOG_scenario_EASA_R1_0_SBGR_SJK_20260521_15-04-25.log",
     "EASA_R1_0_SBGR",  "EASA", "R1", "0°",   "SBGR → SJK"),
    (_EASA_OUT / "STATELOG_scenario_EASA_R2_180_SBGR_SJK_20260521_15-06-18.log",
     "EASA_R2_180_SBGR", "EASA", "R2", "180°", "SBGR → SJK"),
    (_EASA_OUT / "STATELOG_scenario_EASA_R3_0_TAUBATE_SJK_20260521_15-07-24.log",
     "EASA_R3_0_TAU",   "EASA", "R1", "0°",   "Taubaté → SJK"),
    (_EASA_OUT / "STATELOG_scenario_EASA_R4_180_TAUBATE_SJK_20260521_15-08-00.log",
     "EASA_R4_180_TAU", "EASA", "R2", "180°", "Taubaté → SJK"),
    (_FAA_OUT  / "STATELOG_scenario_FAA_R1_0_SBGR_SJK_20260521_16-02-13.log",
     "FAA_R1_0_SBGR",   "FAA",  "R1", "0°",   "SBGR → SJK"),
    (_FAA_OUT  / "STATELOG_scenario_FAA_R2_180_SBGR_SJK_20260521_16-03-51.log",
     "FAA_R2_180_SBGR", "FAA",  "R2", "180°", "SBGR → SJK"),
]


# ── Funções auxiliares ─────────────────────────────────────────────────────────
def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return _haversine_km(lat1, lon1, lat2, lon2) * 1000.0


def _load_traj(path: pathlib.Path, tid: str, reg: str,
               config: str, orient: str, route: str) -> dict:
    """Lê um STATELOG e retorna dicionário de trajetória filtrado/subsampled."""
    lats, lons, alts_m, alts_ft = [], [], [], []
    last_t = -9999.0

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) < 6:
                continue
            try:
                t      = float(parts[0])
                lat    = float(parts[2])
                lon    = float(parts[3])
                alt_ft = float(parts[5])
            except ValueError:
                continue

            dist_km = _haversine_km(lat, lon, TLOF_LAT, TLOF_LON)
            if dist_km > GATE_KM:
                continue
            if (t - last_t) < STEP_S and lats:
                continue

            last_t = t
            lats.append(lat)
            lons.append(lon)
            alt_m = alt_ft          # coluna "alt" do BlueSky está em metros
            alts_m.append(round(alt_m, 1))
            alts_ft.append(round(alt_m / FT_TO_M, 1))

    # Distância acumulada ao longo do trecho (para perfil)
    dist_tlof_m = []
    cum = 0.0
    prev_lat, prev_lon = None, None
    for lat, lon in zip(lats, lons):
        if prev_lat is None:
            cum = 0.0
        else:
            cum += _haversine_m(prev_lat, prev_lon, lat, lon)
        dist_tlof_m.append(round(cum, 1))
        prev_lat, prev_lon = lat, lon

    reg_label   = "EASA Subpart 2" if reg == "EASA" else "FAA EB-105A"
    label = f"{reg_label} {config} {orient} — {route}"

    return {
        "id":          tid,
        "label":       label,
        "reg":         reg,
        "config":      config,
        "orient":      orient,
        "route":       route,
        "lats":        lats,
        "lons":        lons,
        "alts_m":      alts_m,
        "alts_ft":     alts_ft,
        "dist_tlof_m": dist_tlof_m,
    }


# ── Carregar todos os logs ─────────────────────────────────────────────────────
TRAJS: list[dict] = []
for _spec in _LOG_SPECS:
    _path, _tid, _reg, _cfg, _ori, _rte = _spec
    try:
        TRAJS.append(_load_traj(_path, _tid, _reg, _cfg, _ori, _rte))
    except FileNotFoundError:
        print(f"[data.py] AVISO: log não encontrado — {_path}")

if not TRAJS:
    # Fallback vazio para não quebrar o app quando logs estão ausentes
    TRAJS = [{
        "id": "placeholder", "label": "Sem dados", "reg": "EASA",
        "config": "—", "orient": "—", "route": "—",
        "lats": [], "lons": [], "alts_m": [], "dist_tlof_m": [],
    }]

traj_labels: list[str]   = [t["label"] for t in TRAJS]
selected_traj_idx: int   = 0


# ── Figuras Plotly ─────────────────────────────────────────────────────────────
_ESRI_SATELLITE = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)

_FONT = dict(family="Inter, Segoe UI, system-ui, sans-serif", size=11, color="#526078")


def make_map_fig(traj: dict, satellite: bool = True) -> go.Figure:
    color = "#2563eb" if traj["reg"] == "EASA" else "#7c3aed"
    fig = go.Figure()
    if traj["lats"]:
        fig.add_trace(go.Scattermapbox(
            lat=traj["lats"], lon=traj["lons"],
            mode="lines",
            line=dict(width=3, color=color),
            name=traj["label"],
        ))
    if traj["lats"]:
        fig.add_trace(go.Scattermapbox(
            lat=traj["lats"], lon=traj["lons"],
            mode="markers",
            marker=dict(
                size=5,
                color=traj["alts_ft"],
                colorscale="Blues",
                cmin=0,
                cmax=max(traj["alts_ft"]) if traj["alts_ft"] else 500,
                showscale=False,
            ),
            hovertemplate="Alt: %{marker.color:.0f} ft<extra></extra>",
            showlegend=False,
        ))
    fig.add_trace(go.Scattermapbox(
        lat=[TLOF_LAT], lon=[TLOF_LON],
        mode="markers+text",
        marker=dict(size=14, color="#e53e3e"),
        text=["FATO/TLOF"],
        textposition="top right",
        textfont=dict(size=11, color="#ffffff"),
        name="FATO/TLOF",
        hovertemplate="FATO/TLOF — SJC/SBSJ<extra></extra>",
    ))
    if satellite:
        mapbox_cfg = dict(
            style="white-bg",
            center=dict(lat=TLOF_LAT, lon=TLOF_LON),
            zoom=12,
            layers=[dict(below="traces", sourcetype="raster", source=[_ESRI_SATELLITE])],
        )
    else:
        mapbox_cfg = dict(
            style="carto-positron",
            center=dict(lat=TLOF_LAT, lon=TLOF_LON),
            zoom=12,
        )
    fig.update_layout(
        mapbox=mapbox_cfg,
        margin=dict(l=0, r=0, t=0, b=0),
        height=440,
        paper_bgcolor="#ffffff",
        font=_FONT,
        legend=dict(
            x=0.01, y=0.99,
            bgcolor="rgba(0,0,0,0.55)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1,
            font=dict(color="#ffffff", size=11),
        ),
    )
    return fig


def make_fato_fig() -> go.Figure:
    """Vista aproximada do FATO/TLOF com tiles de satélite."""
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        lat=[TLOF_LAT], lon=[TLOF_LON],
        mode="markers+text",
        marker=dict(size=16, color="#e53e3e", symbol="circle"),
        text=["FATO/TLOF"],
        textposition="top right",
        textfont=dict(size=12, color="#ffffff"),
        name="FATO/TLOF",
        hovertemplate="FATO/TLOF<br>Lat: -23.231441°<br>Lon: -45.862719°<extra></extra>",
    ))
    fig.update_layout(
        mapbox=dict(
            style="white-bg",
            center=dict(lat=TLOF_LAT, lon=TLOF_LON),
            zoom=16,
            layers=[dict(
                below="traces",
                sourcetype="raster",
                source=[_ESRI_SATELLITE],
            )],
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        paper_bgcolor="#ffffff",
        font=_FONT,
        showlegend=False,
    )
    return fig


def make_profile_fig(traj: dict) -> go.Figure:
    color = "#2563eb" if traj["reg"] == "EASA" else "#7c3aed"
    fig = go.Figure()
    if traj["dist_tlof_m"]:
        dist_km = [v / 1000 for v in traj["dist_tlof_m"]]
        fig.add_trace(go.Scatter(
            x=dist_km,
            y=traj["alts_ft"],
            mode="lines",
            line=dict(width=2, color=color),
            fill="tozeroy",
            fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)",
            name=traj["label"],
            hovertemplate="Dist: %{x:.2f} km<br>Alt: %{y:.0f} ft<extra></extra>",
        ))
    fig.update_layout(
        xaxis=dict(title="Distância percorrida (km)", gridcolor="#dfe6ee", showgrid=True),
        yaxis=dict(title="Altitude AGL (ft)", gridcolor="#dfe6ee", showgrid=True),
        height=220,
        margin=dict(l=50, r=20, t=10, b=40),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f7f9fb",
        font=_FONT,
    )
    return fig
