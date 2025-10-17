from flask import Flask, request, jsonify

app = Flask(__name__)

clients = [
    {"client_id": 1, "name": "Misha", "age": 22, "tel": 74264573902},
    {"client_id": 2, "name": "Anna", "age": 25, "tel": 73895634298}
]

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

@app.route('/client', methods=['GET'])
def get_clients():
    return jsonify(clients)

@app.route('/client', methods=['POST'])
def create_client():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data["name"]
    if not name or type(name) != str:
        return jsonify({"error": "Name must be a non-empty string"}), 400


    age = data["age"]
    if age is None:
        return jsonify({"error": "The age field is required"}), 400
    try:
        age = int(age)
    except ValueError:
        return jsonify({"error": "Age must be a non-empty integer"}), 400
    if age <= 18:
            return jsonify({"error": "Age must be greater than 18"}), 400


    tel = data["tel"]
    if tel is None:
        return jsonify({"error": "The phone number is a required field to fill in"}), 400
    tel_str = str(tel)

    if not tel_str.isdigit():
        return jsonify({"error": "The phone number must consist of 11 digits"}), 400

    if len(tel_str) != 11:
        return jsonify({"error": "The phone number must consist of 11 digits"}), 400

    client_id = len(clients) + 1
    clients.append({
        "client_id": client_id,
        "name": name,
        "age": age,
        "tel": tel
    })

    return jsonify({
        "message": "A new client has been created",
        "client_id": client_id
    }), 201

@app.route('/client/<int:client_id>', methods=['GET'])
def get_id_clients(client_id):
    for client in clients:
        if client["client_id"] == client_id:
            return jsonify(client)
    return jsonify({"error": "There is no user with this ID"}), 404


@app.route('/client/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    for client in clients:
        if client["client_id"] == client_id:
            clients.remove(client)
            return jsonify({"message": "The client has been deleted"}), 200
    return jsonify({"error": "There is no client with this ID"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)























