from flask import Blueprint, jsonify
from models.models import User, Doctor, db

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/featured-doctors', methods=['GET'])
def get_featured_doctors():
    """Returns top verified doctors for landing page"""
    # Simply get first 4 verified doctors
    docs = db.session.query(User, Doctor).join(Doctor, User.id == Doctor.user_id).filter(Doctor.verification_status == 'verified').limit(4).all()
    
    res = []
    for user, doc in docs:
        res.append({
            "id": user.id,
            "full_name": user.full_name,
            "specialization": doc.specialization,
            "city": doc.city,
            "experience": doc.experience_years
        })
    return jsonify(res), 200

@landing_bp.route('/specializations', methods=['GET'])
def get_specializations():
    """Returns unique specializations from the database"""
    # Get distinct specializations
    specialties = db.session.query(Doctor.specialization).distinct().all()
    res = [s[0] for s in specialties if s[0]]
    return jsonify(res), 200

@landing_bp.route('/cities', methods=['GET'])
def get_cities():
    """Returns list of cities where doctors are available"""
    cities = db.session.query(Doctor.city).distinct().all()
    res = [c[0] for c in cities if c[0]]
    return jsonify(res), 200
