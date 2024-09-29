from flask import Blueprint, jsonify

server = Blueprint('server', __name__)

@server.route('/', methods=['GET'])
def main():
    data = {"message": "hey"}
    return jsonify(data)

@server.route('/api/', methods=['GET'])
def get_data():
    data = {"message": "Hey there!"}
    return jsonify(data)

@server.route('/api/test', methods=['GET'])
def get_test():
    data = {"message": "Hey there test!"}
    return jsonify(data)