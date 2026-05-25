"""Carrega STATELOGs BlueSky e expõe os dados de trajetória.

Exporta:
  TRAJS        : list[dict] — trajetórias carregadas
  TRAJ_LABELS  : list[str] — rótulos para seletores
  NORMAS       : dict — parâmetros nominais por padrão normativo
"""

from __future__ import annotations

import math
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_DATA_DIR = _ROOT / "data" / "logs"
_EASA_DIR = _DATA_DIR / "EASA"
_FAA_DIR = _DATA_DIR / "FAA"

TLOF_LAT: float = -23.231441
TLOF_LON: float = -45.862719
GATE_KM: float = 20.0
STEP_S: float = 5.0
FT_TO_M: float = 0.3048

# Gradientes corretos: EASA 152/1010 = 15,05 %; FAA 73,5/602,8 = 12,19 %
NORMAS: dict[str, dict[str, float]] = {
    "EASA": {"distance_m": 1010.0, "altitude_m": 152.0, "gradient": 0.1505},
    "FAA":  {"distance_m": 602.8,  "altitude_m": 73.5,  "gradient": 0.1219},
}

_LOG_SPECS: list[tuple] = [
    (
        _EASA_DIR / "STATELOG_scenario_EASA_R1_0_SBGR_SJK_20260521_15-04-25.log",
        "EASA_R1_0_SBGR", "EASA", "R1", "0°", "SBGR → SJK",
    ),
    (
        _EASA_DIR / "STATELOG_scenario_EASA_R2_180_SBGR_SJK_20260521_15-06-18.log",
        "EASA_R2_180_SBGR", "EASA", "R2", "180°", "SBGR → SJK",
    ),
    (
        _EASA_DIR / "STATELOG_scenario_EASA_R3_0_TAUBATE_SJK_20260521_15-07-24.log",
        "EASA_R3_0_TAU", "EASA", "R1", "0°", "Taubaté → SJK",
    ),
    (
        _EASA_DIR / "STATELOG_scenario_EASA_R4_180_TAUBATE_SJK_20260521_15-08-00.log",
        "EASA_R4_180_TAU", "EASA", "R2", "180°", "Taubaté → SJK",
    ),
    (
        _FAA_DIR / "STATELOG_scenario_FAA_R1_0_SBGR_SJK_20260521_16-02-13.log",
        "FAA_R1_0_SBGR", "FAA", "R1", "0°", "SBGR → SJK",
    ),
    (
        _FAA_DIR / "STATELOG_scenario_FAA_R2_180_SBGR_SJK_20260521_16-03-51.log",
        "FAA_R2_180_SBGR", "FAA", "R2", "180°", "SBGR → SJK",
    ),
]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return _haversine_km(lat1, lon1, lat2, lon2) * 1000.0


def carregar_trajetoria(
    path: Path,
    tid: str,
    reg: str,
    config: str,
    orient: str,
    route: str,
) -> dict:
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
                alt_raw = float(parts[5])  # BlueSky reporta em metros
            except ValueError:
                continue

            if _haversine_km(lat, lon, TLOF_LAT, TLOF_LON) > GATE_KM:
                continue
            if (t - last_t) < STEP_S and lats:
                continue

            last_t = t
            lats.append(lat)
            lons.append(lon)
            alts_m.append(round(alt_raw, 1))
            alts_ft.append(round(alt_raw / FT_TO_M, 1))

    dist_tlof_m: list[float] = []
    cum = 0.0
    prev_lat, prev_lon = None, None
    for lat, lon in zip(lats, lons):
        cum = 0.0 if prev_lat is None else cum + _haversine_m(prev_lat, prev_lon, lat, lon)
        dist_tlof_m.append(round(cum, 1))
        prev_lat, prev_lon = lat, lon

    reg_label = "EASA Subpart 2" if reg == "EASA" else "FAA EB-105A"
    return {
        "id": tid,
        "label": f"{reg_label} {config} {orient} — {route}",
        "reg": reg,
        "config": config,
        "orient": orient,
        "route": route,
        "lats": lats,
        "lons": lons,
        "alts_m": alts_m,
        "alts_ft": alts_ft,
        "dist_tlof_m": dist_tlof_m,
    }


def carregar_todas() -> list[dict]:
    """Carrega todos os STATELOGs registrados."""
    trajs: list[dict] = []
    for path, tid, reg, cfg, ori, rte in _LOG_SPECS:
        try:
            trajs.append(carregar_trajetoria(path, tid, reg, cfg, ori, rte))
        except FileNotFoundError:
            print(f"[leitura] AVISO: log não encontrado — {path}")
    if not trajs:
        trajs = [{
            "id": "placeholder", "label": "Sem dados", "reg": "EASA",
            "config": "—", "orient": "—", "route": "—",
            "lats": [], "lons": [], "alts_m": [], "alts_ft": [], "dist_tlof_m": [],
        }]
    return trajs


TRAJS: list[dict] = carregar_todas()
TRAJ_LABELS: list[str] = [t["label"] for t in TRAJS]
