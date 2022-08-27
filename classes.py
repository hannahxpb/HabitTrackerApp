from datetime import datetime, date
from enum import Enum

class Habit:
    def __str__(self):
        return f"{self.__class__.__name__}({self.name}: {self.definition} {self.periodicity.value})"

    def __init__(self, name, definition, periodicity):
        self.name = name
        self.definition = definition
        self.periodicity = Periodicity(periodicity)

class HabitCompleted:
    def __str__(self):
        return f"{self.__class__.__name__}({self.name} completed at: {self.date})"
    #

    def __init__(self, name, date: str = None):
        self.name = name
        if date is None:
            self.date = datetime.now().date()
        else:
            self.date = datetime.fromisoformat(date).date()
    # User can add completed habits later on - but if there's no date given, the date will automatically be set to today

    def __lt__(self, other):
        """
        Allows sorting by date, less than
        Parameters
        ----------
        other

        Returns
        -------

        """
        if self.date < other.date:
            return True
        else:
            return False

class Periodicity(str, Enum):
    Daily = "daily"
    Weekly = "weekly"

period_map = {
    Periodicity.Daily: 1,
    Periodicity.Weekly: 7
}











