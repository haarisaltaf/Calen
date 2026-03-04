import sys
from PyQt6.QtWidgets import QApplication
from gui.CalenWindowClass import CalenWindow
from database.EventsClass import Events


if __name__ == "__main__":
    events = Events()
    app = QApplication(sys.argv)
    window = CalenWindow(events)
    window.show()
    app.exec()
    events.close()
