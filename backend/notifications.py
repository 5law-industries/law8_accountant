"""Notifications module for user messaging."""

from typing import Any, Dict, List
from datetime import datetime
import uuid


# In-memory storage for notifications (for testing purposes)
_notifications_store: Dict[str, List[Dict[str, Any]]] = {}


def send_notification(
    user_id: str,
    message: str,
    notif_type: str = "info"
) -> None:
    """
    Send a notification to a user.
    
    Args:
        user_id: User identifier.
        message: Notification message.
        notif_type: Type of notification (info, warning, error, etc.).
    """
    if user_id not in _notifications_store:
        _notifications_store[user_id] = []
    
    notification = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "message": message,
        "type": notif_type,
        "timestamp": datetime.now().isoformat(),
        "read": False,
    }
    
    _notifications_store[user_id].append(notification)


def get_user_notifications(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all notifications for a user.
    
    Args:
        user_id: User identifier.
    
    Returns:
        List of notification dictionaries.
    """
    return _notifications_store.get(user_id, [])


def mark_all_read(user_id: str) -> None:
    """
    Mark all notifications as read for a user.
    
    Args:
        user_id: User identifier.
    """
    if user_id in _notifications_store:
        for notification in _notifications_store[user_id]:
            notification["read"] = True
