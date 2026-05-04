from models.opportunity import Opportunity
from database.db import db

class OpportunityService:
    
    @staticmethod
    def create_opportunity(admin_id, data):
        required_fields = ['name', 'category', 'duration', 'start_date', 'description', 'skills']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400
            
        new_opp = Opportunity(
            admin_id=admin_id,
            name=data['name'],
            category=data['category'],
            duration=data['duration'],
            start_date=data['start_date'],
            description=data['description'],
            skills=data['skills'],
            future_opportunities=data.get('future_opportunities'),
            max_applicants=data.get('max_applicants')
        )
        
        db.session.add(new_opp)
        db.session.commit()
        
        return {'message': 'Opportunity created successfully', 'opportunity': new_opp.to_dict()}, 201

    @staticmethod
    def get_opportunities(admin_id):
        opportunities = Opportunity.query.filter_by(admin_id=admin_id).all()
        return {'opportunities': [opp.to_dict() for opp in opportunities]}, 200

    @staticmethod
    def get_opportunity(admin_id, opp_id):
        opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
        if not opp:
            return {'message': 'Opportunity not found or access denied'}, 404
            
        return {'opportunity': opp.to_dict()}, 200

    @staticmethod
    def update_opportunity(admin_id, opp_id, data):
        opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
        if not opp:
            return {'message': 'Opportunity not found or access denied'}, 404
            
        # Update fields if present in data
        updateable_fields = ['name', 'category', 'duration', 'start_date', 'description', 'skills', 'future_opportunities', 'max_applicants']
        for field in updateable_fields:
            if field in data:
                setattr(opp, field, data[field])
                
        db.session.commit()
        return {'message': 'Opportunity updated successfully', 'opportunity': opp.to_dict()}, 200

    @staticmethod
    def delete_opportunity(admin_id, opp_id):
        opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
        if not opp:
            return {'message': 'Opportunity not found or access denied'}, 404
            
        db.session.delete(opp)
        db.session.commit()
        return {'message': 'Opportunity deleted successfully'}, 200
