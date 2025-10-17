import pytest
import requests

base_url = "http://127.0.0.1:3000/client"

@pytest.mark.parametrize("client, expected_status", [
    ({"name": "Bob", "age": 19, "tel": 71234568901}, 201),
    ({"name": "Alice", "age": 20, "tel": "73426758904"}, 201),
    ({"name": "Sara", "age": "21", "tel": 75462894031}, 201),
    ({"name": 123, "age": 19, "tel": 71234568901}, 400),
    ({"name": "Alice", "age": 10, "tel": 71234568901}, 400),
    ({"name": "Alice", "age": 18, "tel": 71234568901}, 400),
    ({"name": "Alice", "age": "abc", "tel": 71234568901}, 400),
    ({"name": "Alice", "age": 19, "tel": "abc"}, 400),
    ({"name": "Sara", "age": "15", "tel": 75462894031}, 400),
    ({"name": "Sara", "age": "21", "tel": 754}, 400),
    ({"name": "", "age": "21", "tel": 7546289403}, 400),
    ({"name": "Sara", "age": "", "tel": 7546289403}, 400),
    ({"name": "Sara", "age": "21", "tel": ""}, 400),
])
def test_create_client(client, expected_status):
    response = requests.post(base_url, json=client)
    data = response.json()
    assert response.status_code == expected_status
    if expected_status == 201:
        assert "client_id" in data
    print(data)


def test_get_client_id():
    new_client = {"name": "Vova", "age": 40, "tel": 79493456789}
    response = requests.post(base_url, json=new_client)
    assert response.status_code == 201
    data = response.json()
    print(data)
    client_id = data["client_id"]

    url = f"{base_url}/{client_id}"
    response = requests.get(url)
    assert response.status_code == 200
    new_data_client = response.json()
    assert new_client["name"] == new_data_client["name"]
    assert new_client["age"] == new_data_client["age"]
    assert new_client["tel"] == new_data_client["tel"]
    print(new_data_client)

def test_delete_client():
    new_client = {"name": "Dasha", "age": 21, "tel": 71234567898}
    response = requests.post(base_url, json=new_client)
    assert response.status_code == 201
    data = response.json()
    print(data)
    client_id = data["client_id"]

    url = f"{base_url}/{client_id}"
    response = requests.delete(url, json=client_id)
    assert response.status_code == 200
    print(response.json())

    response = requests.get(url)
    assert response.status_code == 404
    print(response.json())

def test_get_client():
    response = requests.get(base_url)
    assert response.status_code == 200
    print(response.json())
































