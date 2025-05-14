import sqlite3

# from typing import List, Dict, Any


class CategoryRepository:
    def __init__(self, db_path: str, month: str, year: int):
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

    def get_categories(self) -> list[str]:
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
            return result[0] if result else []
