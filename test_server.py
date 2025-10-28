from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError

app = Flask(__name__)

clients = {}
client_shema = {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer", "minimum": 18, "maximum": 100 },
        "tel": { "type": "integer", "minimum": 10000000000, "maximum": 99999999999 }
      },
      "required": ["name", "age", "tel"],
      "additionalProperties": False
    }

@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify(clients)

@app.route('/clients', methods=['POST'])
def create_client():
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400

    data = request.json

    try:
        validate(data, client_shema)
    except ValidationError as e:
        return jsonify({"error": f"Validation error: {e.message}"}), 400

    if clients:
        client_id = max(clients.keys()) + 1
    else:
        client_id = 1

    clients[client_id] = {
        "name": data["name"],
        "age": data["age"],
        "tel": data["tel"]
    }
    return jsonify({
        "message": "A new client has been created",
        "client_id": client_id
    }), 201

@app.route('/clients/<int:client_id>', methods=['GET'])
def get_id_clients(client_id):
    client = clients.get(client_id)
    if client:
        return jsonify(client), 200
    else:
        return jsonify({"error": "Client does not exist"}), 404


@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = clients.get(client_id)
    if client:
        del clients[client_id]
        return jsonify({"message": "The client has been deleted"}), 200
    else:
        return jsonify({"error": "There is no client with this ID"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)























