from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QVBoxLayout,
    QLabel,
)
from database.EventsClass import formatGetAllEvents


class RemoveEventGUI(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Remove Event")

        self.layout = QVBoxLayout()

        # get all items and list them
        # TODO: CHANGE TO SERVICE -> ask for date in dropdown then upon selection, get the events for that date.

        # self.con = sqlite3.connect("events.db")  # connects to database
        # self.cur = self.con.cursor()  # allows SQL executions
        # self.cur.execute("SELECT * FROM events")
        # self.allEvents = self.cur.fetchall()
        self.formattedEvents = formatGetAllEvents(self.allEvents)
        self.cur.close()

        self.layout.addWidget(QLabel("Select event to remove:"))
        self.removeEventSelector = QComboBox()
        # self.removeEventSelector.addItems(self.allEvents)
        # TODO: conect this to update the qcombobox events to update based on the selected date
        self.removeEventSelector.currentTextChanged.connect()

        self.layout.addWidget(self.removeEventSelector)

        self.setLayout(self.layout)

    def getToBeRemovedAppointment(self):
        self.currentSelection = self.removeEventSelector.currentText()
        return self.currentSelection
