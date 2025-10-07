import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QMessageBox,
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QLineEdit,
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
from PyQt6.QtCore import Qt, QDateTime

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
            # Adds the events as a label
            self.vLayout.addWidget(self.dayEvents)

        self.vLayout.addWidget(self.label)
        self.container.setLayout(self.vLayout)
        self.setWidget(self.container)

        # TODO: Add events for that day to the widget -- grab events from database and add as a label to the widget


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
            "CREATE TABLE Events (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, date TEXT NOT NULL, rigidity INTEGER, location TEXT);")

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
        print("fetchAllEvents:")
        for row in rows:
            print(row)  # each row is a tuple: (id, name, date, rigidity, location)
        print("")
        return rows

    def fetchDayEvents(self, date):
        self.cur.execute("SELECT * FROM Events WHERE date LIKE ?", date)
        dayEvents = self.cur.fetchall()
        return dayEvents


class AddEventGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Event")

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Event Name:"))
        self.eventNameInput = QLineEdit()
        self.layout.addWidget(self.eventNameInput)

        self.layout.addWidget(QLabel("Date of Event:"))
        self.eventDateInput = QDateTimeEdit()
        self.eventDateInput.setDateTime(QDateTime.currentDateTime())
        self.eventDateInput.setCalendarPopup(True)
        self.layout.addWidget(self.eventDateInput)

        self.layout.addWidget(QLabel("Rigidity:"))
        self.eventRigidityInput = QComboBox()
        self.eventRigidityInput.addItems(["Rigid", "Dynamic"])
        self.layout.addWidget(self.eventRigidityInput)

        self.layout.addWidget(QLabel("Location:"))
        self.eventLocationInput = QLineEdit()
        self.layout.addWidget(self.eventLocationInput)

        self.saveButton = QPushButton("Save")
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

        self.saveButton.clicked.connect(self.accept)

    def getAllData(self):
        """
        Grabs all the data for the new event added.
        """

        return {
            "name": self.eventNameInput.text(),
            "date": self.eventDateInput.dateTime().toString("dd-MM-yyyy HH:mm"),
            "rigidity": self.eventRigidityInput.currentText(),
            "location": self.eventLocationInput.text()
        }


class removeEventGUI(QDialog):
    def __init__(self, currAppointments):
        super().__init__()
        self.setWindowTitle("Remove Event")

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Select event to remove:"))
        self.removeEventSelector = QComboBox()
        self.removeEventSelector.addItems([str(currAppointments)])
        self.layout.addWidget(self.removeEventSelector)


class CalenWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super(CalenWidget, self).__init__()
        self.clicked.connect(self.onClickedDate)

    def onClickedDate(self, date):
        self.selectedDay = date.toString("dd-MM-yyyy")
        # TODO: passthrough the selected day to events.fetch
        print("date:", self.selectedDay)

        # grabbing today's events and passing into day widget
        conn = sqlite3.connect("events.db")
        c = conn.cursor()
        c.execute(
            f"SELECT * FROM Events WHERE date LIKE \'%{self.selectedDay}%\'")
        rows = c.fetchall()
        conn.close()
        print(rows)
        currentDayDockWidget = DayWidget(date, str(rows))

        self.parent().addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                                    currentDayDockWidget)


class CalenWindow(QMainWindow):
    """
    GUI that will hold the calendar widget (CalenWindow) and appointment list.
    Dock Widget will be used to add appointments.
    """

    def __init__(self, parent=None):
        super(CalenWindow, self).__init__()
        self.setWindowTitle("Calen")
        self.resize(800, 600)

        # adding toolbar
        self.toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        self.addEventButton = QPushButton("Add Event")
        self.toolbar.addWidget(self.addEventButton)
        self.addEventButton.clicked.connect(self.openAddEventGUI)

        # Initalising events then adding calendar
        self.events = Events()
        self.calendar = CalenWidget()
        self.setCentralWidget(self.calendar)

        self.removeEventButton = QPushButton("Remove Event")
        # TODO: implement removing events
        self.toolbar.addWidget(self.removeEventButton)
        self.removeEventButton.clicked.connect(
            self.openRemoveEventGUI(self.events.fetchAllEvents))

    def openAddEventGUI(self):
        self.addEventWindow = AddEventGUI()
        if self.addEventWindow.exec():
            # checks if the user has exited via save.
            self.newEventData = self.addEventWindow.getAllData()
            QMessageBox.information(self, "Event Added",
                                    f"Name: {self.newEventData['name']}\n"
                                    f"Date: {self.newEventData['date']}\n"
                                    f"Type: {self.newEventData['rigidity']}\n"
                                    f"Desc: {self.newEventData['location']}")
            # piping the data into the database
            conn = sqlite3.connect("events.db")
            c = conn.cursor()
            c.execute("INSERT INTO events (name, date, rigidity, location) VALUES (?, ?, ?, ?)",
                      (self.newEventData['name'],
                       self.newEventData['date'],
                       self.newEventData['rigidity'],
                       self.newEventData['location']))
            conn.commit()
            conn.close()
        else:
            QMessageBox.information(self, "Event Not Saved")

    def openRemoveEventGUI(self, currAppointments):
        self.removeEventGUI = removeEventGUI(currAppointments)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalenWindow()
    window.show()
    app.exec()
