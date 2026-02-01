# tests/test_notifications.py
import pytest
from backend.notifications import send_notification, get_user_notifications, mark_all_read

def test_send_and_get_notifications():
    user_id = "testuser"
    send_notification(user_id, "Test message 1")
    send_notification(user_id, "Test message 2", notif_type="warning")
    notifs = get_user_notifications(user_id)
    assert len(notifs) >= 2
    assert any(n["message"] == "Test message 1" for n in notifs)
    assert any(n["type"] == "warning" for n in notifs)

def test_mark_all_read():
    user_id = "testuser2"
    send_notification(user_id, "Unread message")
    mark_all_read(user_id)
    notifs = get_user_notifications(user_id)
    assert all(n["read"] for n in notifs)
