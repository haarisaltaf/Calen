import sqlite3
from datetime import datetime
import logging


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
        self.con = sqlite3.connect(
            "database/events.db")  # connects to database
        self.cur = self.con.cursor()  # allows SQL executions
        if (self.checkTables() is []):
            print("Attempting creation")
            logging.warning(
                "No previous Tables found, attempting creation of new")
            self.initialCreation()

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
            (eventName, eventDate, rigidity, location,)
        )
        self.con.commit()  # commit allows for the changes to persist after closure

    def checkTables(self):
        """
        Grabs ALL table names from sqlite_master, returned using .fetchall()
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cur.fetchall()

    def deleteEvent(self, eventName="test"):
        """
        Deletes an event based on the passed through parameter.
        """
        self.cur.execute("DELETE FROM Events WHERE name = ?", (eventName,))

    def fetchDayEvents(self, date):
        self.cur.execute(
            "SELECT * FROM Events WHERE date LIKE ?", (f"%{date}%",))
        dayEvents = self.cur.fetchall()
        return dayEvents

    def fetchAllEvents(self):
        try:
            self.cur.execute("SELECT * FROM Events")
            rows = self.cur.fetchall()
            return rows
        except sqlite3.OperationalError:
            logging.warning("No previous events created.")
            return None

    def close(self):
        self.cur.close()


def formatGetAllEvents(allEvents):
    """
    Formats all events based on the sqlite exection (SELECT * FROM events)
    FOR QComboBox.
    """
    # TODO: need to finishthis fucntion -- Formatting -- CHANGE TO JUST FORMAT 1 PASSED-THROUGH DAY's EVENTS - save resources
    print("PREFORMATTED:",  allEvents)
    # Example of preformatting:
    # [('Revision', '17-08-2025', 'Rigid', 'Laidlaw Library'), ('Laidlaw With Time', '17-08-2025 23:36', 'Rigid', 'Laidlawlianrur')]
