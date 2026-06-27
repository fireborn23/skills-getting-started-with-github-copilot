from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = deepcopy(app_module.activities)
    app_module.activities = deepcopy(original_state)
    yield
    app_module.activities = deepcopy(original_state)


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


def test_signup_adds_a_participant(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["activities"][activity_name]["participants"] == [email]


def test_duplicate_signup_returns_a_conflict(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_their_name(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert email not in response.json()["activities"][activity_name]["participants"]
