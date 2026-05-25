"""Componentes HTML simples para páginas Taipy."""

from __future__ import annotations

import html
from collections.abc import Mapping

import pandas as pd


def renderizar_dataframe_html(
    df: pd.DataFrame,
    *,
    classes_colunas: Mapping[str, str] | None = None,
    mensagem_vazia: str = "Tabela não encontrada.",
) -> str:
    """Converte um DataFrame em tabela HTML editorial estática."""
    if df.empty:
        return f'<p class="empty-state">{html.escape(mensagem_vazia)}</p>'

    classes_colunas = classes_colunas or {}
    cabecalho = "".join(
        f"<th>{html.escape(str(coluna))}</th>" for coluna in df.columns
    )

    linhas: list[str] = []
    for registro in df.to_dict(orient="records"):
        celulas: list[str] = []
        for coluna in df.columns:
            valor = "" if registro[coluna] is None else str(registro[coluna])
            classe = classes_colunas.get(str(coluna), "")
            atributo_classe = f' class="{html.escape(classe)}"' if classe else ""
            celulas.append(f"<td{atributo_classe}>{html.escape(valor)}</td>")
        linhas.append("<tr>" + "".join(celulas) + "</tr>")

    return (
        '<div class="html-table-panel">'
        '<table class="html-data-table">'
        f"<thead><tr>{cabecalho}</tr></thead>"
        f"<tbody>{''.join(linhas)}</tbody>"
        "</table>"
        "</div>"
    )
