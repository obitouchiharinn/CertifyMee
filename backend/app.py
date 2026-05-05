from flask import Flask
from config import Config
from database.db import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Import blueprints
from routes.auth_routes import auth_bp
from routes.opportunity_routes import opp_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(opp_bp, url_prefix='/api')

    # Create database tables if they don't exist
    with app.app_context():
        from models.admin import Admin
        from models.opportunity import Opportunity
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
