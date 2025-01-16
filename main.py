import win32gui
from core.game import Game
from core.gamemaster import GameMaster

emu_name = "LDPlayer"
emu_size = Game.size
emus = []
def enum_windows(handle, result):
    title = win32gui.GetWindowText(handle)
    if title and emu_name in title:
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        emus.append((title, left, top))
        
# finding the emulator windows and creating instances for them.
win32gui.EnumWindows(enum_windows, None)

app = Game(emus[0][0], emus[0][1:])
master = GameMaster(app)

import sys
import multiprocessing
from fastapi import FastAPI, Request
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from uvicorn import Config, Server
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# Define FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/solve")
def solve_letters(request: Request):
    master.recognize_letters()
    return templates.TemplateResponse("solved.html", {"request": request})

# Function to start FastAPI server
def start_server():
    config = Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = Server(config)
    server.run()

# Define the PyQt Browser App
class BrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Master")
        self.setGeometry(100, 100, 1024, 768)

        # Create the browser widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.setWindowIcon(QIcon("./static/logo.jpg"))
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000"))  # URL of the FastAPI server
        layout.addWidget(self.browser)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

# Function to start the PyQt browser
def start_browser():
    app = QApplication(sys.argv)
    browser = BrowserApp()
    browser.show()
    sys.exit(app.exec_())

# Main function to run both processes
if __name__ == "__main__":
    # Start the FastAPI server in a separate process
    server_process = multiprocessing.Process(target=start_server)
    server_process.start()

    try:
        # Start the PyQt browser in the main process
        start_browser()
    finally:
        # Ensure the server process is terminated when the app exits
        server_process.terminate()
        server_process.join()
