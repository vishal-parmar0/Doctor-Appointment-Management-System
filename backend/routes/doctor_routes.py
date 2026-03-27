from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Appointment, Prescription, Doctor
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/appointments/doctor', methods=['GET'])
@jwt_required()
def get_doctor_appointments():
    """Endpoint for doctors to view their schedule"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'doctor':
        return jsonify({"error": "Unauthorized Access"}), 403
        
    # Query: My Appointments JOIN Patients (who are from USERS table)
    apps = db.session.query(Appointment, User).join(User, Appointment.patient_id == User.id).filter(Appointment.doctor_id == current_user['id']).all()
    
    res = []
    for ap, patient_user in apps:
        res.append({
            "id": ap.id,
            "patient_name": patient_user.full_name,
            "patient_id": patient_user.id,
            "date": str(ap.appointment_date),
            "time": str(ap.appointment_time),
            "status": ap.status,
            "type": ap.consultation_type,
            "notes": ap.notes
        })
    
    return jsonify(res), 200

@doctor_bp.route('/appointments/accept/<int:id>', methods=['PUT'])
@jwt_required()
def accept_appointment(id):
    """Mark as confirmed"""
    current_user = get_jwt_identity()
    app = Appointment.query.filter_by(id=id, doctor_id=current_user['id']).first()
    
    if not app:
        return jsonify({"error": "Appointment not found"}), 404
        
    app.status = 'confirmed'
    db.session.commit()
    return jsonify({"message": "Appointment confirmed"}), 200

@doctor_bp.route('/appointments/reject/<int:id>', methods=['PUT'])
@jwt_required()
def reject_appointment(id):
    """Mark as cancelled by doctor"""
    current_user = get_jwt_identity()
    app = Appointment.query.filter_by(id=id, doctor_id=current_user['id']).first()
    
    if not app:
        return jsonify({"error": "Appointment not found"}), 404
        
    app.status = 'cancelled' # Rejection by doctor = cancelled status
    db.session.commit()
    return jsonify({"message": "Appointment rejected"}), 200

@doctor_bp.route('/prescriptions', methods=['POST'])
@jwt_required()
def add_prescription():
    """Doctors upload prescriptions after consultation"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    app_id = data.get('appointment_id')
    medicines = data.get('medicines')
    advice = data.get('advice')
    
    # Check if app exists for THIS doctor
    app = Appointment.query.filter_by(id=app_id, doctor_id=current_user['id']).first()
    if not app:
        return jsonify({"error": "No such appointment session"}), 404
        
    # Create Prescription
    new_rx = Prescription(appointment_id=app_id, medicines=medicines, advice=advice)
    db.session.add(new_rx)
    
    # Update app status to completed
    app.status = 'completed'
    
    db.session.commit()
    return jsonify({"message": "Prescription uploaded and consultation completed!"}), 201
@doctor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_doctor_dashboard():
    """Returns doctor summary info for cards"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'doctor':
        return jsonify({"error": "Unauthorized Access"}), 403
        
    doc_id = current_user['id']
    
    total_patients = db.session.query(Appointment.patient_id).filter_by(doctor_id=doc_id).distinct().count()
    appts_today = Appointment.query.filter_by(doctor_id=doc_id, appointment_date=datetime.utcnow().date()).count()
    total_appts = Appointment.query.filter_by(doctor_id=doc_id).count()
    
    return jsonify({
        "patients": total_patients,
        "today": appts_today,
        "total": total_appts,
        "rating": 4.9 # Default rating placeholder
    }), 200
