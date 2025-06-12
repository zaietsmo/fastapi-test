from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_all_products():
    response = client.get("/all_products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_product_by_name():
    response = client.get("/products/ВОДА НЕГАЗОВАНА мала")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert "name" in data


def test_product_field():
    response = client.get("/products/ВОДА НЕГАЗОВАНА мала/calories")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert isinstance(response.json(), (int, float, str, type(None)))


def test_product_not_found():
    response = client.get("/products/NonExistentProduct")
    assert response.status_code == 404


def test_field_not_found():
    response = client.get("/products/Big Mac/nonexistentfield")
    assert response.status_code in (404, 422)
