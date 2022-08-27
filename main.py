import logging
import math
from sqlite3 import IntegrityError
from typing import List
from datetime import datetime, timedelta
from database import Database
from classes import Habit, Periodicity, HabitCompleted, period_map

DB_DEFAULT_NAME = "database.db"


class HabitTracker:
    def __init__(self, storage = None):
        self.storage = storage or Database(DB_DEFAULT_NAME)
        #
        self.allHabits: List[Habit] = self.storage.get_allhabits()
        self.completedHabits = self.storage.get_alltrackedhabits()

    def create(self, new_habit: Habit):
        """
        Creates a new habit.

        Parameters
        ----------
        new_habit
            habit object or something

        Returns
        -------

        """
        self.storage.store_habit(new_habit.name, new_habit.definition, new_habit.periodicity.value)
        self.allHabits.append(new_habit)

    def complete_habit(self, name: str, date: str = None):
        completed_habit = HabitCompleted(name, date=date)

        try:
            self.storage.complete_habit(completed_habit.name, completed_habit.date)
            self.completedHabits.append(completed_habit)
        except IntegrityError:
            raise ValueError("Please create a habit before completing it.")

        dates = self.storage.get_habitstreak(name)
        dates.sort()

        if completed_habit.date == None:
            if len(dates) >= 2:
                last_entry = dates[-2]
                if abs((completed_habit.date - last_entry.date)).days >= 2:
                    return f"Your previous streak was lost. Habit {completed_habit.name} has been completed for today."

        else:
            return f"Habit {completed_habit.name} has been completed for {completed_habit.date}."

    def delete(self, name: str):
        self.storage.delete_habit(name)
        self.allHabits: List[Habit] = self.storage.get_allhabits()
        self.completedHabits = self.storage.get_alltrackedhabits()

    def update(self, name: str, definition: str, periodicity: str) -> Habit:
        self.storage.update_habit(name, definition, periodicity)
        self.allHabits: List[Habit] = self.storage.get_allhabits()
        for h in self.allHabits:
            if h.name == name:
                return h

    def get_habit(self, name: str):
        habits_completed = self.storage.get_completedhabit(name)
        habits_completed.sort()
        return habits_completed

    def get_longestrun_habit(self, name: str):
        # Sort list of completed habits
        # Looping through the list of completed habits
        # Using .days to compare list elements (if equal or less than one day, add to streak)
        dates = self.storage.get_habitstreak(name)
        dates.sort()
        consecutive_period = 0
        longest_streak = 0

        streak_period = None
        for i in self.allHabits:
            if i.name == name:
                streak_period = period_map[i.periodicity]
                break

        start_longeststreak = None
        end_longeststreak = None
        start_streak = None
        end_streak = None
        longest_streak = 0
        for i in range (1, len(dates)):
            first_entry = dates[i-1]
            second_entry = dates[i]
            start_streak = start_streak or first_entry

            if abs((first_entry.date - second_entry.date).days) <= streak_period:
                end_streak = second_entry
            else:
                # Reset next streak
                start_streak = second_entry
                end_streak = start_streak

            # Check if this was the longest streak and store in that case
            consecutive_period = (end_streak.date-start_streak.date).days
            if consecutive_period > longest_streak:
                start_longeststreak = start_streak
                end_longeststreak = end_streak
                longest_streak = consecutive_period

        print(f"The longest streak began on {start_longeststreak.date} and ended on {end_longeststreak.date}")
        return math.ceil((longest_streak+1) / streak_period)

    def get_longestrun_all(self):
        max_streak = 0
        longest_streak = []
        for h in self.allHabits:
            streak = self.get_longestrun_habit(h.name)
            if streak > max_streak:
                max_streak = streak
                longest_streak = [h.name]
            # [h.name] clears the list and adds the name of the habit if there have been other entries
            elif streak == max_streak:
                longest_streak.append(h.name)
            # .append(h.name) appends the name, so that other names will remain in the list
        return longest_streak, max_streak

    def get_habits_sameperiodicity(self, periodicity: str):
        return self.storage.get_sameperiodicity(periodicity)

    def get_date(self, date: str):
        return self.storage.select_date(date)
















