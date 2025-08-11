import sys
import sqlite3
# from datetime import datetime
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

# QMainWindow for main background with QCalendarWidget class
# to repeatedly create QDockWidget objects for each day.


class DayWidget(QDockWidget):
    """
    GUI that can pop in and out from main window to show:w
    each day and its events.
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


# TODO: implement events and appointments
class Events():
    """
    Events class to create an SQLite Database (events.db).
    Handles querying and creation of database.
    """

    def __init__(self):
        """
        Handles connecting to events.db and 
        inital creation of table and 
        creates cursor to handle SQL execution.
        """
        self.con = sqlite3.connect("events.db")  # connects to database
        self.cur = self.con.cursor()  # allows SQL executions
        if self.checkTables() is None:
            print("Attempting creation")
            self.initialCreation()
        print(self.checkTables())

    def initialCreation(self):
        """
        Runs if self.checkTables returns an empty tuple ie no tables created.
        Creates the inital table with required headers.
        """
        print('Creating tables')
        self.cur.execute("CREATE TABLE events(name, date, rigidity, location)")

    def insertEvent(self, eventName="test", eventDate="testDate", rigidity="testRigidity", location="testLocation"):
        """
        Inserts event into Events table. Uses passed through Name,
        Date, Rigidity, Location.
        """
        self.cur.execute(f"INSERT INTO Events VALUES (f{eventName}, f{
                         eventDate}, f{rigidity}, f{location})")

    def checkTables(self):
        """
        Grabs table names from sqlite_master, returned using .fetchone()
        """
        self.tableNames = self.cur.execute("SELECT * FROM sqlite_master")
        return self.tableNames.fetchone()


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
        self.events = Events()
        self.calendar = CalenWidget()
        self.setCentralWidget(self.calendar)


if __name__ == "__main__":
    eventsTest = Events()
    app = QApplication(sys.argv)
    window = CalenWindow()
    window.show()
    app.exec()
