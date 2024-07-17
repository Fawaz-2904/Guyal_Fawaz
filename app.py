from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)
data_file = 'users.json'

def load_data():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}

def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

def find_user(user_id):
    users = load_data()["users"]
    for user in users:
        if user["id"] == user_id:
            return user
    return None

@app.route('/users', methods=['GET'])
def get_users():
    data = load_data()
    if not data["users"]:
        return jsonify({"error": "No user found"}), 404
    return jsonify(data), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = find_user(user_id)
    if user is None:
        return jsonify({"error": "User doesn't exist"}), 404
    return jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    data = load_data()
    new_user["id"] = len(data["users"]) + 1
    new_user["created_at"] = datetime.now().isoformat()
    new_user["updated_at"] = datetime.now().isoformat()
    data["users"].append(new_user)
    save_data(data)
    return jsonify(new_user), 200

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = find_user(user_id)
    if user is None:
        return jsonify({"error": "User doesn't exist"}), 404

    update_data = request.json
    user.update(update_data)
    user["updated_at"] = datetime.now().isoformat()
    
    data = load_data()
    for idx, u in enumerate(data["users"]):
        if u["id"] == user_id:
            data["users"][idx] = user
            break
    save_data(data)
    return jsonify(user), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = load_data()
    user = find_user(user_id)
    if user is None:
        return jsonify({"error": "User doesn't exist"}), 404
    
    data["users"] = [u for u in data["users"] if u["id"] != user_id]
    save_data(data)
    return '', 204

if __name__ == '_main_':
    app.run(debug=True)