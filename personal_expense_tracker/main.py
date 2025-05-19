"""
The API to track and manage your personal expenses.
"""

from datetime import datetime

from fastapi import FastAPI

from personal_expense_tracker.repositories import (
    BudgetRepository, CategoryRepository
)

app = FastAPI()

budget_repo = BudgetRepository(
    db_path="databases/budget.db",
    month=datetime.now().strftime("%B"),
    year=datetime.now().year,
)

categories_repo = CategoryRepository(db_path="databases/categories.db")


@app.get("/")
def read_root():
    """
    Root endpoint that provides a welcome message and basic information
    about the Personal Expense Tracker API.
    :return: A dictionary with a welcome message and basic information.
    """
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
        "categories": categories_repo.get_list_of_categories(),
        # "housing",
        # "utilities",
        # "subscriptions",
        # "groceries",
        # "entertainment",
        # "transportation"
    }


@app.get("/categories")
def get_categories():
    """
    Endpoint to get the list of categories.
    :return: A list of categories.
    """
    default_dict = {
        "description": "A list of categories and budget for the "
        f"current month of {datetime.now().strftime('%B')} "
        f"{datetime.now().year}.",
        "version": "1.0.0",
        "author": "www.github.com/nlutala",
        "docs": "http://127.0.0.1:8000/docs",
        "current_date": str(datetime.now()),
        "categories": categories_repo.get_list_of_categories(),
        # "housing",
        # "utilities",
        # "subscriptions",
        # "groceries",
        # "entertainment",
        # "transportation"
    }

    categories_and_budget = categories_repo.get_category_budget(
        month=datetime.now().strftime("%B"),
        year=datetime.now().year,
    )

    if categories_and_budget:
        return {**default_dict, **categories_and_budget}

    return default_dict


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
def add_category(new_category: str, budget: int) -> dict | None:
    """
    Endpoint to add a new category.
    :param new_category: The new category to add.
    :param current_budget: The budget for the new category.
    :return: The updated category.
    """
    month, year = datetime.now().strftime("%B"), datetime.now().year
    current_budget = budget_repo.get_budget(
        datetime.now().strftime("%B"), datetime.now().year
    )

    # Check if the category already exists (if it does, do nothing)
    if categories_repo.get_category(new_category.lower(), month, year):
        return {"message": "Category already exists."}

    # Check if the budget of the category is less than the current budget
    elif current_budget - categories_repo.get_reserved_budget(month, year) < 0:
        return {
            "message": f"Budget for {new_category} is greater than current "
            f"budget of {current_budget}."
        }

    # Create the new category and add it to the category table
    else:
        categories_repo.create_category(
            category_name=new_category.lower(),
            current_budget=budget,
            month=datetime.now().strftime("%B"),
            year=datetime.now().year,
        )
        return {
            "message": f"Category {new_category} added successfully.",
            "category": categories_repo.get_category(
                new_category, month, year
            ),
            "current_budget": budget_repo.get_budget(
                month=datetime.now().strftime("%B"),
                year=datetime.now().year,
            ),
        }


@app.delete("/categories")
def remove_category(category: str) -> dict | None:
    """
    Endpoint to remove a category.
    :param category: The category to remove.
    :return: A message you deleted a category.
    """
    month, year = datetime.now().strftime("%B"), datetime.now().year

    # Check if the category already exists (if doesn't, do nothing)
    if not categories_repo.get_category(category.lower(), month, year):
        return {"message": "Category does not exist."}
    else:
        categories_repo.delete_category(
            category_name=category.lower(),
            month=datetime.now().strftime("%B"),
            year=datetime.now().year,
        )
        return {"message": f"Category {category} removed successfully."}
