"""
A file for all the constants to be used in main.py
"""
import os
from personal_expense_tracker.utils.helpers import get_root_path

BUDGET_DB_PATH = os.path.join(get_root_path(), "databases/budget.db")
CATEGORIES_DB_PATH = os.path.join(get_root_path(), "databases/categories.db")
