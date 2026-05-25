"""Página de análise de desvios laterais e verticais."""

from pathlib import Path

from taipy.gui import Markdown

from services.desvios import carregar_resumo_desvios
from services.html import renderizar_dataframe_html

_COLS_CSS: dict[str, str] = {
    "Cenário":          "cell-main",
    "Norma":            "cell-mono cell-short",
    "n pts":            "cell-muted",
    "e_y médio (m)":   "cell-mono",
    "e_y desvpad (m)": "cell-mono",
    "e_y máx (m)":     "cell-mono",
    "e_z médio (m)":   "cell-mono",
    "e_z desvpad (m)": "cell-mono",
    "e_z máx (m)":     "cell-mono",
}

df_desvios = carregar_resumo_desvios()
html_desvios = renderizar_dataframe_html(df_desvios, classes_colunas=_COLS_CSS)


def _montar_markdown() -> str:
    template = (Path(__file__).parent / "desvios.md").read_text(encoding="utf-8")
    return template.replace("<!-- TABELA_DESVIOS -->", html_desvios)


page_desvios = Markdown(_montar_markdown())
