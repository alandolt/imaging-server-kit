from flask import Flask, jsonify, request

app = Flask(__name__)
services = []

@app.route('/register', methods=['POST'])
def register_service():
    service_name = request.json.get('name')
    if service_name:
        services.append(service_name)
        return jsonify({"message": "Service registered", "services": services}), 201
    return jsonify({"error": "Invalid data"}), 400

@app.route('/services', methods=['GET'])
def list_services():
    return jsonify({"services": services}), 200

@app.route('/deregister', methods=['POST'])
def deregister_service():
    service_name = request.json.get('name')
    if service_name in services:
        services.remove(service_name)
        return jsonify({"message": "Service deregistered", "services": services}), 200
    return jsonify({"error": "Service not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
