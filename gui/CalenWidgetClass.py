from PyQt6.QtWidgets import (
    QCalendarWidget,
)
from PyQt6.QtCore import Qt
from gui.DayWidgetClass import DayWidget
import logging
from database.EventsClass import Events


class CalenWidget(QCalendarWidget):
    def __init__(self, parent=None, events=Events()):
        super(CalenWidget, self).__init__()
        self.clicked.connect(self.onClickedDate)
        self.events = events
        if events is None:
            logging.critical(
                "CalenWidget has recieced 'None' as its events, continuing with none")

    def onClickedDate(self, date):
        self.selectedDay = date.toString("dd-MM-yyyy")
        rows = self.events.fetchDayEvents(date=self.selectedDay)
        currentDayDockWidget = DayWidget(date, str(rows))

        self.parent().addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                                    currentDayDockWidget)
