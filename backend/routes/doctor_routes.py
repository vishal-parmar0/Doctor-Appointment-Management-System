import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Appointment, Prescription, Doctor, Review, ActivityLog
from datetime import datetime, timedelta
from sqlalchemy import func, and_

doctor_bp = Blueprint('doctor', __name__)

# ==================== DASHBOARD ENDPOINTS ====================

@doctor_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard summary stats: total patients, appointments today, total consultations, average rating"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        # Total unique patients
        total_patients = db.session.query(func.count(func.distinct(Appointment.patient_id))).filter_by(doctor_id=doctor_id).scalar() or 0
        
        # Appointments today
        today = datetime.utcnow().date()
        appointments_today = db.session.query(func.count(Appointment.id)).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == today
            )
        ).scalar() or 0
        
        # Total completed consultations
        total_consultations = db.session.query(func.count(Appointment.id)).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.status == 'completed'
            )
        ).scalar() or 0
        
        # Average rating from reviews
        avg_rating = db.session.query(func.avg(Review.rating)).filter(
            Review.doctor_id == doctor_id
        ).scalar() or 0
        avg_rating = round(float(avg_rating), 1) if avg_rating else 0
        
        return jsonify({
            "total_patients": total_patients,
            "appointments_today": appointments_today,
            "total_consultations": total_consultations,
            "average_rating": avg_rating
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/appointments/today', methods=['GET'])
@jwt_required()
def get_today_appointments():
    """Get all appointments for today with patient details"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        today = datetime.utcnow().date()
        
        appointments = db.session.query(Appointment, User).join(
            User, Appointment.patient_id == User.id
        ).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == today
            )
        ).order_by(Appointment.appointment_time).all()
        
        result = []
        for appt, patient in appointments:
            result.append({
                "id": appt.id,
                "patient_name": patient.full_name,
                "patient_id": patient.id,
                "reason": appt.notes or "Routine Checkup",
                "appointment_type": appt.consultation_type,
                "time": str(appt.appointment_time),
                "status": appt.status
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/appointments/accept/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def accept_appointment(appointment_id):
    """Accept/Confirm an appointment"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        appointment = Appointment.query.filter_by(
            id=appointment_id,
            doctor_id=doctor_id
        ).first()
        
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        
        appointment.status = 'confirmed'
        db.session.commit()
        
        return jsonify({
            "message": "Appointment confirmed",
            "appointment_id": appointment.id,
            "status": appointment.status
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/appointments/reject/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def reject_appointment(appointment_id):
    """Reject/Cancel an appointment"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        appointment = Appointment.query.filter_by(
            id=appointment_id,
            doctor_id=doctor_id
        ).first()
        
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        
        appointment.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            "message": "Appointment rejected",
            "appointment_id": appointment.id,
            "status": appointment.status
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/appointments/start/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def start_consultation(appointment_id):
    """Start/Begin a consultation (in progress)"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        appointment = Appointment.query.filter_by(
            id=appointment_id,
            doctor_id=doctor_id
        ).first()
        
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        
        appointment.status = 'in_consultation'
        db.session.commit()
        
        return jsonify({
            "message": "Consultation started",
            "appointment_id": appointment.id,
            "status": appointment.status
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/analytics/patient-growth', methods=['GET'])
@jwt_required()
def get_patient_growth_analytics():
    """Get monthly patient count data for growth chart"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        # Get data for last 6 months
        months_data = []
        for i in range(5, -1, -1):
            month_date = datetime.utcnow() - timedelta(days=30*i)
            month_start = month_date.replace(day=1)
            if i == 0:
                month_end = datetime.utcnow().date()
            else:
                next_month = month_date.replace(day=28) + timedelta(days=4)
                month_end = (next_month - timedelta(days=next_month.day)).date()
            
            count = db.session.query(func.count(func.distinct(Appointment.patient_id))).filter(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.appointment_date >= month_start.date(),
                    Appointment.appointment_date <= month_end
                )
            ).scalar() or 0
            
            months_data.append({
                "month": month_date.strftime("%b"),
                "count": count
            })
        
        return jsonify(months_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/activity/recent', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """Get recent activity logs for doctor"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        # Get recent appointments and activities
        activities = db.session.query(ActivityLog).filter_by(
            doctor_id=doctor_id
        ).order_by(ActivityLog.created_at.desc()).limit(5).all()
        
        result = []
        for activity in activities:
            result.append({
                "activity_type": activity.activity_type,
                "patient_name": activity.patient_name,
                "timestamp": activity.created_at.isoformat(),
                "description": activity.description
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/profile/completion', methods=['GET'])
@jwt_required()
def get_profile_completion():
    """Get doctor profile completion percentage"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        user = User.query.get(doctor_id)
        doctor = Doctor.query.filter_by(user_id=doctor_id).first()
        
        if not user or not doctor:
            return jsonify({"error": "Doctor not found"}), 404
        
        completion_fields = {
            "full_name": bool(user.full_name),
            "phone": bool(user.phone),
            "dob": bool(user.dob),
            "address": bool(user.address),
            "specialization": bool(doctor.specialization),
            "experience": doctor.experience_years > 0,
            "consultation_fee": doctor.consultation_fee is not None
        }
        
        completion_percent = int((sum(completion_fields.values()) / len(completion_fields)) * 100)
        
        missing_items = [k for k, v in completion_fields.items() if not v]
        
        return jsonify({
            "completion_percent": completion_percent,
            "missing_items": missing_items,
            "completed_fields": [k for k, v in completion_fields.items() if v]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_doctor_profile():
    """Update doctor profile information"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    data = request.get_json()
    
    try:
        user = User.query.get(doctor_id)
        doctor = Doctor.query.filter_by(user_id=doctor_id).first()
        
        if not user or not doctor:
            return jsonify({"error": "Doctor not found"}), 404
        
        # Update user fields
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "phone" in data:
            user.phone = data["phone"]
        if "dob" in data:
            user.dob = data["dob"]
        if "gender" in data:
            user.gender = data["gender"]
        if "address" in data:
            user.address = data["address"]
        
        # Update doctor fields
        if "specialization" in data:
            doctor.specialization = data["specialization"]
        if "experience_years" in data:
            doctor.experience_years = data["experience_years"]
        if "consultation_fee" in data:
            doctor.consultation_fee = data["consultation_fee"]
        if "city" in data:
            doctor.city = data["city"]
        
        db.session.commit()
        
        return jsonify({
            "message": "Profile updated successfully",
            "doctor_id": doctor_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/patient/add', methods=['POST'])
@jwt_required()
def add_patient():
    """Add a new patient (doctor can create patient record)"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    data = request.get_json()
    
    try:
        # Create new user with patient role
        new_user = User(
            full_name=data.get('name'),
            email=data.get('email', f"patient_{datetime.utcnow().timestamp()}@medibook.local"),
            password_hash=User.hash_password('default123'),
            role='patient',
            phone=data.get('contact'),
            gender=data.get('gender'),
            address=data.get('address')
        )
        
        db.session.add(new_user)
        db.session.flush()
        
        # Log activity
        activity = ActivityLog(
            doctor_id=doctor_id,
            patient_name=new_user.full_name,
            activity_type='patient_added',
            description=f"Added new patient: {new_user.full_name}"
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            "message": "Patient added successfully",
            "patient_id": new_user.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ==================== EXISTING ENDPOINTS ====================

@doctor_bp.route('/appointments/doctor', methods=['GET'])
@jwt_required()
def get_doctor_appointments():
    """Endpoint for doctors to view their schedule"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        apps = db.session.query(Appointment, User).join(User, Appointment.patient_id == User.id).filter(Appointment.doctor_id == doctor_id).all()
        
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/prescriptions', methods=['POST'])
@jwt_required()
def add_prescription():
    """Doctors upload prescriptions after consultation"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    data = request.get_json()
    
    try:
        app_id = data.get('appointment_id')
        medicines = data.get('medicines')
        advice = data.get('advice')
        
        app = Appointment.query.filter_by(id=app_id, doctor_id=doctor_id).first()
        if not app:
            return jsonify({"error": "No such appointment session"}), 404
            
        new_rx = Prescription(appointment_id=app_id, medicines=medicines, advice=advice)
        db.session.add(new_rx)
        
        app.status = 'completed'
        
        db.session.commit()
        return jsonify({"message": "Prescription uploaded and consultation completed!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_doctor_dashboard():
    """Legacy endpoint: Returns doctor summary info for cards"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        total_patients = db.session.query(func.count(func.distinct(Appointment.patient_id))).filter_by(doctor_id=doctor_id).scalar() or 0
        appts_today = db.session.query(func.count(Appointment.id)).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == datetime.utcnow().date()
            )
        ).scalar() or 0
        total_appts = db.session.query(func.count(Appointment.id)).filter_by(doctor_id=doctor_id).scalar() or 0
        
        return jsonify({
            "patients": total_patients,
            "today": appts_today,
            "total": total_appts,
            "rating": 4.9
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_doctor_patients():
    """Get all unique patients for the doctor with their last visit/diagnosis"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        # Subquery to find last appointment for each patient for this doctor
        last_appt_subquery = db.session.query(
            Appointment.patient_id,
            func.max(Appointment.appointment_date).label('last_visit_date'),
            func.max(Appointment.id).label('last_appt_id')
        ).filter(Appointment.doctor_id == doctor_id).group_by(Appointment.patient_id).subquery()

        # Join User with the subquery and optionally with Prescription to get "diagnosis" context
        patients = db.session.query(User, last_appt_subquery.c.last_visit_date, Appointment.notes).join(
            last_appt_subquery, User.id == last_appt_subquery.c.patient_id
        ).join(
            Appointment, Appointment.id == last_appt_subquery.c.last_appt_id
        ).all()
        
        result = []
        for patient, last_visit, last_notes in patients:
            # Calculate age from DOB if available
            age = "N/A"
            if patient.dob:
                today = datetime.utcnow().date()
                dob = datetime.strptime(str(patient.dob), '%Y-%m-%d').date() if isinstance(patient.dob, str) else patient.dob
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            result.append({
                "id": patient.id,
                "patient_id_label": f"MB-{202400 + patient.id}",
                "full_name": patient.full_name,
                "age": age,
                "gender": patient.gender or "N/A",
                "phone": patient.phone or "N/A",
                "last_diagnosis": last_notes or "Regular Checkup",
                "last_visit": str(last_visit)
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_bp.route('/patient/details/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_details(patient_id):
    """Get full medical history for a specific patient of this doctor"""
    current_user = json.loads(get_jwt_identity())
    doctor_id = current_user['id']
    
    try:
        patient = User.query.get(patient_id)
        if not patient or patient.role != 'patient':
            return jsonify({"error": "Patient not found"}), 404
            
        # Get all appointments for this patient with this doctor
        history = db.session.query(Appointment, Prescription).outerjoin(
            Prescription, Appointment.id == Prescription.appointment_id
        ).filter(
            and_(
                Appointment.patient_id == patient_id,
                Appointment.doctor_id == doctor_id
            )
        ).order_by(Appointment.appointment_date.desc()).all()
        
        formatted_history = []
        for appt, rx in history:
            formatted_history.append({
                "date": str(appt.appointment_date),
                "type": appt.consultation_type,
                "notes": appt.notes,
                "medicines": rx.medicines if rx else None,
                "advice": rx.advice if rx else None
            })
            
        return jsonify({
            "patient_info": {
                "id": patient.id,
                "name": patient.full_name,
                "email": patient.email,
                "phone": patient.phone,
                "gender": patient.gender,
                "dob": str(patient.dob) if patient.dob else None,
                "patient_id_label": f"MB-{202400 + patient.id}"
            },
            "history": formatted_history
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
