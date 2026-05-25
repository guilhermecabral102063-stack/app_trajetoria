"""Figuras Plotly para as páginas de trajetória.

Exporta:
  make_map_fig(traj, satellite)  -> go.Figure  mapa de trajetória
  make_profile_fig(traj)         -> go.Figure  perfil de altitude
  make_fato_fig()                -> go.Figure  vista aproximada do FATO
"""

from __future__ import annotations

import plotly.graph_objects as go

from services.leitura import TLOF_LAT, TLOF_LON

_ESRI_SATELLITE = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)

_COR_EASA = "#2563eb"
_COR_FAA  = "#7c3aed"
_FONT = dict(family="Inter, Segoe UI, system-ui, sans-serif", size=11, color="#526078")

_LAYOUT_BASE: dict = dict(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="#ffffff",
    font=_FONT,
)


def make_map_fig(traj: dict, *, satellite: bool = True) -> go.Figure:
    """Mapa Plotly com trajetória colorida por altitude."""
    cor = _COR_EASA if traj["reg"] == "EASA" else _COR_FAA
    fig = go.Figure()

    if traj["lats"]:
        fig.add_trace(go.Scattermapbox(
            lat=traj["lats"], lon=traj["lons"],
            mode="lines",
            line=dict(width=3, color=cor),
            name=traj["label"],
        ))
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

    mapbox_cfg = (
        dict(
            style="white-bg",
            center=dict(lat=TLOF_LAT, lon=TLOF_LON),
            zoom=12,
            layers=[dict(below="traces", sourcetype="raster", source=[_ESRI_SATELLITE])],
        )
        if satellite
        else dict(style="carto-positron", center=dict(lat=TLOF_LAT, lon=TLOF_LON), zoom=12)
    )

    fig.update_layout(
        **_LAYOUT_BASE,
        mapbox=mapbox_cfg,
        height=440,
        legend=dict(
            x=0.01, y=0.99,
            bgcolor="rgba(0,0,0,0.55)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1,
            font=dict(color="#ffffff", size=11),
        ),
    )
    return fig


def make_profile_fig(traj: dict) -> go.Figure:
    """Perfil de altitude ao longo da trajetória de aproximação."""
    cor = _COR_EASA if traj["reg"] == "EASA" else _COR_FAA
    fig = go.Figure()

    if traj["dist_tlof_m"]:
        dist_km = [v / 1000 for v in traj["dist_tlof_m"]]
        r, g, b = int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16)
        fig.add_trace(go.Scatter(
            x=dist_km,
            y=traj["alts_ft"],
            mode="lines",
            line=dict(width=2, color=cor),
            fill="tozeroy",
            fillcolor=f"rgba({r},{g},{b},0.08)",
            name=traj["label"],
            hovertemplate="Dist: %{x:.2f} km<br>Alt: %{y:.0f} ft<extra></extra>",
        ))

    fig.update_layout(
        xaxis=dict(title="Distância percorrida (km)", gridcolor="#dfe6ee", showgrid=True),
        yaxis=dict(title="Altitude AGL (ft)", gridcolor="#dfe6ee", showgrid=True),
        height=240,
        margin=dict(l=56, r=24, t=10, b=48),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f7f9fb",
        font=_FONT,
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
        hovertemplate=(
            f"FATO/TLOF<br>Lat: {TLOF_LAT}°<br>Lon: {TLOF_LON}°<extra></extra>"
        ),
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        mapbox=dict(
            style="white-bg",
            center=dict(lat=TLOF_LAT, lon=TLOF_LON),
            zoom=16,
            layers=[dict(below="traces", sourcetype="raster", source=[_ESRI_SATELLITE])],
        ),
        height=300,
        showlegend=False,
    )
    return fig
