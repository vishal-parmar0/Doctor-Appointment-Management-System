import google.generativeai as genai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Appointment, Prescription, Doctor, Patient, db
from config import Config
from datetime import datetime, timedelta
import base64
import re
import json

ai_bp = Blueprint('ai', __name__)
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """You are MediAI, a professional, warm, and intelligent personal health assistant embedded inside MediBook — a doctor appointment platform.

YOU HAVE ACCESS TO THE PATIENT'S REAL DATA (provided in every message):
- Their upcoming and past appointments
- Their active prescriptions
- Their assigned doctors and specialties

YOUR CAPABILITIES:
1. SYMPTOM TRIAGE: When patient describes symptoms, ask 1-2 smart follow-up questions, then recommend the right specialist. Always end triage with: [BOOK_SPECIALIST: <specialty_name>] on a new line so the frontend can render a Book Now button.

2. PRESCRIPTION EXPLAINER: Explain medicines in simple language. Cover: what it treats, how to take it, side effects, what to avoid. Always end with: "Please consult your doctor before making changes."

3. APPOINTMENT AWARENESS: You know their schedule. Reference it naturally. Example: "Your appointment with Dr. Smith is tomorrow at 10am — would you like to prepare for it?"

4. MEDICINE GUIDANCE: When asked about their medicines or dosage timing, reference their actual medicine list provided in context.

5. HEALTH SUMMARY: When asked for EHR or health summary, generate a clean readable summary from their appointments and prescriptions.

6. EMERGENCY DETECTION: If the message contains any of these keywords: chest pain, heart attack, can't breathe, unconscious, stroke, seizure, severe bleeding, poisoning, overdose, suicide → Immediately respond ONLY with: [EMERGENCY_DETECTED]

7. LAB REPORT / DOCUMENT: If a document is provided, read and explain values in simple patient-friendly language.

TONE: Warm, reassuring, but professional. Never diagnose—only suggest specialists or recommend consulting doctors.
FORMAT: If recommending a specialist, always include [BOOK_SPECIALIST: <specialty>] on its own line."""

EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', "can't breathe", 'unconscious', 'stroke',
    'seizure', 'severe bleeding', 'poisoning', 'overdose', 'suicide'
]

@ai_bp.route('/api/ai/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        # Parse JWT identity (handle both string and dict formats)
        raw_identity = get_jwt_identity()
        try:
            identity = json.loads(raw_identity) if isinstance(raw_identity, str) else raw_identity
        except:
            identity = raw_identity
            
        user_id = identity['id']
        data = request.get_json()

        user_message = data.get('message', '').strip()
        chat_history = data.get('history', [])
        user_name = data.get('user_name', 'Patient')
        medicines = data.get('medicines', [])
        document_base64 = data.get('document', None)
        document_mime = data.get('document_mime', None)

        if not user_message and not document_base64:
            return jsonify({'error': 'Message is required'}), 400

        # Emergency detection
        msg_lower = user_message.lower()
        for keyword in EMERGENCY_KEYWORDS:
            if keyword in msg_lower:
                return jsonify({'reply': '[EMERGENCY_DETECTED]', 'status': 'emergency'}), 200

        # Build patient context from DB
        now = datetime.utcnow()
        seven_days = now + timedelta(days=7)

        upcoming = db.session.query(Appointment).filter(
            Appointment.patient_id == user_id,
            Appointment.status.in_(['confirmed', 'pending']),
            Appointment.appointment_date >= now,
            Appointment.appointment_date <= seven_days
        ).all()

        past = db.session.query(Appointment).filter(
            Appointment.patient_id == user_id,
            Appointment.status == 'completed'
        ).order_by(Appointment.appointment_date.desc()).limit(5).all()

        prescriptions = db.session.query(Prescription).filter(
            Prescription.appointment_id.in_(
                db.session.query(Appointment.id).filter(
                    Appointment.patient_id == user_id
                ).all()
            )
        ).order_by(Prescription.created_at.desc()).limit(10).all()

        context = f"\n--- PATIENT CONTEXT ---\nName: {user_name}\nUpcoming Appointments (next 7 days): "
        if upcoming:
            for apt in upcoming:
                doctor = Doctor.query.join(Appointment).filter(Appointment.id == apt.id).first()
                context += f"\n- {apt.appointment_date} at {apt.appointment_time} ({apt.consultation_type})"
        else:
            context += "None"

        context += "\n\nRecent Visits: "
        if past:
            for apt in past:
                context += f"\n- {apt.appointment_date} ({apt.status})"
        else:
            context += "None"

        context += "\n\nActive Medicines: "
        if medicines:
            for med in medicines:
                context += f"\n- {med}"
        else:
            context += "None"

        # Handle document
        doc_text = ""
        if document_base64:
            try:
                doc_data = base64.b64decode(document_base64)
                if 'pdf' in document_mime:
                    doc_text = f"\n[DOCUMENT: PDF uploaded]\nContent: {doc_data[:500].decode('utf-8', errors='ignore')}"
                elif 'text' in document_mime or 'plain' in document_mime:
                    doc_text = f"\n[DOCUMENT: {document_mime}]\n{doc_data.decode('utf-8')}"
                else:
                    doc_text = f"\n[DOCUMENT: {document_mime}]\n(binary content)"
            except Exception as e:
                doc_text = f"\n[Document parsing error: {str(e)}]"

        # Build Gemini message
        full_message = f"{context}{doc_text}\n\n{user_message}"

        # Convert history for Gemini
        gemini_history = []
        for msg in chat_history:
            if msg.get('role') == 'user':
                gemini_history.append({'role': 'user', 'parts': [msg.get('content', '')]})
            elif msg.get('role') == 'ai':
                gemini_history.append({'role': 'model', 'parts': [msg.get('content', '')]})

        # Call Gemini
        chat_session = model.start_chat(history=gemini_history)
        response = chat_session.send_message(f"{SYSTEM_PROMPT}\n\n{full_message}")
        ai_reply = response.text

        # Detect specialist recommendation
        specialist_match = re.search(r'\[BOOK_SPECIALIST:\s*([^\]]+)\]', ai_reply)
        specialist = specialist_match.group(1).strip() if specialist_match else None

        return jsonify({
            'reply': ai_reply,
            'specialist': specialist,
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
