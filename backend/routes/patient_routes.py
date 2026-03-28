from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Doctor, Patient, Appointment, Prescription

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/doctors', methods=['GET'])
@jwt_required()
def get_all_doctors():
    """Endpoint for patients to find all available/verified doctors"""
    # Join with User table for names
    docs = db.session.query(User, Doctor).join(Doctor, User.id == Doctor.user_id).filter(Doctor.verification_status == 'verified').all()
    
    # Prep response JSON
    res = []
    for user, doc in docs:
        res.append({
            "id": user.id,
            "full_name": user.full_name,
            "specialization": doc.specialization,
            "city": doc.city,
            "consultation_fee": str(doc.consultation_fee),
            "experience_years": doc.experience_years
        })

    return jsonify(res), 200

@patient_bp.route('/appointments', methods=['POST'])
@jwt_required()
def book_appointment():
    """Endpoint to create an appointment slot"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    try:
        # Create Appointment object
        new_app = Appointment(
            patient_id=current_user['id'],
            doctor_id=data.get('doctor_id'),
            appointment_date=data.get('appointment_date'),
            appointment_time=data.get('appointment_time'),
            consultation_type=data.get('consultation_type', 'Clinic'),
            notes=data.get('notes')
        )
        db.session.add(new_app)
        db.session.commit()
        return jsonify({"message": "Appointment request sent successfully!"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@patient_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_patient_appointments_flexible():
    """Flexible endpoint to view personal appointment history as a patient with status and limit"""
    current_user = get_jwt_identity()
    status_filter = request.args.get('status')
    limit = request.args.get('limit', type=int)
    
    query = db.session.query(Appointment, User).join(User, Appointment.doctor_id == User.id).filter(Appointment.patient_id == current_user['id'])
    
    if status_filter:
        statuses = status_filter.split(',')
        query = query.filter(Appointment.status.in_(statuses))
    
    query = query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc())
    
    if limit:
        apps = query.limit(limit).all()
    else:
        apps = query.all()
    
    res = []
    for ap, doc_user in apps:
        res.append({
            "id": ap.id,
            "doctor_name": doc_user.full_name,
            "date": str(ap.appointment_date),
            "time": str(ap.appointment_time),
            "status": ap.status,
            "type": ap.consultation_type,
            "specialty": doc_user.doctor_profile.specialization if doc_user.doctor_profile else "General Physician"
        })
    
    return jsonify(res), 200

@patient_bp.route('/appointments/patient', methods=['GET'])
@jwt_required()
def get_patient_appointments_legacy():
    """Legacy endpoint for patient appointments"""
    return get_patient_appointments_flexible()

@patient_bp.route('/appointments/cancel/<int:id>', methods=['PUT'])
@jwt_required()
def cancel_appointment(id):
    """Update status to cancelled"""
    current_user = get_jwt_identity()
    app = Appointment.query.filter_by(id=id, patient_id=current_user['id']).first()
    
    if not app:
        return jsonify({"error": "Appointment not found or not owned by you"}), 404
        
    app.status = 'cancelled'
    db.session.commit()
    return jsonify({"message": "Appointment cancelled successfully"}), 200
@patient_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_patient_dashboard():
    """Returns patient summary info for cards"""
    current_user = get_jwt_identity()
    patient_id = current_user['id']
    
    total_apps = Appointment.query.filter_by(patient_id=patient_id).count()
    upcoming = Appointment.query.filter_by(patient_id=patient_id, status='confirmed').count()
    completed = Appointment.query.filter_by(patient_id=patient_id, status='completed').count()
    cancelled = Appointment.query.filter_by(patient_id=patient_id, status='cancelled').count()
    
    return jsonify({
        "total": total_apps,
        "upcoming": upcoming,
        "completed": completed,
        "cancelled": cancelled
    }), 200

@patient_bp.route('/prescriptions/patient', methods=['GET'])
@jwt_required()
def get_patient_prescriptions():
    """List all prescriptions issued to this patient"""
    current_user = get_jwt_identity()
    
    # Needs to JOIN Appointment to Filter by patient_id
    data = db.session.query(Prescription, Appointment, User).join(Appointment, Prescription.appointment_id == Appointment.id).join(User, Appointment.doctor_id == User.id).filter(Appointment.patient_id == current_user['id']).all()
    
    res = []
    for rx, app, doc_user in data:
        res.append({
            "id": rx.id,
            "doctor_name": doc_user.full_name,
            "medicines": rx.medicines,
            "advice": rx.advice,
            "date": str(rx.created_at.date())
        })
    return jsonify(res), 200
