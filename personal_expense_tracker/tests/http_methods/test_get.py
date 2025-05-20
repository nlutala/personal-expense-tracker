"""
Tests for all the GET HTTP methods.
"""

from datetime import datetime
import os

from fastapi.testclient import TestClient

from personal_expense_tracker.main import app


def test_get_root():
    """
    Assert that the status code for read_root is 200 and response
    contains expected keys.
    """
    client = TestClient(app)
    response = client.get("/")
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
    client = TestClient(app)
    response = client.get("/categories")
    data = response.json()

    assert response.status_code == 200
    assert "description" in data
    assert "version" in data
    assert "author" in data
    assert "docs" in data
    assert "current_date" in data
    assert "categories" in data
