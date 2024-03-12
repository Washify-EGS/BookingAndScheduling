# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_bookings():
    response = client.get("/busy")
    assert response.status_code == 200
    assert response.json() == []

def test_create_booking():
    booking_data = {"date": "2022-12-01"}
    response = client.post("/busy", json=booking_data)
    assert response.status_code == 201
    assert response.json()["date"] == "2022-12-01"

# Add more test functions for other endpoints
