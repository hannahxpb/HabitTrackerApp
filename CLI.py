from sqlite3 import IntegrityError
from typing import Optional

import typer
from main import HabitTracker
from classes import Habit, HabitCompleted
from datetime import datetime
import json

app = typer.Typer()
ht = HabitTracker()

@app.command()
def show_allhabits():
    for h in ht.allHabits:
        print(h)

@app.command()
def show_alltrackedhabits():
    ht.completedHabits.sort()
    for h in ht.completedHabits:
        print(h)

@app.command()
def create_habit(name: str, definition: str, periodicity: str):
    new_habit = Habit(name = name, definition = definition, periodicity = periodicity)
    try:
        ht.create(new_habit)
        print(f"Habit {name}: {definition} with periodicity {periodicity} has been created")
    except IntegrityError:
        print("Habit with this name already exists.")

@app.command()
def complete_habit(name: str, date: Optional[str] = typer.Option(None, help="Default date for a completed habit is today")):
    try:
        print(ht.complete_habit(name, date))
    except ValueError:
        print("Invalid date format. Please enter the date in the following format: YYYY-MM-DD.")

@app.command()
def delete_habit(name: str):
    ht.delete(name)
    print(f"Habit {name} has been deleted")

@app.command()
def update_habit(name: str, definition: str, periodicity: str):
    ht.update(name, definition, periodicity)
    print(f"Habit {name} has been updated. \nUpdated definition: {definition}\nUpdated periodicity: {periodicity}")

@app.command()
def show_habit(name: str):
    print(f"The habit {name} has been completed on the following days: \n" + str(ht.get_habit(name)))

@app.command()
def show_habit_longeststreak(name: str):
    print(ht.get_longestrun_habit(name))

@app.command()
def show_habit_sameperiodicity(periodicity: str):
    print(f"The following habits have the periodicity {periodicity}: " + str(ht.get_habits_sameperiodicity(periodicity)))

@app.command()
def show_longeststreak_all():
    print(ht.get_longestrun_all())

@app.command()
def show_date(date: str):
    print(f"You have completed the following habits on the date {date}: \n" + str(ht.get_date(date)))

if __name__ == "__main__":
    app()

# def updateHabit(name: str, definition: str, periodicity: str = None):
#     pass