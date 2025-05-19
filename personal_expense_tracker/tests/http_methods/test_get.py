"""
Tests for all the GET HTTP methods.
"""

from fastapi.testclient import TestClient
from personal_expense_tracker.main import app
from personal_expense_tracker.repositories import (
    BudgetRepository, CategoryRepository
)
from datetime import datetime
import os

CLIENT = TestClient(app)


def test_get_root(mocker):
    """
    Assert that the status code for read_root is 200 and response
    contains expected keys.
    """
    # Mock the budget and categories repo
    path = os.path.join(os.path(__file__), "databases/budget.db")
    print(path)

    mocker.patch(
        "personal_expense_tracker.main.budget_repo",
        budget_repo=BudgetRepository(
            db_path=path,
            month=datetime.now().strftime("%B"),
            year=datetime.now().year,
        ),
    )

    response = CLIENT.get("/")
    data = response.json()

    assert response.status_code == 200
    assert "description" in data
    assert "version" in data
    assert "author" in data
    assert "docs" in data
    assert "current_date" in data
    assert "current_budget" in data
    assert "current_expenditure" in data
    assert "current_remaining" in data
    assert "categories" in data


def test_get_categories():
    """
    Assert that the status code for get_categories is 200 and response
    contains expected keys.
    """
    response = CLIENT.get("/categories")
    data = response.json()

    assert response.status_code == 200
    assert "description" in data
    assert "version" in data
    assert "author" in data
    assert "docs" in data
    assert "current_date" in data
    assert "categories" in data
