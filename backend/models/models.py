from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime


# Shared Instance
db = SQLAlchemy()
bcrypt = Bcrypt()

# -----------------
# 1. User Model (Auth & Basic Info)
# -----------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('patient', 'doctor', 'admin'), default='patient')
    phone = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Helper function to hash password
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    # Helper function to check hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# -----------------
# 2. Doctor Profile
# -----------------
class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    consultation_fee = db.Column(db.Numeric(10, 2), nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    verification_status = db.Column(db.Enum('pending', 'verified', 'rejected'), default='pending')
    available_slots = db.Column(db.Text, nullable=True) # Ex: 10:00, 11:30
    vacation_mode = db.Column(db.Boolean, default=False)

    # Relation (optional backref for ease)
    user = db.relationship('User', backref=db.backref('doctor_profile', uselist=False))

# -----------------
# 3. Patient Profile
# -----------------
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=True)
    blood_group = db.Column(db.String(5), nullable=True)
    medical_history = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('patient_profile', uselist=False))

# -----------------
# 4. Appointment
# -----------------
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # Refers to Patient User
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # Refers to Doctor User
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    consultation_type = db.Column(db.Enum('Video', 'Clinic'), default='Clinic')
    status = db.Column(db.Enum('pending', 'confirmed', 'completed', 'cancelled'), default='pending')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -----------------
# 5. Prescription
# -----------------
class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False)
    medicines = db.Column(db.Text, nullable=False)
    advice = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
