from PyQt6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
)
from PyQt6.QtCore import QDateTime


class AddEventGUI(QDialog):
    """
    GUI for when selecting to create a new event in the calendar.
    """

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
