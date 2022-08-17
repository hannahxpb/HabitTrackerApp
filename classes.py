from datetime import datetime
from enum import Enum

class Habit:
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}: {self.definition} {self.periodicity})"

    def __init__(self, name, definition, periodicity):
        self.name = name
        self.definition = definition
        self.periodicity = periodicity

class HabitCompleted:
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name} completed at: {self.date})"

    def __init__(self, name, date = None):
        self.name = name
        if date is None:
            self.date = datetime.now().date()
        else:
            self.date = datetime.fromisoformat(date)

    def __lt__(self, other):
        if self.date < other.date:
            return True
        else:
            return False

class Periodicity(str, Enum):
    Daily = "daily"
    Weekly = "weekly"
    Monthly = "monthly"

# workout = Habit("Workout", "Workout done", Periodicity.Daily)
# steps = Habit("Steps", "More than 3,000 steps", Periodicity.Daily)
# water = Habit("Water", "Drinking at leats 2l of water", Periodicity.Daily)
# sleep = Habit("Sleep", "Sleeping at least 7h", Periodicity.Daily)
# stretching = Habit("Streching", "Stretching done", Periodicity.Weekly)













