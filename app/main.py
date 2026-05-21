"""
main.py — Entrada única do app Taipy.
Página única com layout SandBox: sidebar 260px | content.
"""

import pathlib
import sys

_APP_DIR = pathlib.Path(__file__).resolve().parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import data as d
from taipy.gui import Gui, State

# ── Estado inicial ─────────────────────────────────────────────────────────────
map_satellite     = True
map_toggle_lbl    = "Mapa Normal"
sel_idx           = 0

map_fig     = d.make_map_fig(d.TRAJS[0], satellite=True)
profile_fig = d.make_profile_fig(d.TRAJS[0])
fato_fig    = d.make_fato_fig()

# Classe CSS de cada pill (primeiro ativo por padrão)
pill_0 = "traj-pill pill-easa active-pill"
pill_1 = "traj-pill pill-easa"
pill_2 = "traj-pill pill-easa"
pill_3 = "traj-pill pill-easa"
pill_4 = "traj-pill pill-faa"
pill_5 = "traj-pill pill-faa"


# ── Helpers ────────────────────────────────────────────────────────────────────
def _pill_classes(active: int) -> list:
    regs = ["easa", "easa", "easa", "easa", "faa", "faa"]
    return [
        "traj-pill pill-" + regs[i] + (" active-pill" if i == active else "")
        for i in range(6)
    ]


def _select(state: State, idx: int) -> None:
    classes = _pill_classes(idx)
    state.pill_0 = classes[0]
    state.pill_1 = classes[1]
    state.pill_2 = classes[2]
    state.pill_3 = classes[3]
    state.pill_4 = classes[4]
    state.pill_5 = classes[5]
    state.sel_idx     = idx
    state.map_fig     = d.make_map_fig(d.TRAJS[idx], satellite=state.map_satellite)
    state.profile_fig = d.make_profile_fig(d.TRAJS[idx])


def toggle_map_style(state: State, *_) -> None:
    state.map_satellite = not state.map_satellite
    state.map_toggle_lbl = "Mapa Normal" if state.map_satellite else "Satélite"
    state.map_fig = d.make_map_fig(d.TRAJS[state.sel_idx], satellite=state.map_satellite)


# ── Callbacks dos pills ────────────────────────────────────────────────────────
def sel_0(state: State, *_) -> None: _select(state, 0)
def sel_1(state: State, *_) -> None: _select(state, 1)
def sel_2(state: State, *_) -> None: _select(state, 2)
def sel_3(state: State, *_) -> None: _select(state, 3)
def sel_4(state: State, *_) -> None: _select(state, 4)
def sel_5(state: State, *_) -> None: _select(state, 5)


# ── Página ─────────────────────────────────────────────────────────────────────
_PAGE_PATH = _APP_DIR / "pages" / "home.md"
page = _PAGE_PATH.read_text(encoding="utf-8")

# ── Entrypoint ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.chdir(_APP_DIR)
    Gui(page=page, css_file="taipy.css").run(
        title="Trajetória eVTOL — Vertiporto SJC/SBSJ",
        host="0.0.0.0",
        port=5000,
        dark_mode=False,
        margin="0px",
        stylekit=False,
        use_reloader=False,
        watermark="",
    )
