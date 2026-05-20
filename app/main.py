from taipy.gui import Gui, navigate
from pages.home import home_page
from pages.trajetorias import trajetorias_page

pages = {
    "/": home_page,
    "trajetorias": trajetorias_page,
}


def navigate_trajetorias(state):
    navigate(state, "trajetorias")


if __name__ == "__main__":
    gui = Gui(pages=pages)
    gui.run(
        host="0.0.0.0",
        port=5000,
        title="App Trajetória — Vertiporto SJC",
        dark_mode=False,
    )
