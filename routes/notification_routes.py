from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from models import db
from models.notification_model import Notification

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/api/notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(user_email=current_user.email, is_read=False).all()
    return jsonify({'notifications': [{'id': notification.id, 'message': notification.message} for notification in notifications]})

@notification_bp.route('/api/notifications/mark-as-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification and notification.user_email == current_user.email:
        notification.is_read = True
        db.session.commit()
        return jsonify({'message': 'تم وضع علامة على الإشعار كمقروء'}), 200
    else:
        return jsonify({'message': 'لم يتم العثور على الإشعار'}), 404

@notification_bp.route('/api/notifications/clear-all', methods=['POST'])
@login_required
def clear_all():
    notifications = Notification.query.filter_by(user_email=current_user.email, is_read=False).all()
    for notification in notifications:
        notification.is_read = True
    db.session.commit()
    return jsonify({'message': 'تم مسح جميع الإشعارات'}), 200