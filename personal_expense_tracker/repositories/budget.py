import sqlite3
from typing import List, Dict, Any

class BudgetRepository:
    def __init__(self, db_path: str, month: str, year: int):
        """
        Initialize the BudgetRepository with a database path, month, and year.
        :param db_path: Path to the SQLite database file.
        """
        self.month = month
        self.year = year
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self._create_budget_table(self.month, self.year)

    def _create_budget_table(self, month: str, year: int):
        """
        Create the budget table if it doesn't exist.
        """
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budget (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month VARCHAR(9) NOT NULL,
                    year INTEGER NOT NULL,
                    budget INTEGER NOT NULL,
                    expenditure INTEGER NOT NULL,
                    remaining INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()

    def update_budget(self, month: str, year: int, budget: float):
        """
        Update the budget for a specific month and year.
        """
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE budget
                SET budget = ?
                WHERE month = ? AND year = ?
            ''', (budget, month, year))
            self.connection.commit()
