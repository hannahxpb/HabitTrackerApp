import datetime
import sqlite3
from typing import List
from classes import Habit, HabitCompleted

class Database:
    def __init__(self, name="database.db"):
        self.database = sqlite3.connect(name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.database.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""CREATE TABLE IF NOT EXISTS habit(
            name TEXT PRIMARY KEY,
            definition TEXT,
            periodicity TEXT)""")
    
        cursor.execute("""CREATE TABLE IF NOT EXISTS habitCompleted(
            date TEXT,
            habitName TEXT,
            FOREIGN KEY (habitName) REFERENCES habit(name)
            )""")
    
        self.database.commit()
    
    def store_habit(self, name, definition, periodicity):
        cursor = self.database.cursor()
        cursor.execute("INSERT INTO habit VALUES (?, ?, ?)", (name, definition, periodicity))
        self.database.commit()
    
    def get_allhabits(self) -> List[Habit]:
        cursor = self.database.cursor()
        cursor.execute("SELECT name, definition, periodicity FROM habit")
        list_of_tuples = cursor.fetchall()
        list_of_habits = []
        for (name, definition, periodicity) in list_of_tuples:
            habit = Habit(name, definition, periodicity)
            list_of_habits.append(habit)
            # Converting the output to a list (instead of a tuple)
        return list_of_habits

    def get_alltrackedhabits(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT habitName, date FROM habitCompleted")
        list_of_tuples = cursor.fetchall()
        list_of_habits = []
        for (name, date) in list_of_tuples:
            hc = HabitCompleted(name, date)
            list_of_habits.append(hc)
            # Converting the output to a list (instead of a tuple)
        return list_of_habits

    def delete_habit(self, name: str):
        cursor = self.database.cursor()
        cursor.execute("DELETE FROM habitCompleted where habitName = ?", (name,))
        cursor.execute("DELETE FROM habit WHERE name = ?", (name, ))
        self.database.commit()

    def complete_habit(self, habitName, date = None):
        cursor = self.database.cursor()
        if date is None:
            date = datetime.date.today().isoformat()
        cursor.execute("INSERT INTO habitCompleted VALUES (?, ?)", (date, habitName))
        self.database.commit()

    def update_habit(self, name: str, definition: str, periodicity: str):
        cursor = self.database.cursor()
        cursor.execute("UPDATE habit SET definition = :definition, periodicity = :periodicity WHERE name = :name",
                        dict(name=name, definition=definition, periodicity=periodicity))
        self.database.commit()
        modified_rows = cursor.rowcount
        if modified_rows == 0:
            raise Exception(f"Could not find name: {name}")

    def get_completedhabit(self, habitName):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM habitCompleted WHERE habitName=?", (habitName, ))
        return cursor.fetchall()

    def get_completedhabits(self, habitName):
        cursor = self.database.cursor()
        cursor.execute("SELECT habitName, date FROM habitCompleted WHERE habitName=?", (habitName, ))
        list_of_tuples = cursor.fetchall()
        list_of_habits = []
        for (name, date) in list_of_tuples:
            h = HabitCompleted(name, date)
            list_of_habits.append(h)
        return list_of_habits

    def get_sameperiodicity(self, periodicity):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM habit WHERE periodicity=?", (periodicity, ))
        return cursor.fetchall()

    def select_date(self, date):
        cursor = self.database.cursor()
        cursor.execute("SELECT date, habitName FROM habitCompleted WHERE date=?", (date, ))
        return cursor.fetchall()
