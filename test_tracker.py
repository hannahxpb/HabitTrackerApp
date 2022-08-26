import datetime
from sqlite3 import IntegrityError
import pytest
from main import HabitTracker
from database import Database
from classes import Habit, HabitCompleted

class TestTracker:
    def setup_method(self):
        self.tracker = HabitTracker(storage = Database("test.db"))

    def test_create(self):
        new_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(new_habit)
        assert new_habit in self.tracker.allHabits
        with pytest.raises(IntegrityError):
            self.tracker.create(new_habit)
        # Raise IntegrityError if new_habit already exists

        with pytest.raises(ValueError):
            bad_habit = Habit("test_name2", "test_definition2", "biweekly")

    def test_complete(self):
        new_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(new_habit)
        self.tracker.complete_habit("test_name")
        assert len(self.tracker.completedHabits) > 0
        # Assert that length of completedHabits > 0 after completing a habit
        completed = self.tracker.completedHabits[0]
        assert completed.name == "test_name"
        assert completed.date == datetime.datetime.now().date()
        # Assert that name and date of the completed habit are indeed the test_name and todays date

        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        self.tracker.complete_habit("test_name", yesterday.isoformat())
        assert len(self.tracker.completedHabits) == 2
        # Create a completed habit for yesterday and check length of completedHabits again

        completed1 = self.tracker.completedHabits[1]
        assert completed1.date == yesterday
        # Assert that the date of the completed habit is indeed yesterday

    def test_complete_brokenstreak(self):
        new_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(new_habit)
        self.tracker.complete_habit("test_name")
        before_yesterday = datetime.datetime.now().date() - datetime.timedelta(days=2)
        assert self.tracker.complete_habit("test_name", before_yesterday.isoformat()) == "Your previous streak was lost. Habit test_name has been completed for today."
        # Create 2 completed habits to see if the return value indicates that the streak was lost

    def test_delete(self):
        new_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(new_habit)
        self.tracker.complete_habit("test_name")
        assert len(self.tracker.completedHabits) == 1
        # Assert that the length of the completedHabits list is 1 after creating and completing the habit
        self.tracker.delete("test_name")
        assert len(self.tracker.completedHabits) == 0
        # Assert that the length of the completedHabits list is 1 after deleting the habit

    def test_streak(self):
        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        completed1 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        completed2 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        completed3 = self.tracker.complete_habit("test_name")
        complete_habits = []
        complete_habits.append(completed1)
        complete_habits.append(completed2)
        complete_habits.append(completed3)
        assert self.tracker.get_longestrun_habit("test_name") == 2

    def test_date(self):
        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        completed1 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        assert len(self.tracker.get_date("2022-08-24")) == 1
        # Assert that the length of the output list is 1 (contains completed1 object)

    def test_longeststreak(self):
        yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
        habit1 = Habit("name1", "definition", "daily")
        self.tracker.create(habit1)
        habit2 = Habit("name2", "definition", "daily")
        self.tracker.create(habit2)
        self.tracker.complete_habit("name1")
        self.tracker.complete_habit("name1", yesterday.isoformat())
        self.tracker.complete_habit("name2")
        self.tracker.complete_habit("name2", yesterday.isoformat())
        assert len(self.tracker.get_longestrun_all()[0]) == 2
        # Assert that the length of the first list entry is 2 (both habits name1 and name2)
        assert self.tracker.get_longestrun_all()[1] == 2
        # Assert that the second list entry is 2 (2 day streak)

    def test_update(self):
        habit1 = Habit("test_name", "test_definition", "test_periodicity")
        self.tracker.create(habit1)
        habit1 = self.tracker.update("test_name", "test_definition2", "test_periodicity")
        assert habit1.definition == "test_definition2"

    def teardown_method(self):
        import os
        os.remove("test.db")


