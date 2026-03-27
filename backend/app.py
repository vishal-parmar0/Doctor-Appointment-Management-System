from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.models import db, bcrypt
from config import Config

# Routes
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.admin_routes import admin_bp
from routes.landing_routes import landing_bp

def create_app():
    """Application Factory for MediBook Backend"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app) # Allow Cross-Origin (connecting frontend to backend)
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(landing_bp, url_prefix='/api/public')

    # Global Error Handlers (404, 500)
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint Not Found"}), 444

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal Server Error"}), 505

    # Heartbeat
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "status": "MediBook Backend is LIVE!",
            "message": "Visit /api/auth/register to get started.",
            "version": "1.0.0"
        }), 200

    return app

if __name__ == "__main__":
    # Create the app instance
    app = create_app()
    
    # Run server locally (host '0.0.0.0' allows LAN access)
    # Default port: 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
