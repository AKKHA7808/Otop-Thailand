import pytest


@pytest.mark.django_db
def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/products/",
        "/provinces/",
        "/map/",
        "/search/",
        "/about/",
    ],
)
def test_pages_load(client, path):
    r = client.get(path)
    assert r.status_code in (200, 302)


@pytest.mark.django_db
def test_api_products_json(client):
    r = client.get("/api/products.json")
    assert r.status_code == 200
