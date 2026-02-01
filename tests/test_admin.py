
# tests/test_admin.py
import sys
import os
import pytest
# Ensure backend is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.admin import list_users, get_logs, get_system_health

def test_list_users():
    users = list_users()
    assert isinstance(users, list)
    assert any("email" in u for u in users)

def test_get_logs():
    logs = get_logs()
    assert isinstance(logs, list)
    assert all("timestamp" in l for l in logs)

def test_get_system_health():
    health = get_system_health()
    assert isinstance(health, dict)
    assert health["status"] == "OK"
