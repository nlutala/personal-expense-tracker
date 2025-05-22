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


def test_add_category_when_budget_exceeds_remaining_balance():
    """
    Assert that you get a message when trying to add a category that
    has a greater budget than the remaining balance.
    """
    client = TestClient(app)

    # Get the current budget
    response = client.get("/")
    current_budget = response.json().get("current_budget")

    new_category = "test_category"

    # Make the budget for the test category greater than the current
    # budget
    budget = current_budget + 1

    response = client.post(
        "/categories", params={"new_category": new_category, "budget": budget}
    )
    data = response.json()

    assert response.status_code == 200
    assert (
        data.get("message")
        == f"Budget for {new_category} is greater than current budget of {current_budget}."
    )


# def test_add_category_is_successful():
#     """
#     Assert that you get a message after successfully adding a category.
#     """
#     client = TestClient(app)

#     # Set up for the test
#     # If someone happens to use the name test_category:
#     # 1. Get the name of the category and budget to store it

#     if "test_category" in categories:
#         client.get(
#             "/categories", params={"new_category": new_category, "budget": budget}
#         )

#     # 2. Delete it from the DB
#     # 3. Add the test version and make the assertions
#     # 4. Delete the test category and replace it with the original
#     response = client.get("/categories")
#     categories = response.json().get("categories", [])

#     new_category = "test_category"
#     budget = 0

#     if "test_category" not in categories:
#         client.post(
#             "/categories", params={"new_category": new_category, "budget": budget}
#         )

#     response = client.post(
#         "/categories", params={"new_category": new_category, "budget": budget}
#     )
#     data = response.json()

#     assert response.status_code == 200
#     assert data.get("message") == "Category already exists."

#     # Delete the category from DB
#     client.delete("/categories", params={"category": new_category})
