import bcrypt
from datetime import timedelta
from flask_jwt_extended import create_access_token
from models.admin import Admin
from database.db import db
import re
import os

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
    def send_reset_email(to_email, reset_link):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import os
        
        sender_email = os.environ.get('MAIL_USERNAME')
        sender_password = os.environ.get('MAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = "Sky Foundation - Password Reset Request"
            
            body = f"Hello,\n\nWe received a request to reset your password for the Sky Foundation Admin Portal.\n\nPlease click the link below to set a new password:\n{reset_link}\n\nThis link will expire in 1 hour.\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nSky Foundation Team"
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception:
            return False

    @staticmethod
    def forgot_password(data):
        email = data.get('email')
        if not email:
            return {'message': 'Missing email'}, 400
            
        admin = Admin.query.filter_by(email=email).first()
        
        if admin:
            reset_token = create_access_token(identity=str(admin.id), expires_delta=timedelta(hours=1))
            frontend_url = os.environ.get('FRONTEND_URL', 'http://127.0.0.1:5500/sky/admin.html')
            reset_link = f"{frontend_url}?token={reset_token}"
            AuthService.send_reset_email(email, reset_link)
            
        return {'message': 'If the email exists, a reset link will be sent.'}, 200

    @staticmethod
    def reset_password(data):
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return {'message': 'Missing token or new password'}, 400
            
        from flask_jwt_extended import decode_token
        
        try:
            decoded = decode_token(token)
            admin_id = decoded['sub']
            
            admin = Admin.query.get(admin_id)
            if not admin:
                return {'message': 'Invalid token'}, 400
                
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin.password = hashed_password
            db.session.commit()
            
            return {'message': 'Password has been reset successfully.'}, 200
        except Exception as e:
            err_str = str(e).lower()
            if 'expired' in err_str:
                return {'message': 'Reset link has expired. Please request a new one.'}, 400
            return {'message': 'Invalid or expired reset link.'}, 400
