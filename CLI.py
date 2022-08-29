from sqlite3 import IntegrityError
from typing import Optional

import typer
from main import HabitTracker
from classes import Habit, Periodicity
from rich import print

app = typer.Typer()
ht = HabitTracker()

@app.command()
def create_habit(name: str, definition: str, periodicity: Periodicity):
    """
    Creates a new habit. Requires all 3 arguments: name, definition and periodicity.
    For the periodicity, you can choose between "daily" or "weekly".
    """
    new_habit = Habit(name = name, definition = definition, periodicity = periodicity)
    try:
        ht.create(new_habit)
        print(f"Habit {name}: {definition} with periodicity {periodicity} has been created.")
    except IntegrityError:
        print("Habit with this name already exists.")

@app.command()
def complete_habit(name: str, date: Optional[str] = typer.Option(None, help="Default date for a completed habit is today")):
    """
    Completes a habit. A habit needs to be created before it can be completed.
    Requires name as an argument. The date is optional, the default is today.
    State both the name and the date to add completed habits later on.
    """
    try:
        name, date = ht.complete_habit(name, date)
        print(f"The habit {name} was completed on the {date}.")
    except ValueError:
        print("Invalid date format. Please enter the date in the following format: YYYY-MM-DD.")

@app.command()
def delete_habit(name: str):
    """
    Deletes a habit. Requires name as an argument.
    """
    ht.delete(name)
    print(f"Habit {name} has been deleted.")

@app.command()
def update_habit(name: str, definition: str, periodicity: str):
    """
    Updates the definition and/or periodicity of a habit.
    Requires all 3 arguments: name, definition and periodicity.
    State the name of the habit you want to update and both the definition and periodicity including the update.
    """
    ht.update(name, definition, periodicity)
    print(f"Habit {name} has been updated. \nUpdated definition: {definition}\nUpdated periodicity: {periodicity}")

@app.command()
def show_allhabits():
    """
    Shows all habits.
    """
    for h in ht.allHabits:
        print(h)

@app.command()
def show_alltrackedhabits():
    """
    Shows all tracked habits and their completions.
    """
    ht.completedHabits.sort()
    for h in ht.completedHabits:
        print(h)

@app.command()
def show_completions(name: str):
    """
    Shows the completions of a habit. Requires the name of the habit as an argument.
    """
    completions = ht.get_habitcompletions(name)
    print(f"The habit {name} has been completed on the following days: \n{completions}")

@app.command()
def show_allstreaks_habit(name: str):
    """
    Shows all streaks of a habit. Requires the name of the habit as an argument.
    """
    periodicity = ht.get_streakperiod(name)
    streaks = ht.find_allstreaks(name)
    if periodicity == 1:
        for start, end, length in streaks:
            print(f"Streak of {length} days from {start.date} to {end.date}.")
    elif periodicity == 7:
        for start, end, length in streaks:
            print(f"Streak of {length} weeks from {start.date} to {end.date}.")

@app.command()
def show_habit_longeststreak(name: str):
    """
    Shows the longest streak of a habit. Requires the name of the habit as an argument.
    """
    periodicity = ht.get_streakperiod(name)
    consec_period, start, end = ht.get_longeststreak_habit(name)
    if periodicity == 1:
        print(f"Your longest streak is from {start} to {end}. Your longest streak is: {consec_period} days.")
    elif periodicity == 7:
        print(f"Your longest streak is from {start} to {end}. Your longest streak is: {consec_period} weeks.")

@app.command()
def show_habit_sameperiodicity(periodicity: Periodicity):
    """
    Shows all habits with the same periodicity.
    For the periodicity, you can choose between "daily" or "weekly".
    """
    habits = ht.get_habits_sameperiodicity(periodicity)
    print(f"The following habits have the periodicity {periodicity}: {habits}")

@app.command()
def show_longeststreak_all():
    """
    Shows the longest streak run out of all habits.
    """
    habits, streak = ht.get_longeststreak_all()
    print(f"The following habit(s) have the longest streak of {streak} times:\n{habits}")

@app.command()
def show_date(date: str):
    """
    Shows all completions for one specific date. Requires the date as an argument.
    Enter the date as follows: "YYYY-MM-DD"
    """
    completions = ht.get_date(date)
    print(f"You have completed the following habits on the date {date}: \n{completions}")

if __name__ == "__main__":
    app()
