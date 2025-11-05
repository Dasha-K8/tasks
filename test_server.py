from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError

app = Flask(__name__)

clients = {}
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
client_patch_schema = {
      "type": "object",
      "properties": client_schema["properties"],
      "minProperties": 1,
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
        validate(data, client_schema)
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
        return jsonify({"message": "The client has been deleted"}), 204
    else:
        return jsonify({"error": "There is no client with this ID"}), 404


@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = clients.get(client_id)
    if not client:
        return jsonify({"error": "There is no client with this ID"}), 404

    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400

    data = request.json
    try:
        validate(data, client_schema)
    except ValidationError as e:
        return jsonify({"error": f"Validation error: {e.message}"}), 400

    clients[client_id].update({
        "name": data["name"],
        "age": data["age"],
        "tel": data["tel"]
    })
    return jsonify({
        "message": "Client has been updated successfully",
    }), 201


@app.route('/clients/<int:client_id>', methods=['PATCH'])
def patch_client(client_id):
    client = clients.get(client_id)
    if not client:
        return jsonify({"error": "There is no client with this ID"}), 404

    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400

    data = request.json
    try:
        validate(data, client_patch_schema)
    except ValidationError as e:
        return jsonify({"error": f"Validation error: {e.message}"}), 400

    required_fields = ["name", "age", "tel"]
    for field in required_fields:
        if field in data:
            clients[client_id][field] = data[field]
    return jsonify({
        "message": "Client data has been updated"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)