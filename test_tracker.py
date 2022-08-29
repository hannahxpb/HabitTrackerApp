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

    def test_delete(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        self.tracker.complete_habit("test_name")
        assert len(self.tracker.completedHabits) == 1
        # Assert that the length of the completedHabits list is 1 after creating and completing the habit
        self.tracker.delete("test_name")
        assert len(self.tracker.completedHabits) == 0
        # Assert that the length of the completedHabits list is 1 after deleting the habit

    def test_update(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        test_habit = self.tracker.update("test_name", "test_definition2", "daily")
        assert test_habit.definition == "test_definition2"

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

    def test_completehabit_today(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        today = datetime.datetime.now().date()
        habit_name, habit_date = self.tracker.complete_habit("test_name")
        assert habit_date == today

    def test_complete_badhabit(self):
        with pytest.raises(ValueError):
            # Assert that a habit that wasn't created cannot be completed
            self.tracker.complete_habit("bad_habit")


    def test_allstreaks(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        self.tracker.complete_habit("test_name", yesterday.isoformat())
        self.tracker.complete_habit("test_name")
        assert self.tracker.find_allstreaks("test_name")

    def test_complete_twobrokenstreaks(self):
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

        consec_period, start, end = self.tracker.get_longeststreak_habit("test_name")
        assert consec_period == 4
        assert end > start

    def test_streak_specific(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
        completed1 = self.tracker.complete_habit("test_name")
        completed2 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        consec_period, start_date, end_date = self.tracker.get_longeststreak_habit("test_name")
        assert consec_period == 2
        assert start_date < end_date

    def test_streak_specific_sameday(self):
        # Create two objects for the same day to check that only one of them is counted for the streak
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        completed1 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        completed2 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        consec_period, start_date, end_date = self.tracker.get_longeststreak_habit("test_name")
        assert consec_period == 1

    def test_longeststreakall(self):
        yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
        test_habit1 = Habit("name1", "definition", "daily")
        self.tracker.create(test_habit1)
        test_habit2 = Habit("name2", "definition", "daily")
        self.tracker.create(test_habit2)
        self.tracker.complete_habit("name1")
        self.tracker.complete_habit("name1", yesterday.isoformat())
        self.tracker.complete_habit("name2")
        self.tracker.complete_habit("name2", yesterday.isoformat())
        habits, streak = self.tracker.get_longeststreak_all()
        assert streak == 2
        # Assert that the length of the streak is 2
        assert len(habits) == 2
        # Assert that the length the habit entry is 2 (both habits name1 and name2)

    def test_streak_weekly(self):
        test_habit = Habit("test_name", "test_definition", "weekly")
        self.tracker.create(test_habit)
        onemonthago = datetime.datetime.now().date() - datetime.timedelta(weeks=4)
        for i in range(2):
            date = onemonthago + datetime.timedelta(weeks=i)
            self.tracker.complete_habit("test_name", date.isoformat())
        consec_period, start_date, end_date = self.tracker.get_longeststreak_habit("test_name")
        assert consec_period == 2
        assert start_date < end_date

    def test_getdate(self):
        test_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(test_habit)
        yesterday = datetime.datetime.now().date()-datetime.timedelta(days=1)
        completed1 = self.tracker.complete_habit("test_name", yesterday.isoformat())
        assert len(self.tracker.get_date(yesterday.isoformat())) == 1
        # Assert that the length of the output list is 1 (contains completed1 object)

    def teardown_method(self):
        import os
        os.remove("test.db")


