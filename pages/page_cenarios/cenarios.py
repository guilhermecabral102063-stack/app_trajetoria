"""Página de cenários — tabela DoE dos cenários simulados."""

from pathlib import Path

import pandas as pd
from taipy.gui import Markdown

from services.html import renderizar_dataframe_html
from services.leitura import NORMAS, TRAJS

_COLS_CSS: dict[str, str] = {
    "Cenário":     "cell-main",
    "Norma":       "cell-mono cell-short",
    "Rota":        "cell-muted",
    "Orientação":  "cell-muted",
    "Dist. (m)":   "cell-mono",
    "Alt. (m)":    "cell-mono",
    "Gradiente":   "cell-mono",
    "Status":      "cell-muted",
}


def _montar_df_cenarios() -> pd.DataFrame:
    registros = []
    for traj in TRAJS:
        if traj["id"] == "placeholder":
            continue
        norma = NORMAS.get(traj["reg"], {})
        gradient_pct = f"{norma.get('gradient', 0) * 100:.1f} %"
        registros.append({
            "Cenário":    traj["label"],
            "Norma":      traj["reg"],
            "Rota":       traj["route"],
            "Orientação": traj["orient"],
            "Dist. (m)":  f"{norma.get('distance_m', '—'):.0f}",
            "Alt. (m)":   f"{norma.get('altitude_m', '—'):.1f}",
            "Gradiente":  gradient_pct,
            "Status":     "✓ Logado",
        })
    return pd.DataFrame(registros)


df_cenarios = _montar_df_cenarios()
html_cenarios = renderizar_dataframe_html(df_cenarios, classes_colunas=_COLS_CSS)


def _montar_markdown() -> str:
    template = (Path(__file__).parent / "cenarios.md").read_text(encoding="utf-8")
    return template.replace("<!-- TABELA_CENARIOS -->", html_cenarios)


page_cenarios = Markdown(_montar_markdown())
