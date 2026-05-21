"""
main.py — Entrada única do app Taipy.
Página única com layout SandBox: sidebar 260px | content.
"""

import pathlib
import sys

# Garante que o diretório do app está no path quando rodado fora dele
_APP_DIR = pathlib.Path(__file__).resolve().parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import data as d
from taipy.gui import Gui, State

# ── Estado inicial ─────────────────────────────────────────────────────────────
selected_traj_idx: str = d.traj_labels[0]   # selector usa o label como valor
traj_labels        = d.traj_labels
map_fig            = d.make_map_fig(d.TRAJS[0])
profile_fig        = d.make_profile_fig(d.TRAJS[0])


# ── Callback do selector ───────────────────────────────────────────────────────
def on_traj_change(state: State) -> None:
    """Atualiza mapa e perfil quando o usuário escolhe outra trajetória."""
    label = state.selected_traj_idx
    try:
        idx = d.traj_labels.index(label)
    except ValueError:
        idx = 0
    state.map_fig     = d.make_map_fig(d.TRAJS[idx])
    state.profile_fig = d.make_profile_fig(d.TRAJS[idx])


# ── Página ─────────────────────────────────────────────────────────────────────
_PAGE_PATH = _APP_DIR / "pages" / "home.md"
page = _PAGE_PATH.read_text(encoding="utf-8")

# ── Entrypoint ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    Gui(page=page, css_file=str(_APP_DIR / "taipy.css")).run(
        title="Trajetória eVTOL — Vertiporto SJC/SBSJ",
        host="0.0.0.0",
        port=5000,
        dark_mode=False,
        margin="0px",
        stylekit=False,
        use_reloader=False,
        watermark="",
    )
