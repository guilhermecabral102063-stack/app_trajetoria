"""Página de parâmetros da aeronave e norma de aproximação."""

from pathlib import Path

from taipy.gui import Markdown

from services.leitura import NORMAS

norma_easa = NORMAS["EASA"]

page_aeronave = Markdown(str(Path(__file__).parent / "aeronave.md"))
