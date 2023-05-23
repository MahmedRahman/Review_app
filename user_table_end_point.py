from flask import Flask, jsonify, request,Blueprint
from user_table import UserTable


endpoint_user_table = Blueprint('endpoint_user_table', __name__)

# Create an instance of UserTable
user_table = UserTable(host="localhost", user="root", password="12345678", database="eva")

@endpoint_user_table.route('/users', methods=['GET'])
def get_all_users():
    users = []
    all_users = user_table.get_all_users()
    for user in all_users:
        users.append({
            'id': user[0],
            'name': user[1],
            'email': user[2]
        })
    return jsonify({'users': users})


@endpoint_user_table.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    user_id = user_table.create_user(name=name, email=email)
    return jsonify({'user_id': user_id})

@endpoint_user_table.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_table.get_user(user_id=user_id)
    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'message': 'User not found'}), 404

@endpoint_user_table.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    updated_rows = user_table.update_user(user_id=user_id, name=name, email=email)
    if updated_rows > 0:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

@endpoint_user_table.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleted_rows = user_table.delete_user(user_id=user_id)
    if deleted_rows > 0:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


