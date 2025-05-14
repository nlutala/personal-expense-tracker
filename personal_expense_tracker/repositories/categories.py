import sqlite3

# from typing import List, Dict, Any


class CategoryRepository:
    def __init__(self, db_path: str):
        """
        Initialize the CategoryRepository with a database path, month, and year.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._create_categories_table()

    def _create_categories_table(self):
        """
        Create the categories table if it doesn't exist.
        :param month: Month to create the category for.
        :param year: Year to create the category for.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month VARCHAR(9) NOT NULL,
                    year INTEGER NOT NULL,
                    category_name VARCHAR(50),
                    current_budget INTEGER NOT NULL,
                    expenditure INTEGER NOT NULL,
                    remaining INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    def get_list_of_categories(self) -> list[str]:
        """
        Get the categories of expenditure.
        :return: List of categories.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT category_name FROM categories
                ORDER BY category_name
            """
            )
            conn.commit()
            result = cursor.fetchone()
            return list(result) if result else []

    def get_category(self, category_name: str, month: str, year: int) -> dict | None:
        """
        Get a specific category by name.
        :param category_name: The name of the category to retrieve.
        :return: The category details or None if not found.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT category_name FROM categories
                WHERE category_name = ? AND month = ? AND year = ?
            """,
                (category_name, month, year),
            )
            conn.commit()
            result = cursor.fetchone()
            return result[0] if result else None

    def get_category_budget(self, month: str, year: int) -> list[dict]:
        """
        Get all categories and their budget for a specific month and year.
        :param month: The month to retrieve categories for.
        :param year: The year to retrieve categories for.
        :return: List of categories for the specified month and year.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT category_name, current_budget, expenditure, remaining
                FROM categories
                WHERE month = ? AND year = ?
            """,
                (month, year),
            )
            conn.commit()
            result = cursor.fetchall()
            return [dict(row) for row in result] if result else []

    def create_category(
        self, category_name: str, current_budget: int, month: str, year: int
    ) -> None:
        """
        Create a new category.
        :param category_name: The name of the category to create.
        :param current_budget: The budget for the category.
        :param month: The month for the category.
        :param year: The year for the category.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO categories (month, year, category_name, current_budget, expenditure, remaining)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (month, year, category_name, current_budget, 0, current_budget),
            )
            conn.commit()
