from flask import request, jsonify
from services.auth_service import AuthService

def signup():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    result, status_code = AuthService.signup(data)
    return jsonify(result), status_code

def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
        
    result, status_code = AuthService.login(data)
    return jsonify(result), status_code

def forgot_password():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
        
    result, status_code = AuthService.forgot_password(data)
    return jsonify(result), status_code

def reset_password():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
        
    result, status_code = AuthService.reset_password(data)
    return jsonify(result), status_code
