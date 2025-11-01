import pytest
import requests
from jsonschema import validate

base_url = "http://127.0.0.1:3000/clients"

client_schema = {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer", "minimum": 18 },
        "tel": { "type": "string",
                 "pattern": r"^(\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$"}
      },
      "required": ["name", "age", "tel"],
      "additionalProperties": False
    }

class TestClientPositive:
    @pytest.mark.parametrize("client, expected_status", [
        ({"name": "Bob", "age": 100, "tel": "+7 912 345 67 89"}, 201),
        ({"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}, 201)
    ])
    def test_create_client(self, client, expected_status):
        response = requests.post(base_url, json=client)
        data = response.json()
        print(data)
        assert response.status_code == expected_status
        assert "client_id" in data
        client_id = data["client_id"]
        assert client_id > 0

        response = requests.get(base_url)
        assert response.status_code == 200
        all_clients = response.json()

        assert str(client_id) in all_clients
        data_client = all_clients[str(client_id)]
        validate(data_client, client_schema)
        assert client["name"] == data_client["name"]
        assert client["age"] == data_client["age"]
        assert client["tel"] == data_client["tel"]



    def test_get_client_id(self):
        new_client = {"name": "Vova", "age": 40, "tel": "8(495)123-50-90"}
        response = requests.post(base_url, json=new_client)
        assert response.status_code == 201
        data = response.json()
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        response = requests.get(url)
        assert response.status_code == 200
        new_data_client = response.json()
        validate(new_data_client, client_schema)
        assert new_client["name"] == new_data_client["name"]
        assert new_client["age"] == new_data_client["age"]
        assert new_client["tel"] == new_data_client["tel"]


    def test_delete_client(self):
        new_client = {"name": "Dasha", "age": 21, "tel": "+7 912 456 98 12"}
        response = requests.post(base_url, json=new_client)
        assert response.status_code == 201
        data = response.json()
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        response = requests.delete(url)
        assert response.status_code == 200
        print(response.json())

        response = requests.get(url)
        assert response.status_code == 404
        print(response.json())


    def test_get_clients(self):
        response = requests.get(base_url)
        assert response.status_code == 200
        data = response.json()
        assert data is not None and type(data) is dict

        for client_id, client in data.items():
            assert int(client_id) > 0
            assert "name" in client
            assert "age" in client
            assert "tel" in client

            assert client["name"]
            assert client["age"]
            assert client["tel"]


    def test_put_client(self):
        base_client = {"name": "Dasha", "age": 21, "tel": "+7 912 456 98 12"}
        response = requests.post(base_url, json=base_client)
        assert response.status_code == 201
        data = response.json()
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        new_client = {"name": "Sara", "age": 18, "tel": "8(495)123-45-67"}
        response = requests.put(url, json=new_client)
        assert response.status_code == 200

        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        validate(data, client_schema)
        assert data["name"] == new_client["name"]
        assert data["age"] == new_client["age"]
        assert data["tel"] == new_client["tel"]


    @pytest.mark.parametrize("new_data_client", [
        {"age": 22, "tel": "8(495)123-45-67"},
        {"name": "Sara"}
    ])
    def test_patch_client(self, new_data_client):
        base_client = {"name": "Misha", "age": 21, "tel": "+7 912 456 98 12"}
        response = requests.post(base_url, json=base_client)
        assert response.status_code == 201
        data = response.json()
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        response = requests.patch(url, json=new_data_client)
        assert response.status_code == 200

        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        validate(data, client_schema)

        for key, value in new_data_client.items():
            assert key in data
            assert data[key] == value


class TestClientNegative:
    @pytest.mark.parametrize("client", [
        ({"name": "Alice", "age": 17, "tel": "8(495)123-45-67"}),
        ({"name": "Alice", "age": 18, "tel": 71234568901}),
        ({"name": "Alice", "age": 18, "tel": "+7123"}),
        ({"name": 123, "age": "abc", "tel": "abs"}),
        (["Hello"]),
        ([123456]),
        ({"city": "Alice", "apple": 19, "table": "8(495)123-45-67"}),
        ({"name": "Alice", "age": "18", "tel": "51234568901"})
    ])
    def test_negative_create_client(self, client):
        response = requests.post(base_url, json=client)
        data = response.json()
        assert response.status_code == 400
        assert "Validation error" in data["error"]
        print(data)

    @pytest.mark.parametrize("client_id", [-1,0, "abc", None])
    def test_negative_client_id(self, client_id):
        url = f"{base_url}/{client_id}"
        response = requests.get(url)
        assert response.status_code == 404

    @pytest.mark.parametrize("client_id", [-1, 0, "abc", None])
    def test_negative_delete_client(self, client_id):
        url = f"{base_url}/{client_id}"
        response = requests.delete(url)
        assert response.status_code == 404

    @pytest.mark.parametrize( "client_id, client",
        [(0, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        (-1, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        ("abc", {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        (None, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        (1, {"age": 18, "tel": "8(495)123-45-67"}),
        (1, {"age": 18, "tel": "8(495)123-45-67"}),
        (1, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67", "city": "Moscow"}),
        (1, {"city": "Alice", "apple": 19, "table": "8(495)123-45-67"})]
    )
    def test_negative_put_client(self, client_id, client):
        url = f"{base_url}/{client_id}"
        response = requests.put(url, json=client)
        print(response)
        assert response.status_code in [404, 400]

    @pytest.mark.parametrize( "client_id, client",
        [(0, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        (-1, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        ("abc", {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        (None, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"}),
        (1, { "age": 17, "tel": "9(495)123-45-67"}),
        (1, {"name": "Alice", "age": 18, "tel": "8(495)123-45-67", "city": "Moscow"}),
        (1, {"city": "Alice", "apple": 19})]
    )
    def test_negative_patch_client(self, client_id, client):
        url = f"{base_url}/{client_id}"
        response = requests.patch(url, json=client)
        print(response)
        assert response.status_code in [404, 400]