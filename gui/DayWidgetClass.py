from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QDockWidget,
)
from PyQt6.QtCore import Qt


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
