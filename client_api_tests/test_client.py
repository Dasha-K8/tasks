import pytest
import requests
from jsonschema import validate, ValidationError

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

negative_clients = [
    (0, {"name": "Alice", "age": 17, "tel": "8(495)123-45-67"}, 404,
        "There is no client with this ID"),
    (1, {"name": "Alice", "age": 18, "tel": 71234568901}, 400,
        "Invalid data type"),
    (1, {"name": "Alice", "age": 18, "tel": "+7123"}, 400,
        "Incorrect data format"),
    (2, {"name": "Dasha", "tel": "8(495)123-45-67"}, 400,
        "Required field is missing"),
    (1, {"name": 123, "age": 18, "tel": "8(495)123-45-67"}, 400,
        "Invalid data type"),
    (1, "Hello", 400,
        "Invalid data type"),
    (1, [123456], 400,
        "Invalid data type"),
    (3, {"city": "Dasha", "apple": 19, "table": "8(495)123-45-67"}, 400,
        "Required field is missing"),
    (1, {"name": "Alice", "age": "18", "tel": "51234568901"}, 400,
        "Incorrect data format")
]

def create_client(base_client):
    response = requests.post(base_url, json=base_client)
    assert response.status_code == 201
    data = response.json()
    return data

class TestClientPositive:
    @pytest.mark.parametrize("base_client", [
        ({"name": "Bob", "age": 100, "tel": "+7 912 345 67 89"}),
        ({"name": "Alice", "age": 18, "tel": "8(495)123-45-67"})
    ])
    def test_create_client(self, base_client):
        data = create_client(base_client)
        assert data["message"] == "A new client has been created"
        assert "client_id" in data
        client_id = data["client_id"]
        assert client_id > 0

        url = f"{base_url}/{client_id}"
        response = requests.get(url)
        data_client = response.json()

        assert response.status_code == 200
        try:
            validate(data_client, client_schema)
        except ValidationError as e:
            raise ValidationError(e.message)
        assert base_client == data_client

    def test_delete_client(self):
        response = requests.get(base_url)
        all_clients_befor = response.json()

        new_client = [
        {"name": "Alice", "age": 18, "tel": "8(495)123-45-67"},
        {"name": "Sara", "age": 19, "tel": "+7 949 456 98 12"},
        {"name": "Bob", "age": 45, "tel": "+7 949 123 45 67"},
        {"name": "Alex", "age": 69, "tel": "+7 949 768 89 16"},
        {"name": "Masha", "age": 54, "tel": "8(949)345-87-98"}
            ]

        client_id = []
        for base_client in new_client:
            data = create_client(base_client)
            client_id.append(data["client_id"])

        client_delete = client_id[2]
        response = requests.delete(f"{base_url}/{client_delete}")
        assert response.status_code == 204
        assert not response.text

        response = requests.get(base_url)
        assert response.status_code == 200
        all_clients_after = response.json()

        assert len(all_clients_after) == len(all_clients_befor) + len(new_client) - 1
        assert str(client_delete) not in all_clients_after


    def test_get_clients(self):
        response = requests.get(base_url)
        assert response.status_code == 200
        data = response.json()
        assert data is not None and type(data) is dict

        for client_id, client in data.items():
            assert int(client_id) > 0
            try:
                validate(client, client_schema)
            except ValidationError as e:
                raise ValidationError(e.message)

    def test_put_client(self):
        base_client = {"name": "Dasha", "age": 21, "tel": "+7 912 456 98 12"}
        data = create_client(base_client)
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        new_client = {"name": "Sara", "age": 18, "tel": "8(495)123-45-67"}
        response = requests.put(url, json=new_client)
        assert response.status_code == 201
        data_put = response.json()
        assert data_put["message"] == "Client has been updated successfully"

        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        try:
            validate(data, client_schema)
        except ValidationError as e:
            raise ValidationError(e.message)
        assert data == new_client


    @pytest.mark.parametrize("new_data_client", [
        {"age": 22, "tel": "8(495)123-45-67"},
        {"name": "Sara"}
    ])
    def test_patch_client(self, new_data_client):
        base_client = {"name": "Misha", "age": 21, "tel": "+7 912 456 98 12"}
        data = create_client(base_client)
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        response = requests.patch(url, json=new_data_client)
        assert response.status_code == 200
        data_patch = response.json()
        assert data_patch["message"] == "Client data has been updated"

        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        try:
            validate(data, client_schema)
        except ValidationError as e:
            raise ValidationError(e.message)

        for key, value in base_client.items():
            if key not in new_data_client:
                assert data[key] == value

        for key, value in new_data_client.items():
            assert key in data
            assert data[key] == value

class TestClientNegative:
    @pytest.mark.parametrize("client_id, client, status_code, expected_message", negative_clients)
    def test_negative_create_client(self, client_id, client, status_code, expected_message):
        if client_id == 0:
            expected_message = "You must be 18 years old or older"
        response = requests.post(base_url, json=client)
        data = response.json()
        assert response.status_code == 400
        assert "Validation error" in data
        assert expected_message in data["Validation error"]

    @pytest.mark.parametrize("client_id", [-1,0, "abc", None])
    def test_negative_client_id(self, client_id):
        url = f"{base_url}/{client_id}"
        response = requests.get(url)
        assert response.status_code == 404
        if client_id == 0:
            assert response.status_code == 404
            assert response.json()["error"] == "Client does not exist"

    @pytest.mark.parametrize("client_id", [-1, 0, "abc", None])
    def test_negative_delete_client(self, client_id):
        url = f"{base_url}/{client_id}"
        response = requests.delete(url)
        assert response.status_code == 404
        if client_id == 0:
            assert response.status_code == 404
            assert response.json()["error"] == "There is no client with this ID"

    @pytest.mark.parametrize( "client_id, client, status_code, expected_message", negative_clients)
    def test_negative_put_client(self, client_id, client, status_code, expected_message):
        url = f"{base_url}/{client_id}"
        response = requests.put(url, json=client)
        assert response.status_code == status_code

        try:
            data = response.json()
            assert expected_message in data["error"]
        except ValueError:
            message_data = response.text
            assert str(expected_message) in message_data

    @pytest.mark.parametrize( "client_id, client, status_code, expected_message", negative_clients)
    def test_negative_patch_client(self, client_id, client, status_code, expected_message):
        url = f"{base_url}/{client_id}"
        if client_id == 2 and client["name"] == "Dasha":
            client["tel"] = "5(495)123-45-67"
            expected_message = "Incorrect data format"
        if client_id == 3 and client["city"] == "Dasha":
            expected_message = "There are extra fields"

        response = requests.patch(url, json=client)
        assert response.status_code == status_code

        try:
            data = response.json()
            assert expected_message in data["error"]
        except ValueError:
            message_data = response.text
            assert str(expected_message) in message_data


