import sqlite3
# from typing import List, Dict, Any


class BudgetRepository:
    def __init__(self, db_path: str, month: str, year: int):
        """
        Initialize the BudgetRepository with a database path, month, and year.
        :param db_path: Path to the SQLite database file.
        """
        self.month = month
        self.year = year
        self.db_path = db_path
        self._create_budget_table(month, year)

    def _create_budget_table(self, month: str, year: int):
        """
        Create the budget table if it doesn't exist.
        :param month: Month to create the budget for.
        :param year: Year to create the budget for.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS budget (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month VARCHAR(9) NOT NULL,
                    year INTEGER NOT NULL,
                    current_budget INTEGER NOT NULL,
                    expenditure INTEGER NOT NULL,
                    remaining INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            cursor.execute(
                """
                INSERT OR IGNORE INTO budget (month, year, current_budget, expenditure, remaining)
                VALUES (?, ?, ?, ?, ?)
                """,
                (month, year, 0, 0, 0),
            )
            conn.commit()

    def get_budget(self, month: str, year: int) -> int:
        """
        Get the budget for a specific month and year.
        :param month: Month to get the budget for.
        :param year: Year to get the budget for.
        :return: Budget amount.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT current_budget FROM budget
                WHERE month = ? AND year = ?
            """,
                (month, year),
            )
            conn.commit()
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_expenditure(self, month: str, year: int) -> int:
        """
        Get the expenditure for a specific month and year.
        :param month: Month to get the expenditure for.
        :param year: Year to get the expenditure for.
        :return: Expenditure amount.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT expenditure FROM budget
                WHERE month = ? AND year = ?
            """,
                (month, year),
            )
            conn.commit()
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_remaining(self, month: str, year: int) -> int:
        """
        Get the remaining budget for a specific month and year.
        :param month: Month to get the remaining budget for.
        :param year: Year to get the remaining budget for.
        :return: Remaining budget amount.
        """
        result = None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT remaining FROM budget
                WHERE month = ? AND year = ?
            """,
                (month, year),
            )
            conn.commit()
            result = cursor.fetchone()
            return result[0] if result else 0

    def update_budget(self, month: str, year: int, new_budget: int):
        """
        Update the budget for a specific month and year.
        :param month: Month to update the budget for.
        :param year: Year to update the budget for.
        :param budget: New budget amount.
        """
        expenditure = self.get_expenditure(month, year)
        remaining = new_budget - expenditure

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE budget
                SET current_budget = ?, remaining = ?, updated_at = CURRENT_TIMESTAMP
                WHERE month = ? AND year = ?
            """,
                (new_budget, remaining, month, year),
            )
            conn.commit()
