from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, Notification

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """Fetch all notifications for the current patient"""
    current_user = get_jwt_identity()
    notifications = Notification.query.filter_by(patient_id=current_user['id']).order_by(Notification.created_at.desc()).all()
    
    res = []
    for n in notifications:
        res.append({
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "is_read": n.is_read,
            "created_at": str(n.created_at)
        })
    return jsonify(res), 200

@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get count of unread notifications"""
    current_user = get_jwt_identity()
    count = Notification.query.filter_by(patient_id=current_user['id'], is_read=False).count()
    return jsonify({"unread_count": count}), 200

@notification_bp.route('/read/<int:id>', methods=['PUT'])
@jwt_required()
def mark_as_read(id):
    """Mark a specific notification as read"""
    current_user = get_jwt_identity()
    notification = Notification.query.filter_by(id=id, patient_id=current_user['id']).first()
    
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
        
    notification.is_read = True
    db.session.commit()
    return jsonify({"message": "Notification marked as read"}), 200

@notification_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_as_read():
    """Mark all notifications for the current user as read"""
    current_user = get_jwt_identity()
    db.session.query(Notification).filter_by(patient_id=current_user['id'], is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({"message": "All notifications marked as read"}), 200
