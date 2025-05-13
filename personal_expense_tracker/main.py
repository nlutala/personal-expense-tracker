from typing import Union
from datetime import datetime
from repositories.budget import BudgetRepository

from fastapi import FastAPI

app = FastAPI()
budget_repo = BudgetRepository(
    db_path="budget.db",
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
        "categories": [
            # "housing",
            # "utilities",
            # "subscriptions",
            # "groceries",
            # "entertainment",
            # "transportation",
        ],
    }


@app.put("/budget/{new_budget}")
def change_budget(new_budget: int):
    """
    Endpoint to change the current budget.
    """
    # TODO: Add validation to check if the new budget is a positive integer
    # TODO: Get this working and incorporate it into the root endpoint
    budget_repo.update_budget(
        month=datetime.now().strftime("%B"),
        year=datetime.now().year,
        budget=new_budget,
    )
    return {"current_budget": new_budget}


# TODO: Add a new category... Will revisit this later
# @app.get("/add_category/{category_name}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
