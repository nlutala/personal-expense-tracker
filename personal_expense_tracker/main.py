# from typing import Union
from datetime import datetime
from repositories import BudgetRepository, CategoryRepository

from fastapi import FastAPI

app = FastAPI()

budget_repo = BudgetRepository(
    db_path="databases/budget.db",
    month=datetime.now().strftime("%B"),
    year=datetime.now().year,
)

categories_repo = CategoryRepository(
    db_path="databases/categories.db",
    month=datetime.now().strftime("%B"),
    year=datetime.now().year,
)


@app.get("/")
def read_root():
    """
    Root endpoint that provides a welcome message and basic information
    about the Personal Expense Tracker API."""
    return {
        "description": "Welcome to the Personal Expense Tracker API. "
        "This API helps you track your personal expenses. "
        "This was designed as a monthly budget tracker, now currently "
        f"displaying the current month of {datetime.now().strftime('%B')} "
        f" {datetime.now().year}. "
        "You can add, update, and delete expenses, "
        "as well as view your current budget and remaining balance. "
        "This API is built using FastAPI and is designed to be easy "
        "to use and understand.",
        "version": "1.0.0",
        "author": "www.github.com/nlutala",
        "docs": "http://127.0.0.1:8000/docs",
        "current_date": str(datetime.now()),
        "current_budget": budget_repo.get_budget(
            month=datetime.now().strftime("%B"),
            year=datetime.now().year,
        ),
        "current_expenditure": budget_repo.get_expenditure(
            month=datetime.now().strftime("%B"),
            year=datetime.now().year,
        ),
        "current_remaining": budget_repo.get_remaining(
            month=datetime.now().strftime("%B"),
            year=datetime.now().year,
        ),
        "categories": categories_repo.get_categories()
        # "housing",
        # "utilities",
        # "subscriptions",
        # "groceries",
        # "entertainment",
        # "transportation"
    }


@app.put("/budget")
def change_budget(new_budget: int):
    """
    Endpoint to change the current budget.
    :param new_budget: The new budget amount.
    :return: The updated budget.
    """
    budget_repo.update_budget(
        month=datetime.now().strftime("%B"),
        year=datetime.now().year,
        new_budget=new_budget,
    )
    return {
        "current_budget": budget_repo.get_budget(
            month=datetime.now().strftime("%B"),
            year=datetime.now().year,
        )
    }


@app.post("/categories")
def add_category(new_category: str, current_budget: int) -> dict | None:
    """
    Endpoint to add a new category.
    :param new_category: The new category to add.
    :param current_budget: The budget for the new category.
    :return: The updated category.
    """
    # Check if the category already exists (if it does, do nothing)
    # Check if the budget of the category is less than the current budget
    # Create the new category and add it to the category table
