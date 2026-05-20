import os
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from taipy.gui import Markdown

_BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
_CSV_EASA = _BASE_DIR / "Bluesky" / "trajetorias_rampas_vertiporto_EASA_Subpart_2.csv"
_CSV_FAA  = _BASE_DIR / "Bluesky" / "trajetorias_rampas_vertiporto_FAA_eb_105a.csv"

_FIG_DIR = pathlib.Path(__file__).resolve().parents[1] / "figures"
_FIG_DIR.mkdir(parents=True, exist_ok=True)

_FIG_0_PDF   = str(_FIG_DIR / "fig_perfil_rampa_0.pdf")
_FIG_180_PDF = str(_FIG_DIR / "fig_perfil_rampa_180.pdf")
_FIG_0_PNG   = str(_FIG_DIR / "fig_perfil_rampa_0.png")
_FIG_180_PNG = str(_FIG_DIR / "fig_perfil_rampa_180.png")

_COLOR_EASA = "#9ecae1"
_COLOR_FAA  = "#3182bd"
_FONTSIZE   = 11
_RC = {
    "font.size": _FONTSIZE,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "axes.edgecolor": "#cccccc",
    "axes.spines.top": False,
    "axes.spines.right": False,
}


def _load_orientation(df: pd.DataFrame, degrees: int) -> pd.DataFrame:
    mask = df["ramp_name"].str.contains(f"({degrees}°)", regex=False)
    return df.loc[mask].copy()


def _plot_profile(
    easa_df: pd.DataFrame,
    faa_df: pd.DataFrame,
    degrees: int,
    fig_num: int,
    out_pdf: str,
    out_png: str,
) -> None:
    with plt.rc_context(_RC):
        fig, ax = plt.subplots(figsize=(9, 4.5))

        if not easa_df.empty:
            easa_sorted = easa_df.sort_values("distance_along_m")
            ax.plot(
                easa_sorted["distance_along_m"],
                easa_sorted["alt_m"],
                color=_COLOR_EASA,
                linewidth=2,
                label="EASA Subpart 2",
            )

        if not faa_df.empty:
            faa_sorted = faa_df.sort_values("distance_along_m")
            ax.plot(
                faa_sorted["distance_along_m"],
                faa_sorted["alt_m"],
                color=_COLOR_FAA,
                linewidth=2,
                label="FAA EB-105A",
            )

        ax.set_xlabel("Distância ao TLOF (m)", fontsize=_FONTSIZE)
        ax.set_ylabel("Altitude (m)", fontsize=_FONTSIZE)
        ax.set_title(
            f"Figura {fig_num} — Perfil de Rampa de Aproximação (Orientação {degrees}°)",
            fontsize=_FONTSIZE,
            fontweight="bold",
            pad=12,
        )
        ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.7)
        ax.legend(loc="upper right", framealpha=0.9, fontsize=_FONTSIZE - 1)

        fig.tight_layout()
        fig.savefig(out_pdf, format="pdf", bbox_inches="tight")
        fig.savefig(out_png, format="png", dpi=150, bbox_inches="tight")
        plt.close(fig)


def _build_figures() -> None:
    easa = pd.read_csv(_CSV_EASA)
    faa  = pd.read_csv(_CSV_FAA)

    _plot_profile(
        _load_orientation(easa, 0),
        _load_orientation(faa, 0),
        degrees=0,
        fig_num=1,
        out_pdf=_FIG_0_PDF,
        out_png=_FIG_0_PNG,
    )

    _plot_profile(
        _load_orientation(easa, 180),
        _load_orientation(faa, 180),
        degrees=180,
        fig_num=2,
        out_pdf=_FIG_180_PDF,
        out_png=_FIG_180_PNG,
    )


_build_figures()

trajetorias_page = Markdown("""
<|container|

# Trajetórias de Rampa — Comparativo EASA vs. FAA

---

## Perfil de Aproximação — Orientação 0°

Conforme apresentado na Figura 1, o perfil de altitude em função da distância ao TLOF
revela diferenças estruturais entre as normas **EASA Subpart 2** e **FAA EB-105A** para
a orientação de 0°. A norma EASA apresenta uma rampa de maior extensão horizontal, enquanto
o padrão FAA define um percurso mais compacto com ângulo de descida diferenciado.

<|figures/fig_perfil_rampa_0.png|image|width=100%|>

---

## Perfil de Aproximação — Orientação 180°

Conforme apresentado na Figura 2, a orientação de 180° inverte a direção de aproximação ao
vertiporto, mantendo as características regulatórias de cada norma. A comparação evidencia
como cada regulamentação impacta o envelope de proteção ao obstáculo e a geometria da
trajetória de rampa.

<|figures/fig_perfil_rampa_180.png|image|width=100%|>

---

> **Nota:** Os gráficos vetoriais (PDF) estão salvos em `app/figures/` para uso em
> relatórios e publicações. As figuras acima são renderizadas em PNG para exibição no app.

|>
""")
