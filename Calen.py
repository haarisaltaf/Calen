import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QCalendarWidget,
    QDockWidget,
    QApplication,
    QMainWindow
)
from PyQt6.QtCore import Qt

# QMainWindow for main background with QCalendarWidget class to repeatedly create QDockWidget objects for each day.


class DayWidget(QDockWidget):
    """
    GUI that can pop in and out from main window to show each day and its events.
    Inherited: QDockWidget
    Parameters: the current Date object
    """

    def __init__(self, selectedDate):
        super(DayWidget, self).__init__()
        # Dock can appear on left or right side.
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.RightDockWidgetArea)

        self.label = QLabel(f"{selectedDate.toString()}")
        self.container = QWidget()
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.label)
        self.container.setLayout(self.vLayout)
        self.setWidget(self.container)


class Appointments():
    def __init__(self):
        return None


class CalenWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super(CalenWidget, self).__init__()
        self.clicked.connect(self.onClickedDate)

    def onClickedDate(self, date):
        currentDay = DayWidget(date)
        self.parent().addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                                    currentDay)


class CalenWindow(QMainWindow):
    """
    GUI that will hold the calendar widget (CalenWindow) and appointment list.
    Dock Widget will be used to add appointments.
    """

    def __init__(self, parent=None):
        super(CalenWindow, self).__init__()
        self.setWindowTitle("Calen")
        self.resize(800, 600)

        # Defining needed Classes/ Methods
        self.appointments = Appointments()
        self.calendar = CalenWidget()
        self.setCentralWidget(self.calendar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalenWindow()
    window.show()
    app.exec()
