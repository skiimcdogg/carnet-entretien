from uuid import uuid4

from fastapi.testclient import TestClient

from carnet_entretien.api.main import app

client = TestClient(app)


def test_read_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_vehicle_returns_201_and_contains_id():
    response = client.post(
        "/vehicles",
        json={"brand": "Dacia", "model": "Sandero", "mileage_kms": 39000, "first_registration_date": "2019-07-12"},
    )

    assert response.status_code == 201
    assert "id" in response.json()


def test_create_vehicle_without_kms_returns_422():
    response = client.post(
        "/vehicles",
        json={"brand": "Dacia", "model": "Sandero", "first_registration_date": "2019-07-12"},
    )

    assert response.status_code == 422


def test_create_vehicle_with_negative_kms_returns_422():
    response = client.post(
        "/vehicles",
        json={"brand": "Dacia", "model": "Sandero", "mileage_kms": -39000, "first_registration_date": "2019-07-12"},
    )

    assert response.status_code == 422


def test_get_vehicle_returns_200():
    post_response = client.post(
        "/vehicles",
        json={"brand": "Dacia", "model": "Sandero", "mileage_kms": 39000, "first_registration_date": "2019-07-12"},
    )

    vehicle_dict = post_response.json()
    vehicle_id = vehicle_dict["id"]

    get_response = client.get(f"/vehicles/{vehicle_id}")

    assert get_response.json() == {
        "brand": "Dacia",
        "model": "Sandero",
        "mileage_kms": 39000,
        "first_registration_date": "2019-07-12",
        "id": vehicle_id,
        "maintenance_history": [],
    }


def test_get_vehicle_with_wrong_id_returns_422():
    vehicle_fake_id = "1234"

    get_response = client.get(f"/vehicles/{vehicle_fake_id}")

    assert get_response.status_code == 422


def test_get_vehicle_with_non_existing_id_returns_404():
    vehicle_fake_id = uuid4()

    get_response = client.get(f"/vehicles/{vehicle_fake_id}")
    assert get_response.status_code == 404


def test_get_vehicle_list():
    post_response = client.post(
        "/vehicles",
        json={"brand": "Dacia", "model": "Sandero", "mileage_kms": 39000, "first_registration_date": "2019-07-12"},
    )

    get_response = client.get("/vehicles")
    vehicle_list = get_response.json()
    vehicle_list_id = [v["id"] for v in vehicle_list]

    assert get_response.status_code == 200
    assert post_response.json()["id"] in vehicle_list_id
