from sqlite3 import IntegrityError

import pytest

from main import HabitTracker
from database import Database
from classes import Habit, HabitCompleted

class TestTracker:
    def setup_method(self):
        self.tracker = HabitTracker(storage = Database("test.db"))

    def test_tracker(self):
        new_habit = Habit("test_name", "test_definition", "daily")
        self.tracker.create(new_habit)
        assert new_habit in self.tracker.allHabits
        with pytest.raises(IntegrityError):
            self.tracker.create(new_habit)

    def teardown_method(self):
        import os
        os.remove("test.db")


