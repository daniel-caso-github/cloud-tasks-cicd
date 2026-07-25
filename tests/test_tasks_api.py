"""Unit tests for the task CRUD (no network, moto mocks AWS)."""

import pytest

pytestmark = pytest.mark.unit


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["status"] == "pending"


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task(client):
    created = client.post("/tasks", json={"title": "Task 1"}).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_not_found(client):
    response = client.get("/tasks/does-not-exist")
    assert response.status_code == 404


def test_update_task_status(client):
    created = client.post("/tasks", json={"title": "Task 1"}).json()

    response = client.patch(f"/tasks/{created['id']}", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Task 1"}).json()

    delete_response = client.delete(f"/tasks/{created['id']}")
    get_response = client.get(f"/tasks/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_upload_attachment(client):
    created = client.post("/tasks", json={"title": "Task 1"}).json()

    response = client.post(
        f"/tasks/{created['id']}/attachment",
        files={"file": ("note.txt", b"hello world", "text/plain")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["attachment_key"] == f"{created['id']}/note.txt"
