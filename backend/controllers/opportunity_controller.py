from flask import request, jsonify
from services.opportunity_service import OpportunityService
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_opportunity():
    admin_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
        
    result, status_code = OpportunityService.create_opportunity(int(admin_id), data)
    return jsonify(result), status_code

@jwt_required()
def get_opportunities():
    admin_id = get_jwt_identity()
    result, status_code = OpportunityService.get_opportunities(int(admin_id))
    return jsonify(result), status_code

@jwt_required()
def get_opportunity(id):
    admin_id = get_jwt_identity()
    result, status_code = OpportunityService.get_opportunity(int(admin_id), id)
    return jsonify(result), status_code

@jwt_required()
def update_opportunity(id):
    admin_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
        
    result, status_code = OpportunityService.update_opportunity(int(admin_id), id, data)
    return jsonify(result), status_code

@jwt_required()
def delete_opportunity(id):
    admin_id = get_jwt_identity()
    result, status_code = OpportunityService.delete_opportunity(int(admin_id), id)
    return jsonify(result), status_code
