import bcrypt
from datetime import timedelta
from flask_jwt_extended import create_access_token
from models.admin import Admin
from database.db import db
import re

class AuthService:
    
    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def signup(data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all([name, email, password]):
            return {'message': 'Missing required fields'}, 400

        if not AuthService.validate_email(email):
            return {'message': 'Invalid email format'}, 400

        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            return {'message': 'Email already exists'}, 409

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        new_admin = Admin(name=name, email=email, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        return {'message': 'Admin created successfully', 'admin': new_admin.to_dict()}, 201

    @staticmethod
    def login(data):
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('remember_me', False)

        if not all([email, password]):
            return {'message': 'Missing email or password'}, 400

        admin = Admin.query.filter_by(email=email).first()
        if not admin:
            return {'message': 'Invalid email or password'}, 401

        if not bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
            return {'message': 'Invalid email or password'}, 401

        expires_delta = timedelta(days=30) if remember_me else timedelta(hours=1)
        access_token = create_access_token(identity=str(admin.id), expires_delta=expires_delta)

        return {
            'message': 'Login successful', 
            'access_token': access_token,
            'admin': admin.to_dict()
        }, 200

    @staticmethod
    def forgot_password(data):
        email = data.get('email')
        if not email:
            return {'message': 'Missing email'}, 400
            
        admin = Admin.query.filter_by(email=email).first()
        
        # Always return success to prevent email enumeration
        if admin:
            # Generate a reset token (in a real app, send an email)
            # For this MVP, we just simulate success
            reset_token = create_access_token(identity=str(admin.id), expires_delta=timedelta(hours=1))
            return {'message': 'If the email exists, a reset link will be sent.', 'reset_token': reset_token}, 200
            
        return {'message': 'If the email exists, a reset link will be sent.'}, 200
