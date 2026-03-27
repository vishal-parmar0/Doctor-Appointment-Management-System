from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Message, Appointment
from sqlalchemy import or_, and_, desc

message_bp = Blueprint('message', __name__)

@message_bp.route('/', methods=['GET'])
@jwt_required()
def get_conversations():
    """List all unique doctors/patients the current user is chatting with"""
    current_user = get_jwt_identity()
    user_id = current_user['id']
    
    # Fetch all messages involving the current user
    messages = Message.query.filter(or_(Message.sender_id == user_id, Message.receiver_id == user_id)).order_by(desc(Message.timestamp)).all()
    
    conversations = {}
    for m in messages:
        other_id = m.receiver_id if m.sender_id == user_id else m.sender_id
        if other_id not in conversations:
            other_user = User.query.get(other_id)
            if not other_user: continue
            unread_count = Message.query.filter_by(sender_id=other_id, receiver_id=user_id, is_read=False).count()
            conversations[other_id] = {
                "other_id": other_id,
                "other_name": other_user.full_name,
                "last_message": m.message,
                "timestamp": str(m.timestamp),
                "unread_count": unread_count
            }
            
    return jsonify(list(conversations.values())), 200

@message_bp.route('/thread/<int:other_id>', methods=['GET'])
@jwt_required()
def get_message_thread(other_id):
    """Fetch all messages between current user and specified other user"""
    current_user = get_jwt_identity()
    user_id = current_user['id']
    
    messages = Message.query.filter(or_(
        and_(Message.sender_id == user_id, Message.receiver_id == other_id),
        and_(Message.sender_id == other_id, Message.receiver_id == user_id)
    )).order_by(Message.timestamp.asc()).all()
    
    res = []
    for m in messages:
        res.append({
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "message": m.message,
            "timestamp": str(m.timestamp),
            "is_read": m.is_read
        })
    return jsonify(res), 200

@message_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send a new message"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    receiver_id = data.get('receiver_id')
    message_text = data.get('message')
    
    if not receiver_id or not message_text:
        return jsonify({"error": "Fields missing"}), 400
        
    # Optional constraint: only allow if appointment exists
    appointment_exists = Appointment.query.filter(or_(
        and_(Appointment.patient_id == current_user['id'], Appointment.doctor_id == receiver_id),
        and_(Appointment.patient_id == receiver_id, Appointment.doctor_id == current_user['id'])
    )).first()
    
    if not appointment_exists:
        return jsonify({"error": "You can only message users you have a scheduled appointment with"}), 403

    new_msg = Message(sender_id=current_user['id'], receiver_id=receiver_id, message=message_text)
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({"message": "Message sent successfully!", "id": new_msg.id}), 201

@message_bp.route('/read/<int:id>', methods=['PUT'])
@jwt_required()
def mark_read(id):
    """Mark specific message as read"""
    current_user = get_jwt_identity()
    msg = Message.query.filter_by(id=id, receiver_id=current_user['id']).first()
    
    if not msg:
        return jsonify({"error": "Message not found"}), 404
        
    msg.is_read = True
    db.session.commit()
    return jsonify({"message": "Message marked as read"}), 200

@message_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_read():
    """Mark all messages for the current user (receiver) as read"""
    current_user = get_jwt_identity()
    db.session.query(Message).filter_by(receiver_id=current_user['id'], is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({"message": "All messages marked as read"}), 200
