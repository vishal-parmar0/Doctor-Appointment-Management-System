from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.models import db, User, Doctor, Patient

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint to register patients, doctors, or admins"""
    data = request.get_json()
    
    # Input Basic Fields
    try:
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        role = data.get('role', 'patient') # Default: patient
        phone = data.get('phone')

        if not email or not password or not full_name:
            return jsonify({"error": "Fields are missing"}), 400

        # Unique Check
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User email already registered"}), 400

        # Main User Row
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=User.hash_password(password),
            role=role,
            phone=phone
        )
        db.session.add(new_user)
        db.session.flush() # ID required for next steps

        # Create Profile
        if role == 'doctor':
             specialization = data.get('specialization', 'General Physician')
             city = data.get('city', 'Ahmedabad')
             fee = data.get('consultation_fee', 500)
             
             new_doc = Doctor(user_id=new_user.id, specialization=specialization, city=city, consultation_fee=fee)
             db.session.add(new_doc)
        elif role == 'patient':
             new_patient = Patient(user_id=new_user.id)
             db.session.add(new_patient)

        db.session.commit()
        return jsonify({"message": f"{role.capitalize()} registered successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get JWT Access Token"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Additional logic check: Is doctor verified?
        if user.role == 'doctor':
            doc_profile = Doctor.query.filter_by(user_id=user.id).first()
            if doc_profile and doc_profile.verification_status != 'verified':
                return jsonify({"error": "Doctor account not verified by Admin"}), 403

        # Success - Generate Token
        access_token = create_access_token(identity={"id": user.id, "role": user.role, "email": user.email})
        return jsonify({
            "token": access_token,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "role": user.role
            }
        }), 200

    return jsonify({"error": "Invalid email or matching password"}), 401
