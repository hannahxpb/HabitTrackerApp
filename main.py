from typing import List
from datetime import datetime, timedelta
from database import Database
from classes import Habit, Periodicity, HabitCompleted


class HabitTracker:
    def __init__(self):
        self.storage = Database()
        self.allHabits: List[Habit] = self.storage.get_allhabits()
        self.completedHabits = self.storage.get_alltrackedhabits()

    def complete_habit(self, name: str):
        completed_habit = HabitCompleted(name)
        self.storage.add_completedhabit(completed_habit.name, completed_habit.date)
        self.completedHabits.append(completed_habit)

    def delete(self, name: str):
        self.storage.delete_habit(name)
        for habit in self.allHabits:
            if habit.name == name:
                self.allHabits.remove(habit)

    def create(self, new_habit: Habit):
        self.storage.store_habit(new_habit.name, new_habit.definition, new_habit.periodicity)
        self.allHabits.append(new_habit)

    def select_habit(self, name: str):
        print(self.storage.select_habit(name))

    def select_habit_streak(self, name: str):
        # Sort list of completed habits
        # Looping through the list of completed habits
        # Using timedelta to compare list elements (if equal or less than one day, add to streak)
        dates = self.storage.select_habit_streak(name)
        dates.sort()
        consecutive_days = [dates[0]]
        for i in range(1, len(dates)):
            if (dates[i].date - dates[i-1].date).days == 1:
                consecutive_days.append(i)
        print(len(consecutive_days))

    # def get_date(self, date: ):
    #     pass

    # def update(self, habit):
    #     pass
    #
    # def get_habitsSamePeriodicity(self, habits):
    #     pass
    #
    # def get_longestStreakRunAll(self, habits):
    #     pass
    #

#
# workout = Habit("Workout", "Workout done", Periodicity.Daily)
# steps = Habit("Steps", "More than 3,000 steps", Periodicity.Daily)
# water = Habit("Water", "Drinking at leats 2l of water", Periodicity.Daily)
# sleep = Habit("Sleep", "Sleeping at least 7h", Periodicity.Daily)
# stretching = Habit("Streching", "Stretching done", Periodicity.Weekly)













