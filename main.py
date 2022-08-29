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
        new_habit object: name, definition, periodicity
        """
        self.storage.store_habit(new_habit.name, new_habit.definition, new_habit.periodicity.value)
        self.allHabits.append(new_habit)

    def delete(self, name: str):
        self.storage.delete_habit(name)
        self.allHabits: List[Habit] = self.storage.get_allhabits()
        self.completedHabits = self.storage.get_alltrackedhabits()

    def update(self, name: str, definition: str, periodicity: str) -> Habit:
        """
        Updates the definition and periodicity of a given habit.
        """
        self.storage.update_habit(name, definition, periodicity)
        self.allHabits: List[Habit] = self.storage.get_allhabits()
        for h in self.allHabits:
            if h.name == name:
                return h

    def complete_habit(self, name: str, date: str = None):
        """
        Completes a habit that was created. The date is optional - default is today.
        """
        completed_habit = HabitCompleted(name, date=date)

        try:
            self.storage.complete_habit(completed_habit.name, completed_habit.date)
            self.completedHabits.append(completed_habit)

        except IntegrityError:
            raise ValueError("Please create a habit before completing it.")

        current_streak = (self.is_current_streak_active(completed_habit))

        return completed_habit.name, completed_habit.date, current_streak

    def find_allstreaks(self, habit_name, streak_period)->list:
        """
        Finds all streaks and can be used in other functions (f.e. to establish current or longest streaks)
        Returns a list of all streaks.
        """
        dates = self.storage.get_completedhabits(habit_name)
        start_streak = None
        end_streak = None
        streak_list = []
        for i in range(1, len(dates)):
            first_entry = dates[i - 1]
            second_entry = dates[i]
            start_streak = start_streak or first_entry

            if abs((first_entry.date - second_entry.date).days) <= streak_period:
                end_streak = second_entry
            else:
                streak_length = math.ceil((end_streak.date - start_streak.date).days/streak_period)+1
                streak_list.append((start_streak, end_streak, streak_length))
                # Reset next streak
                start_streak = second_entry
                end_streak = start_streak

        return streak_list

    def is_current_streak_active(self, completed_habit)->int:
        """
        Determines the length of the current streak
        Returns: int
        """
        streak_period = None
        for i in self.allHabits:
            if i.name == completed_habit.name:
                streak_period = period_map[i.periodicity]
                break
        # Get the periodicity of the completed habit

        today = datetime.now().date()

        all_streaks = self.find_allstreaks(completed_habit.name, streak_period)
        if not all_streaks:
            return 0
        latest_streak = max(all_streaks, key = lambda i: i[2])
        # Returns the max value of the 3. element of the latest_streak list which is the end date of the last streak
        start, end, length = latest_streak

        if abs((today - end.date).days) <= streak_period:
            return length

    def get_habitcompletions(self, name: str):
        habits_completed = self.storage.get_completedhabit(name)
        habits_completed.sort()
        return habits_completed

    def get_longeststreak_habit(self, name: str):
        dates = self.storage.get_completedhabits(name)
        if len(dates) < 1:
            return None, None, None

        streak_period = None
        for i in self.allHabits:
            if i.name == name:
                streak_period = period_map[i.periodicity]
                break

        all_streaks = self.find_allstreaks(name, streak_period)
        if len(all_streaks) < 1:
            return None, None, None
        def get_streak_length(streak):
            return streak[2]
        longest_streak = max(all_streaks, key=get_streak_length)
        start, end, streak_length = longest_streak

        return streak_length, start.date, end.date
        # Returning the longest consecutive period in either days or weeks, depending on the periodicity

    def get_longeststreak_all(self):
        max_streak = 0
        longest_streak_habits = []
        for h in self.allHabits:
            streak, *_ = self.get_longeststreak_habit(h.name)
            if streak == None:
                continue
            # because the return value of the get_longestrun_habit is a tuple and only the longest streak run is needed
            if streak > max_streak:
                max_streak = streak
                longest_streak_habits = [h.name]
            # [h.name] clears the list and adds the name of the habit if there have been other entries
            elif streak == max_streak:
                longest_streak_habits.append(h.name)
            # .append(h.name) appends the name, so that other names will remain in the list
        return longest_streak_habits, max_streak

    def get_habits_sameperiodicity(self, periodicity: str):
        return self.storage.get_sameperiodicity(periodicity)

    def get_date(self, date: str):
        return self.storage.select_date(date)
















