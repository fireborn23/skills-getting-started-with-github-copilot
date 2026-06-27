from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_delete_participant_unregisters_student():
    response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )
    assert response.status_code == 200

    delete_response = client.delete(
        "/activities/Chess Club/participants/student@example.com"
    )
    assert delete_response.status_code == 200
    assert "student@example.com" not in client.get("/activities").json()["Chess Club"]["participants"]
