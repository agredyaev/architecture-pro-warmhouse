import pytest
import requests
import os

BASE_URL = os.getenv('BASE_URL', 'http://app:8080')

def test_health_check():
    """Tests that the health check endpoint is working."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200

def test_create_and_get_sensor():
    """Tests creating a new sensor and then retrieving it."""
    # Create a new sensor
    new_sensor = {
        "name": "Living Room Temperature",
        "type": "temperature",
        "location": "Living Room",
        "unit": "°C"
    }
    response = requests.post(f"{BASE_URL}/api/v1/sensors", json=new_sensor)
    assert response.status_code == 201
    sensor_id = response.json()["id"]

    # Get the sensor by ID
    response = requests.get(f"{BASE_URL}/api/v1/sensors/{sensor_id}")
    assert response.status_code == 200
    assert response.json()["name"] == new_sensor["name"]
    assert "value" in response.json()
    assert response.json()["value"] != 0

def test_update_sensor():
    """Tests updating an existing sensor."""
    # Create a new sensor to update
    new_sensor = {
        "name": "Kitchen Temperature",
        "type": "temperature",
        "location": "Kitchen",
        "unit": "°C"
    }
    response = requests.post(f"{BASE_URL}/api/v1/sensors", json=new_sensor)
    assert response.status_code == 201
    sensor_id = response.json()["id"]

    # Update the sensor
    updated_sensor = {
        "name": "Kitchen Temperature (Updated)",
        "type": "temperature",
        "location": "Kitchen",
        "unit": "°F"
    }
    response = requests.put(f"{BASE_URL}/api/v1/sensors/{sensor_id}", json=updated_sensor)
    assert response.status_code == 200

    # Verify the update
    response = requests.get(f"{BASE_URL}/api/v1/sensors/{sensor_id}")
    assert response.status_code == 200
    assert response.json()["name"] == updated_sensor["name"]
    assert response.json()["unit"] == updated_sensor["unit"]

def test_delete_sensor():
    """Tests deleting a sensor."""
    # Create a new sensor to delete
    new_sensor = {
        "name": "Garage Temperature",
        "type": "temperature",
        "location": "Garage",
        "unit": "°C"
    }
    response = requests.post(f"{BASE_URL}/api/v1/sensors", json=new_sensor)
    assert response.status_code == 201
    sensor_id = response.json()["id"]

    # Delete the sensor
    response = requests.delete(f"{BASE_URL}/api/v1/sensors/{sensor_id}")
    assert response.status_code == 204

    # Verify the deletion
    response = requests.get(f"{BASE_URL}/api/v1/sensors/{sensor_id}")
    assert response.status_code == 404