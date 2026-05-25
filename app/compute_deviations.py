"""
compute_deviations.py — Calcula desvios laterais (e_y) e verticais (e_z)
para cada trajetória nos 6 STATELOGs.
"""

import math
import pathlib
import statistics

# ── Constantes ─────────────────────────────────────────────────────────────
TLOF_LAT = -23.231441
TLOF_LON = -45.862719
FT_TO_M = 0.3048

EASA_NOMINAL = {
    "distance_m": 1010,
    "altitude_m": 152,  # acima do TLOF
    "gradient": 0.125,
}

FAA_NOMINAL = {
    "distance_m": 602.8,
    "altitude_m": 73.5,  # acima do TLOF
    "gradient": 0.125,
}

# ── Funções auxiliares ─────────────────────────────────────────────────────
def haversine_m(lat1, lon1, lat2, lon2):
    """Distância em metros entre dois pontos (haversine)."""
    R = 6371000  # m
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def compute_deviations(lats, lons, alts_m, dist_to_tlof_m, nominal_config):
    """
    Calcula desvios laterais e verticais para uma trajetória.

    Returns:
        (e_y_list, e_z_list, stats_dict)
    """
    e_y = []  # lateral deviations (m)
    e_z = []  # vertical deviations (m)

    nominal_alt_start = 639.5 + nominal_config["altitude_m"]
    nominal_dist_start = nominal_config["distance_m"]

    for i, (lat, lon, alt_m, dist_m) in enumerate(zip(lats, lons, alts_m, dist_to_tlof_m)):
        # Desvio lateral: distância perpendicular ao eixo de aproximação
        # Simplificação: usar distância lateral (perpendicular) como proxy
        # Em primeira aproximação, usar diferença na coordenada perpendicular
        if i > 0:
            # Lateral deviation: aproximado como variância na lat/lon durante descent
            lat_diff = abs(lat - lats[i-1]) * 111000  # ~111 km per degree
            lon_diff = abs(lon - lons[i-1]) * 111000 * math.cos(math.radians(lat))
            lateral_dev = math.sqrt(lat_diff**2 + lon_diff**2)
            e_y.append(lateral_dev)

        # Desvio vertical: diferença entre altitude real vs. nominal
        # Nominal: descida linear de (nominal_alt_start) a (639.5 m) ao longo de (nominal_dist_start) m
        if dist_m <= nominal_dist_start:
            progress_ratio = 1 - (dist_m / nominal_dist_start)  # 1 no gate, 0 no TLOF
            nominal_alt = 639.5 + (nominal_config["altitude_m"] * progress_ratio)
        else:
            nominal_alt = 639.5  # já no TLOF

        vertical_dev = alt_m - nominal_alt
        e_z.append(vertical_dev)

    # Estatísticas
    stats = {
        "e_y_mean": statistics.mean(e_y) if e_y else 0,
        "e_y_std": statistics.stdev(e_y) if len(e_y) > 1 else 0,
        "e_y_max": max(e_y) if e_y else 0,
        "e_y_min": min(e_y) if e_y else 0,
        "e_z_mean": statistics.mean(e_z) if e_z else 0,
        "e_z_std": statistics.stdev(e_z) if len(e_z) > 1 else 0,
        "e_z_max": max(e_z) if e_z else 0,
        "e_z_min": min(e_z) if e_z else 0,
        "n_points": len(e_z),
    }

    return e_y, e_z, stats


# ── Carregar e processar logs ──────────────────────────────────────────────
def process_statelog(path, nominal_config, reg_type):
    """Processa um STATELOG e retorna desvios."""
    lats, lons, alts_m = [], [], []
    dist_to_tlof_m = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) < 6:
                continue

            try:
                lat = float(parts[2])
                lon = float(parts[3])
                alt_m = float(parts[5])  # em metros
            except ValueError:
                continue

            # Gate filter (20 km)
            dist_km = haversine_m(lat, lon, TLOF_LAT, TLOF_LON) / 1000
            if dist_km > 20:
                continue

            lats.append(lat)
            lons.append(lon)
            alts_m.append(alt_m)
            dist_to_tlof_m.append(dist_km * 1000)

    if not lats:
        return None

    e_y, e_z, stats = compute_deviations(lats, lons, alts_m, dist_to_tlof_m, nominal_config)

    return {
        "reg": reg_type,
        "n_points": len(lats),
        "alt_m_range": (min(alts_m), max(alts_m)),
        "stats": stats,
    }


# ── Processar todos os logs ────────────────────────────────────────────────
def main():
    app_dir = pathlib.Path(__file__).parent

    scenarios = [
        (app_dir / "logs" / "EASA" / "STATELOG_scenario_EASA_R1_0_SBGR_SJK_20260521_15-04-25.log",
         "EASA R1 0deg SBGR-SJK", EASA_NOMINAL),
        (app_dir / "logs" / "EASA" / "STATELOG_scenario_EASA_R2_180_SBGR_SJK_20260521_15-06-18.log",
         "EASA R2 180deg SBGR-SJK", EASA_NOMINAL),
        (app_dir / "logs" / "EASA" / "STATELOG_scenario_EASA_R3_0_TAUBATE_SJK_20260521_15-07-24.log",
         "EASA R1 0deg Taubate-SJK", EASA_NOMINAL),
        (app_dir / "logs" / "EASA" / "STATELOG_scenario_EASA_R4_180_TAUBATE_SJK_20260521_15-08-00.log",
         "EASA R2 180deg Taubate-SJK", EASA_NOMINAL),
        (app_dir / "logs" / "FAA" / "STATELOG_scenario_FAA_R1_0_SBGR_SJK_20260521_16-02-13.log",
         "FAA R1 0deg SBGR-SJK", FAA_NOMINAL),
        (app_dir / "logs" / "FAA" / "STATELOG_scenario_FAA_R2_180_SBGR_SJK_20260521_16-03-51.log",
         "FAA R2 180deg SBGR-SJK", FAA_NOMINAL),
    ]

    results = []

    print("=" * 80)
    print("TRAJECTORY DEVIATION ANALYSIS — SJC/SBSJ VERTIPORT")
    print("=" * 80)

    for path, label, nominal_cfg in scenarios:
        if not path.exists():
            print(f"[SKIP] {label} — arquivo não encontrado")
            continue

        result = process_statelog(path, nominal_cfg, label.split()[0])

        if result:
            results.append((label, result))
            stats = result["stats"]

            print(f"\n{label}")
            print(f"  Points analyzed: {stats['n_points']}")
            print(f"  Lateral deviation (e_y):")
            print(f"    Mean: {stats['e_y_mean']:.2f} m  |  Std: {stats['e_y_std']:.2f} m")
            print(f"    Max:  {stats['e_y_max']:.2f} m  |  Min: {stats['e_y_min']:.2f} m")
            print(f"  Vertical deviation (e_z):")
            print(f"    Mean: {stats['e_z_mean']:.2f} m  |  Std: {stats['e_z_std']:.2f} m")
            print(f"    Max:  {stats['e_z_max']:.2f} m  |  Min: {stats['e_z_min']:.2f} m")

    print("\n" + "=" * 80)
    print("COMPARATIVE SUMMARY")
    print("=" * 80)

    easa_results = [r for l, r in results if "EASA" in l]
    faa_results = [r for l, r in results if "FAA" in l]

    if easa_results:
        easa_e_y_means = [r["stats"]["e_y_mean"] for r in easa_results]
        easa_e_z_means = [r["stats"]["e_z_mean"] for r in easa_results]
        print(f"\nEASA (n={len(easa_results)} scenarios):")
        print(f"  Avg lateral deviation: {statistics.mean(easa_e_y_means):.2f} m")
        print(f"  Avg vertical deviation: {statistics.mean(easa_e_z_means):.2f} m")

    if faa_results:
        faa_e_y_means = [r["stats"]["e_y_mean"] for r in faa_results]
        faa_e_z_means = [r["stats"]["e_z_mean"] for r in faa_results]
        print(f"\nFAA (n={len(faa_results)} scenarios):")
        print(f"  Avg lateral deviation: {statistics.mean(faa_e_y_means):.2f} m")
        print(f"  Avg vertical deviation: {statistics.mean(faa_e_z_means):.2f} m")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
