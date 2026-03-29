from flask import Blueprint, jsonify, request
from models.models import User, Doctor, db

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/featured-doctors', methods=['GET'])
def get_featured_doctors():
    """Returns top verified doctors for landing page"""
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
    specialties = db.session.query(Doctor.specialization).distinct().all()
    res = [s[0] for s in specialties if s[0]]
    return jsonify(res), 200

@landing_bp.route('/cities', methods=['GET'])
def get_cities():
    """Returns list of cities where doctors are available"""
    cities = db.session.query(Doctor.city).distinct().all()
    res = [c[0] for c in cities if c[0]]
    return jsonify(res), 200

@landing_bp.route('/doctors', methods=['GET'])
def get_all_doctors():
    """Get all verified doctors with optional filters"""
    query = db.session.query(User, Doctor).join(Doctor, User.id == Doctor.user_id).filter(Doctor.verification_status == 'verified')
    
    # Filter by specialty
    specialty = request.args.get('specialty')
    if specialty:
        query = query.filter(Doctor.specialization.ilike(f'%{specialty}%'))
    
    # Filter by city
    city = request.args.get('city')
    if city:
        query = query.filter(Doctor.city.ilike(f'%{city}%'))
    
    # Filter by name
    name = request.args.get('name')
    if name:
        query = query.filter(User.full_name.ilike(f'%{name}%'))
    
    doctors = query.all()
    
    res = []
    for user, doc in doctors:
        res.append({
            "id": user.id,
            "full_name": user.full_name,
            "specialization": doc.specialization,
            "city": doc.city,
            "consultation_fee": str(doc.consultation_fee),
            "experience_years": doc.experience_years,
            "bio": doc.bio if hasattr(doc, 'bio') else ""
        })
    
    return jsonify(res), 200
