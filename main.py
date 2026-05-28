"""Entrada do aplicativo de trajetórias eVTOL — Vertiporto SBSJ."""

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from taipy.gui import Gui, Icon, State, navigate

from pages.page_trajetorias.trajetorias import (
    fato_fig,
    map_fig,
    map_satellite,
    map_toggle_lbl,
    page_trajetorias,
    pill_0, pill_1, pill_2, pill_3,
    profile_fig,
    sel_0, sel_1, sel_2, sel_3,
    sel_traj_idx,
    sel_traj_label,
    toggle_map_style,
    traj_labels,
)
from pages.page_aeronave.aeronave import (
    norma_easa,
    page_aeronave,
)

menu_items = [
    ("trajetorias", Icon("/assets/trajetorias.svg", "Trajetórias")),
    ("aeronave",    Icon("/assets/aeronave.svg",    "Parâmetros")),
]


def on_menu(state: State, id, payload) -> None:
    navigate(state, payload["args"][0])


if __name__ == "__main__":
    host = os.environ.get("TAIPY_HOST", "127.0.0.1")
    port = int(os.environ.get("TAIPY_PORT", "5000"))
    use_reloader = os.environ.get("TAIPY_RELOADER", "1").lower() in {
        "1", "true", "yes", "on",
    }

    pages = {
        "trajetorias": page_trajetorias,
        "aeronave":    page_aeronave,
    }

    Gui(
        pages=pages,
        css_file="taipy.css",
        path_mapping={"assets": str(_ROOT / "assets")},
    ).run(
        title="Trajetória eVTOL — Vertiporto SJC/SBSJ",
        host=host,
        port=port,
        margin="0px",
        dark_mode=False,
        use_reloader=use_reloader,
        watermark="",
    )
