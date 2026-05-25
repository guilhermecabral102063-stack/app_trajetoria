"""Página inicial — Simulação de Trajetórias eVTOL."""

from datetime import datetime
from pathlib import Path

from taipy.gui import Markdown

DIAS_SEMANA = {
    0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
    3: "quinta-feira",  4: "sexta-feira", 5: "sábado", 6: "domingo",
}


def _formatar_data_hora() -> tuple[str, str, str]:
    agora = datetime.now().astimezone()
    dia = f"{DIAS_SEMANA[agora.weekday()]}, {agora:%d/%m/%Y}"
    hora = agora.strftime("%H:%M:%S")
    fuso = agora.tzname() or "fuso local"
    return dia, hora, fuso


dia_sistema, hora_sistema, fuso_sistema = _formatar_data_hora()

page_home = Markdown(str(Path(__file__).parent / "home.md"))
