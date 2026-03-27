from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Doctor, Patient, Appointment

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Admin dashboard to view all users and their basic info"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Admin access required"}), 403
        
    users = User.query.all()
    res = []
    for u in users:
        res.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role,
            "created_at": str(u.created_at)
        })
    
    return jsonify(res), 200

@admin_bp.route('/verify-doctor/<int:id>', methods=['PUT', 'POST'])
@jwt_required()
def verify_doctor(id):
    """Admin desk approves doctor verification via ID"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Admin portal access required"}), 403
        
    doc = Doctor.query.filter_by(user_id=id).first()
    if not doc:
        return jsonify({"error": "Doctor profile not found"}), 404
        
    doc.verification_status = 'verified'
    db.session.commit()
    return jsonify({"message": f"Doctor {id} verified successfully"}), 200

@admin_bp.route('/reject-doctor/<int:id>', methods=['PUT', 'POST'])
@jwt_required()
def reject_doctor(id):
    """Admin desk rejects doctor verification via ID"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Admin portal access required"}), 403
        
    doc = Doctor.query.filter_by(user_id=id).first()
    if not doc:
        return jsonify({"error": "Doctor profile not found"}), 404
        
    doc.verification_status = 'rejected'
    db.session.commit()
    return jsonify({"message": f"Doctor {id} rejected"}), 200

@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_admin_analytics():
    """Stats for the central dashboard cards"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Admin portal access required"}), 403
        
    # Count totals
    total_docs = Doctor.query.filter_by(verification_status='verified').count()
    total_patients = Patient.query.count()
    total_apps = Appointment.query.count()
    pending_verifications = Doctor.query.filter_by(verification_status='pending').count()
    
    return jsonify({
        "doctors": total_docs,
        "patients": total_patients,
        "appointments": total_apps,
        "pending_verifications": pending_verifications
    }), 200
@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_admin_dashboard():
    """Returns platform overview for admin cards"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Admin portal access required"}), 403
        
    total_docs = Doctor.query.count()
    total_patients = Patient.query.count()
    # Simple mock for platform revenue - 10% of all confirmed consults
    revenue = db.session.query(db.func.sum(Doctor.consultation_fee)).join(Appointment, Doctor.user_id == Appointment.doctor_id).filter(Appointment.status == 'confirmed').scalar() or 0
    revenue = float(revenue) * 0.1
    
    signups_today = User.query.filter(db.func.date(User.created_at) == db.func.current_date()).count()
    
    return jsonify({
        "doctors": total_docs,
        "patients": total_patients,
        "revenue": round(revenue, 2),
        "signups": signups_today
    }), 200
@admin_bp.route('/pending-doctors', methods=['GET'])
@jwt_required()
def get_pending_doctors():
    """List all doctors awaiting admin verification"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Admin portal access required"}), 403
        
    pending = db.session.query(User, Doctor).join(Doctor, User.id == Doctor.user_id).filter(Doctor.verification_status == 'pending').all()
    
    res = []
    for user, doc in pending:
        res.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "specialization": doc.specialization,
            "experience_years": doc.experience_years,
            "city": doc.city
        })
    return jsonify(res), 200
