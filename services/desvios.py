"""Cálculo de desvios laterais (e_y) e verticais (e_z) por trajetória.

Exporta:
  calcular_desvios(traj, norma)  -> dict com e_y_list, e_z_list, stats
  carregar_resumo_desvios()      -> pd.DataFrame com stats de todos os cenários
"""

from __future__ import annotations

import math
import statistics

import pandas as pd

from services.leitura import NORMAS, TRAJS


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6_371_000.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


def calcular_desvios(traj: dict, norma: dict) -> dict:
    """Calcula desvios laterais e verticais para uma trajetória.

    Retorna dict com:
      e_y, e_z  — listas de desvios (m)
      stats     — dicionário de estatísticas resumidas
    """
    lats = traj["lats"]
    lons = traj["lons"]
    alts_m = traj["alts_m"]
    dist_to_tlof_m = traj["dist_tlof_m"]

    dist_gate = norma["distance_m"]
    alt_gate = norma["altitude_m"]
    alt_tlof = 639.5  # altitude AMSL do TLOF/SBSJ (m)

    e_y: list[float] = []
    e_z: list[float] = []

    for i, (lat, lon, alt_m, dist_m) in enumerate(
        zip(lats, lons, alts_m, dist_to_tlof_m)
    ):
        # Desvio lateral: variação ponto a ponto perpendicular ao eixo de aproximação
        if i > 0:
            lat_diff = abs(lat - lats[i - 1]) * 111_000
            lon_diff = (
                abs(lon - lons[i - 1]) * 111_000 * math.cos(math.radians(lat))
            )
            e_y.append(math.sqrt(lat_diff ** 2 + lon_diff ** 2))

        # Desvio vertical: altitude real vs. rampa nominal linear
        if dist_m <= dist_gate:
            progress = 1.0 - dist_m / dist_gate
            nominal_alt = alt_tlof + alt_gate * progress
        else:
            nominal_alt = alt_tlof
        e_z.append(alt_m - nominal_alt)

    _mean = lambda lst: statistics.mean(lst) if lst else 0.0
    _std  = lambda lst: statistics.stdev(lst) if len(lst) > 1 else 0.0

    return {
        "e_y": e_y,
        "e_z": e_z,
        "stats": {
            "e_y_mean": _mean(e_y),
            "e_y_std":  _std(e_y),
            "e_y_max":  max(e_y) if e_y else 0.0,
            "e_z_mean": _mean(e_z),
            "e_z_std":  _std(e_z),
            "e_z_max":  max(e_z) if e_z else 0.0,
            "n_pontos": len(e_z),
        },
    }


def carregar_resumo_desvios() -> pd.DataFrame:
    """Processa todos os cenários e retorna tabela de estatísticas."""
    registros: list[dict] = []
    for traj in TRAJS:
        if not traj["lats"]:
            continue
        norma = NORMAS.get(traj["reg"])
        if norma is None:
            continue
        resultado = calcular_desvios(traj, norma)
        s = resultado["stats"]
        registros.append({
            "Cenário":        traj["label"],
            "Norma":          traj["reg"],
            "n pts":          s["n_pontos"],
            "e_y médio (m)":  f"{s['e_y_mean']:.2f}",
            "e_y desvpad (m)": f"{s['e_y_std']:.2f}",
            "e_y máx (m)":    f"{s['e_y_max']:.2f}",
            "e_z médio (m)":  f"{s['e_z_mean']:.2f}",
            "e_z desvpad (m)": f"{s['e_z_std']:.2f}",
            "e_z máx (m)":    f"{s['e_z_max']:.2f}",
        })
    return pd.DataFrame(registros)
