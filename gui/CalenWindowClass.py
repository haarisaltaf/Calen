from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QToolBar,
    QMainWindow
)
import logging
from PyQt6.QtCore import Qt
from database.EventsClass import Events
from gui.CalenWidgetClass import CalenWidget
from gui.AddEventGUIClass import AddEventGUI
from gui.RemoveEventGUIClass import RemoveEventGUI


class CalenWindow(QMainWindow):
    """
    GUI that will hold the calendar widget (CalenWindow) and appointment list.
    Dock Widget will be used to add appointments.
    """

    def __init__(self, parent=None, events=Events()):
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
        self.events = events
        if self.events is None:
            logging.critical(
                "CalenWindow has recieced 'None' as its eventService, continuing with new Events instance")
        print("ALL EVENTS: ", self.events.fetchAllEvents())
        self.calendar = CalenWidget(self.events)
        self.setCentralWidget(self.calendar)

        self.removeEventButton = QPushButton("Remove Event")
        # TODO: implement removing events
        self.toolbar.addWidget(self.removeEventButton)
        self.removeEventButton.clicked.connect(self.openRemoveEventGUI)

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

            self.events.insertEvent(self.newEventData['name'], self.newEventData['date'],
                                    self.newEventData['rigidity'], self.newEventData['location'])
        else:
            print("no event saved")
            pass

    def openRemoveEventGUI(self):
        # TODO: MAKE THIS WORK
        self.removeEventWindow = RemoveEventGUI()
        if self.removeEventWindow.exec():
            return self.removeEventWindow.getToBeRemovedAppointment()
        else:
            print("no event saved")
            pass
