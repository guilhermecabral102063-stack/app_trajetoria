from taipy.gui import Gui
from pages.home import home_page

pages = {
    "/": home_page,
}

if __name__ == "__main__":
    gui = Gui(pages=pages)
    gui.run(
        host="0.0.0.0",
        port=5000,
        title="App Trajetória — Vertiporto SJC",
        dark_mode=False,
    )
