import sys
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
from routes.notification_routes import notification_bp
from routes.message_routes import message_bp

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
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(message_bp, url_prefix='/api/messages')

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
    
    # Check for 'runserver' argument
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        print("🚀 MediBook Server starting in 'runserver' mode...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        # Default run behavior
        app.run(host='0.0.0.0', port=5000, debug=True)
