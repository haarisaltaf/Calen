import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QPushButton,
    QToolBar,
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
    GUI that can pop in and out from main window to show
    each day and its events.
    Inherited: QDockWidget
    Parameters: the current Date object
    """

    def __init__(self, selectedDate, dayEvents=None):
        super(DayWidget, self).__init__()
        # Dock can appear on left or right side.
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.RightDockWidgetArea)

        self.label = QLabel(f"{selectedDate.toString()}")
        self.container = QWidget()
        self.vLayout = QVBoxLayout()
        if dayEvents is not None:
            self.dayEvents = QLabel(dayEvents)
            self.vLayout.addWidget(self.dayEvents)

        self.vLayout.addWidget(self.label)
        self.container.setLayout(self.vLayout)
        self.setWidget(self.container)


# TODO: Integrate into Calen -> Display events
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
        self.now = datetime.now()
        self.dateTimeNow = self.now.strftime("%d/%m/%Y, %H:%M:%S")
        self.con = sqlite3.connect("events.db")  # connects to database
        self.cur = self.con.cursor()  # allows SQL executions
        if self.fetchAllEvents() is None:
            print("Attempting creation")
            self.initialCreation()
        print("CheckTables: ", self.checkTables())

    def initialCreation(self):
        """
        Runs if self.checkTables returns an empty tuple ie no tables created.
        Creates the inital table with required headers.
        """
        print('Creating tables')
        self.cur.execute(
            "CREATE TABLE Events (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, date TEXT NOT NULL, rigidity TEXT, location TEXT);")

    def insertEvent(self, eventName="test", eventDate="testDate", rigidity="testRigidity", location="testLocation"):
        """
        Inserts event into Events table. Uses passed through Name,
        Date, Rigidity, Location.
        """

        self.cur.execute(
            "INSERT INTO Events (name, date, rigidity, location) VALUES (?, ?, ?, ?)",
            (eventName, eventDate, rigidity, location)
        )
        self.con.commit()  # commit allows for the changes to persist after closure

    def checkTables(self):
        """
        Grabs table names from sqlite_master, returned using .fetchall()
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print(self.cur.fetchall())

    def deleteEvent(self, eventName="test"):
        """
        Deletes an event based on the passed through parameter.
        """
        self.cur.execute(f"DELETE FROM Events WHERE name = {eventName}")

    def fetchAllEvents(self):
        self.cur.execute("SELECT * FROM Events")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)  # each row is a tuple: (id, name, date, rigidity, location)
        return rows


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

        self.toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.addEventButton = QPushButton("Add Event")
        self.toolbar.addWidget(self.addEventButton)

        # Initalising events then adding calendar
        self.events = Events()
        self.calendar = CalenWidget()
        self.setCentralWidget(self.calendar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalenWindow()
    window.show()
    app.exec()
