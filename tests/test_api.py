import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "/api/airports" in data["endpoints"]

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_settings():
    res = client.get("/api/settings")
    assert res.status_code == 200
    data = res.json()
    assert "supported_years" in data

def test_airports_catalog():
    res = client.get("/api/airports")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert any(a["airport_code"] == "SEA" for a in data)

def test_airport_kpis():
    res = client.get("/api/airports/SEA/kpis?year=2023")
    assert res.status_code == 200
    data = res.json()
    assert data["airport_code"] == "SEA"
    assert "direct_destinations" in data

def test_airport_routes():
    res = client.get("/api/airports/SEA/routes?year=2023&min_departures=10")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["origin"] == "SEA"

def test_airline_network():
    res = client.get("/api/airlines/UA/network?year=2023")
    assert res.status_code == 200
    data = res.json()
    assert data["carrier_code"] == "UA"
    assert "hubs" in data
    assert "routes" in data

def test_airline_kpis():
    res = client.get("/api/airlines/UA/kpis?year=2023")
    assert res.status_code == 200
    data = res.json()
    assert data["carrier_code"] == "UA"
    assert "system_load_factor" in data

def test_fleet_summary():
    res = client.get("/api/fleet/summary?family=Boeing%20737&year=2023")
    assert res.status_code == 200
    data = res.json()
    assert data["family_filter"] == "Boeing 737"
    assert "kpis" in data
    assert "subfleets" in data
    assert len(data["subfleets"]) > 0

if __name__ == "__main__":
    test_root()
    test_health()
    test_settings()
    test_airports_catalog()
    test_airport_kpis()
    test_airport_routes()
    test_airline_network()
    test_airline_kpis()
    test_fleet_summary()
    print("All API endpoints tested and passed!")
