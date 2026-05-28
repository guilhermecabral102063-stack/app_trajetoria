"""Pagina de visualizacao de trajetorias - mapa + perfil de altitude."""

from pathlib import Path

from taipy.gui import Markdown, State

from services.figuras import make_fato_fig, make_map_fig, make_profile_fig
from services.leitura import TRAJS, TRAJ_LABELS

VIDEO_SRCS = [
    "/assets/videos/traj_0.mp4",
    "/assets/videos/traj_1.mp4",
    "/assets/videos/traj_2.mp4",
    "/assets/videos/traj_3.mp4",
]

map_satellite = True
map_toggle_lbl = "Mapa Normal"

sel_traj_label: str = TRAJ_LABELS[0] if TRAJ_LABELS else "Sem dados"
traj_labels: list[str] = TRAJ_LABELS

map_fig = make_map_fig(TRAJS[0], satellite=True)
profile_fig = make_profile_fig(TRAJS[0])
fato_fig = make_fato_fig()

video_src: str = VIDEO_SRCS[0]


def _pill_cls(idx: int) -> str:
    norma = "easa" if idx < len(TRAJS) and TRAJS[idx]["reg"] == "EASA" else "faa"
    return f"traj-pill pill-{norma}"


pill_0 = _pill_cls(0) + " active-pill"
pill_1 = _pill_cls(1)
pill_2 = _pill_cls(2)
pill_3 = _pill_cls(3)


def _update_pills(state: State, active_idx: int) -> None:
    for i in range(4):
        cls = _pill_cls(i)
        if i == active_idx:
            cls += " active-pill"
        setattr(state, f"pill_{i}", cls)


def _select_traj(state: State, idx: int) -> None:
    if idx >= len(TRAJS):
        return
    traj = TRAJS[idx]
    state.sel_traj_label = TRAJ_LABELS[idx]
    state.map_fig = make_map_fig(traj, satellite=state.map_satellite)
    state.profile_fig = make_profile_fig(traj)
    state.video_src = VIDEO_SRCS[idx]
    _update_pills(state, idx)


def sel_0(state: State, *_) -> None: _select_traj(state, 0)
def sel_1(state: State, *_) -> None: _select_traj(state, 1)
def sel_2(state: State, *_) -> None: _select_traj(state, 2)
def sel_3(state: State, *_) -> None: _select_traj(state, 3)


def toggle_map_style(state: State, *_) -> None:
    state.map_satellite = not state.map_satellite
    state.map_toggle_lbl = "Mapa Normal" if state.map_satellite else "Satelite"
    idx = TRAJ_LABELS.index(state.sel_traj_label) if state.sel_traj_label in TRAJ_LABELS else 0
    state.map_fig = make_map_fig(TRAJS[idx], satellite=state.map_satellite)


page_trajetorias = Markdown(str(Path(__file__).parent / "trajetorias.md"))
