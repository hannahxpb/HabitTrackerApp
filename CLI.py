from sqlite3 import IntegrityError
import typer
from main import HabitTracker
from classes import Habit, HabitCompleted

app = typer.Typer()
ht = HabitTracker()

@app.command()
def list_allhabits():
    for h in ht.allHabits:
        print(h)

@app.command()
def list_alltrackedhabits():
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
def completeHabit(name: str):
    ht.complete_habit(name)
    print(f"Habit {name} has been completed for today")

@app.command()
def delete_habit(name: str):
    ht.delete(name)
    print(f"Habit {name} has been deleted")

@app.command()
def show_specific(name: str):
    ht.select_habit(name)

@app.command()
def show_specific_streak(name: str):
    ht.select_habit_streak(name)

if __name__ == "__main__":
    app()

# def updateHabit(name: str, definition: str, periodicity: str = None):
#     pass