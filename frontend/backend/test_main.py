from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) >= 3

def test_match_returns_ranked_results_and_explanation():
    response = client.post("/matches", json={
        "title": "Python API optimization",
        "description": "Improve FastAPI endpoints and optimize PostgreSQL database queries"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 3
    assert data["results"][0]["score"] >= data["results"][-1]["score"]
    assert data["results"][0]["explanation"]

def test_missing_title_rejected():
    response = client.post("/matches", json={
        "title": "",
        "description": "A sufficiently long description for a test"
    })
    assert response.status_code == 422

def test_unknown_employee_not_found():
    response = client.get("/employees/UNKNOWN")
    assert response.status_code == 404
