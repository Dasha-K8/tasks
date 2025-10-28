import pytest
import requests

base_url = "http://127.0.0.1:3000/clients"


class TestClientPositive:
    @pytest.mark.parametrize("client, expected_status", [
        ({"name": "Bob", "age": 100, "tel": 10000000000}, 201),
        ({"name": "Alice", "age": 18, "tel": 99999999999}, 201)
    ])
    def test_create_client(self, client, expected_status):
        response = requests.post(base_url, json=client)
        data = response.json()
        assert response.status_code == expected_status
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        response = requests.get(url)
        assert response.status_code == 200
        new_data_client = response.json()
        assert client["name"] == new_data_client["name"]
        assert client["age"] == new_data_client["age"]
        assert client["tel"] == new_data_client["tel"]


    def test_get_client_id(self):
        new_client = {"name": "Vova", "age": 40, "tel": 79493456789}
        response = requests.post(base_url, json=new_client)
        assert response.status_code == 201
        data = response.json()
        client_id = data["client_id"]

        url = f"{base_url}/{client_id}"
        response = requests.get(url)
        assert response.status_code == 200
        new_data_client = response.json()
        assert new_client["name"] == new_data_client["name"]
        assert new_client["age"] == new_data_client["age"]
        assert new_client["tel"] == new_data_client["tel"]


    def test_delete_client(self):
        new_client = {"name": "Dasha", "age": 21, "tel": 71234567898}
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


    def test_get_client(self):
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
            assert client["age"] is not None
            assert client["tel"] is not None



class TestClientNegative:
    @pytest.mark.parametrize("client", [
        ({"name": "Bob", "age": 101, "tel": 71234568901}),
        ({"name": "Alice", "age": 17, "tel": 71234568901}),
        ({"name": "Alice", "age": 18, "tel": 71234568901123}),
        ({"name": 123, "age": "abc", "tel": ""}),
        (["Hello"]),
        ([123456]),
        ({"city": "Alice", "apple": 19, "table": 71234568901}),
        ({"name": "Alice", "age": "18", "tel": "71234568901"})
    ])
    def test_negative_client(self, client):
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

    def test_negative_get_clients(self):
        url = "http://127.0.0.1:3000/client"
        response = requests.get(url)
        assert response.status_code == 404






































