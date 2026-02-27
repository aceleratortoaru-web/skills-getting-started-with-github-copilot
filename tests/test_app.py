from fastapi.testclient import TestClient
import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app, activities  # Import activities directly

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    # Arrange: (nothing to arrange for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

# Test POST /activities/{activity_name}/signup (success)
def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json().get("message", "")
    # Clean up: remove test user if needed
    activities[activity]["participants"].remove(email)

# Test POST /activities/{activity_name}/signup (duplicate)
def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    # Add once
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    # Clean up
    activities[activity]["participants"].remove(email)

# Test POST /activities/{activity_name}/signup (activity not found)
def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser3@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
