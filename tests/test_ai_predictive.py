
# tests/test_ai_predictive.py
import sys
import os
import pytest
# Ensure backend is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.ai_predictive import detect_anomalies, predict_tax_liability, classify_document

def test_detect_anomalies():
    txns = [
        {'amount': 5000},
        {'amount': 15000},
        {'amount': 200}
    ]
    anomalies = detect_anomalies(txns)
    assert len(anomalies) == 1
    assert anomalies[0]['amount'] == 15000

def test_predict_tax_liability():
    txns = [
        {'amount': 100, 'type': 'expense'},
        {'amount': 200, 'type': 'income'},
        {'amount': 50, 'type': 'expense'}
    ]
    assert predict_tax_liability(txns) == 150

def test_classify_document():
    assert classify_document('This is an invoice for services.') == 'invoice'
    assert classify_document('T4 Statement of Remuneration Paid') == 't4 slip'
    assert classify_document('Random text') == 'unknown'
