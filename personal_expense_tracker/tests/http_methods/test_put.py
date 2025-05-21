"""
Tests for all the PUT HTTP methods.
"""

import random
from fastapi.testclient import TestClient

from personal_expense_tracker.main import app


def test_put_budget_is_less_than_zero():
    """
    Assert that you cannot put a budget less than zero.
    """
    client = TestClient(app)

    # Random number less than 0
    budget = random.randint(-999999, -1)

    response = client.put("/budget", params={"new_budget": budget})
    data = response.json()

    assert response.status_code == 200
    assert data.get("message") == "Monthly budget cannot be less than zero."


def test_put_budget_is_zero_or_greater():
    """
    Assert that you can only put a budget greater than zero.
    """
    client = TestClient(app)

    # Set up for the test
    # Get the current budget to save for later
    response = client.get("/")
    current_budget = response.json().get("current_budget")

    # Random number less than 0
    budget = random.randint(0, 9999999)

    response = client.put("/budget", params={"new_budget": budget})
    data = response.json()

    assert response.status_code == 200
    assert data.get("current_budget") == budget

    # Revert back to the normal budget
    client.put("/budget", params={"new_budget": current_budget})
