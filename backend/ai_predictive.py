"""AI predictive analytics module."""

from typing import Any, Dict, List


def detect_anomalies(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect anomalies in transaction data.
    
    Args:
        transactions: List of transaction dictionaries with 'amount' field.
    
    Returns:
        List of transactions identified as anomalies.
    """
    if not transactions:
        return []
    
    # Simple anomaly detection: flag transactions > 2x median amount
    amounts = [t.get('amount', 0) for t in transactions]
    if not amounts:
        return []
    
    sorted_amounts = sorted(amounts)
    median = sorted_amounts[len(sorted_amounts) // 2]
    threshold = median * 2
    
    anomalies = [t for t in transactions if t.get('amount', 0) > threshold]
    return anomalies


def predict_tax_liability(transactions: List[Dict[str, Any]]) -> float:
    """
    Predict tax liability based on transaction data.
    
    Args:
        transactions: List of transaction dictionaries with 'amount' and 'type' fields.
    
    Returns:
        Total expense amount (potential tax liability).
    """
    if not transactions:
        return 0.0
    
    # Calculate total expenses
    total_expenses = 0.0
    for txn in transactions:
        amount = txn.get('amount', 0)
        txn_type = txn.get('type', '')
        
        if txn_type == 'expense':
            total_expenses += amount
    
    return total_expenses


def classify_document(text: str) -> str:
    """
    Classify document type based on text content.
    
    Args:
        text: Document text content.
    
    Returns:
        Document classification (e.g., 'invoice', 't4 slip', 'unknown').
    """
    text_lower = text.lower()
    
    if 'invoice' in text_lower:
        return 'invoice'
    elif 't4' in text_lower and ('statement' in text_lower or 'remuneration' in text_lower):
        return 't4 slip'
    else:
        return 'unknown'
