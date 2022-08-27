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
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        assert test_habit in self.tracker.allHabits
        with pytest.raises(IntegrityError):
            self.tracker.create(test_habit)
        # Raise IntegrityError if test_habit already exists

        with pytest.raises(ValueError):
            bad_habit = Habit("test_name2", "test_definition2", "biweekly")

    def test_complete(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
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

    def test_complete_badhabit(self):
        with pytest.raises(ValueError):
            # Assert that a habit that wasn't created cannot be completed
            self.tracker.complete_habit("bad_habit")

    def test_completehabit_today(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        today = datetime.datetime.now().date()
        assert self.tracker.complete_habit("test_name") == f"Habit test_name has been completed for {today.isoformat()}."
        # Assert that the return value for a complete habit contains the name & date

    def test_complete_brokenstreak(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        self.tracker.complete_habit("test_name")
        before_yesterday = datetime.datetime.now().date() - datetime.timedelta(days=2)
        assert self.tracker.complete_habit("test_name", before_yesterday.isoformat()) == "Habit test_name has been completed for 2022-08-25."
        # Create 2 completed habits with 2 days apart to see if the return value indicates that the streak was lost

    def test_twobrokenstreaks(self):
        twoweeksago = datetime.datetime.now().date() - datetime.timedelta(weeks=2)
        oneweekago = datetime.datetime.now().date() - datetime.timedelta(weeks=1)
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        for i in range(4):
            date = twoweeksago + datetime.timedelta(days=i)
            self.tracker.complete_habit("test_name", date.isoformat())

        for i in range(3):
            date = oneweekago + datetime.timedelta(days=i)
            self.tracker.complete_habit("test_name", date.isoformat())

        assert self.tracker.get_longestrun_habit("test_name") == 4

    def test_delete(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        self.tracker.complete_habit("test_name")
        assert len(self.tracker.completedHabits) == 1
        # Assert that the length of the completedHabits list is 1 after creating and completing the habit
        self.tracker.delete("test_name")
        assert len(self.tracker.completedHabits) == 0
        # Assert that the length of the completedHabits list is 1 after deleting the habit

    def test_streak(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        completed1 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        completed2 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        # Create two objects for the same day to check if only one of them is counted for the streak
        completed3 = self.tracker.complete_habit("test_name")
        complete_habits = []
        complete_habits.append(completed1)
        complete_habits.append(completed2)
        complete_habits.append(completed3)
        assert self.tracker.get_longestrun_habit("test_name") == 2

    def test_date(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        completed1 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        assert len(self.tracker.get_date(yesterday.isoformat())) == 1
        # Assert that the length of the output list is 1 (contains completed1 object)

    def test_longeststreak(self):
        yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
        test_habit1 = Habit("name1", "definition", "daily")
        self.tracker.create(test_habit1)
        test_habit2 = Habit("name2", "definition", "daily")
        self.tracker.create(test_habit2)
        self.tracker.complete_habit("name1")
        self.tracker.complete_habit("name1", yesterday.isoformat())
        self.tracker.complete_habit("name2")
        self.tracker.complete_habit("name2", yesterday.isoformat())
        assert len(self.tracker.get_longestrun_all()[0]) == 2
        # Assert that the length of the first list entry is 2 (both habits name1 and name2)
        assert self.tracker.get_longestrun_all()[1] == 2
        # Assert that the second list entry is 2 (2 day streak)

    def test_update(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        test_habit = self.tracker.update("test_name", "test_definition2", "daily")
        assert test_habit.definition == "test_definition2"

    def test_weekly(self):
        test_habit = Habit("test_name", "test_definition", "weekly")
        self.tracker.create(test_habit)
        onemonthago = datetime.datetime.now().date() - datetime.timedelta(weeks=4)

        for i in range(2):
            date = onemonthago + datetime.timedelta(weeks=i)
            self.tracker.complete_habit("test_name", date.isoformat())

        assert self.tracker.get_longestrun_habit("test_name") == 2

    def teardown_method(self):
        import os
        os.remove("test.db")


