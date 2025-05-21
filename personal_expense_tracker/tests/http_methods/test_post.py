"""
Tests for all the POST HTTP methods.
"""

from fastapi.testclient import TestClient

from personal_expense_tracker.main import app


def test_add_category_when_exists():
    """
    Assert that you get a message when trying to add a category that
    already exists in the DB.
    """
    client = TestClient(app)

    # Set up for the test
    # Get list of categories to check if test_category exists or not
    # If it isn't, add it in (then delete later)
    response = client.get("/categories")
    categories = response.json().get("categories", [])

    new_category = "test_category"
    budget = 0

    if "test_category" not in categories:
        client.post(
            "/categories", params={"new_category": new_category, "budget": budget}
        )

    response = client.post(
        "/categories", params={"new_category": new_category, "budget": budget}
    )
    data = response.json()

    assert response.status_code == 200
    assert data.get("message") == "Category already exists."

    # Delete the category from DB
    client.delete("/categories", params={"category": new_category})
