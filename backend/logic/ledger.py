"""Ledger module for accounting journal entries and chart of accounts."""

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Tuple


@dataclass
class JournalLine:
    """
    Represents a single line in a journal entry.
    
    Attributes:
        account_code: Account code from chart of accounts.
        account_name: Account name/description.
        debit: Debit amount (must be >= 0).
        credit: Credit amount (must be >= 0).
    """
    account_code: str
    account_name: str
    debit: float = 0.0
    credit: float = 0.0
    
    def __post_init__(self):
        """Validate journal line upon creation."""
        # Both debit and credit cannot be non-zero
        if self.debit != 0 and self.credit != 0:
            raise ValueError("A journal line cannot have both debit and credit amounts")
        
        # Amounts must be non-negative
        if self.debit < 0:
            raise ValueError("Debit amount cannot be negative")
        if self.credit < 0:
            raise ValueError("Credit amount cannot be negative")


@dataclass
class JournalEntry:
    """
    Represents a complete journal entry with multiple lines.
    
    Attributes:
        entry_date: Date of the journal entry.
        description: Description of the transaction.
        lines: List of journal lines that make up this entry.
    """
    entry_date: date
    description: str
    lines: List[JournalLine] = field(default_factory=list)
    
    def is_balanced(self) -> bool:
        """
        Check if the journal entry is balanced (total debits = total credits).
        
        Returns:
            True if balanced, False otherwise.
        """
        total_debits = sum(line.debit for line in self.lines)
        total_credits = sum(line.credit for line in self.lines)
        
        # Use a small epsilon for floating point comparison
        return abs(total_debits - total_credits) < 0.01
    
    def validate(self, chart_of_accounts: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
        """
        Validate the journal entry.
        
        Args:
            chart_of_accounts: Optional chart of accounts to validate against.
        
        Returns:
            Tuple of (is_valid, list_of_errors).
        """
        errors = []
        
        # Check if entry is balanced
        if not self.is_balanced():
            errors.append("Entry not balanced: total debits must equal total credits")
        
        # Check if there are any lines
        if not self.lines:
            errors.append("Entry must have at least one line")
        
        # Validate against chart of accounts if provided
        if chart_of_accounts:
            for line in self.lines:
                if line.account_code not in chart_of_accounts:
                    errors.append(f"Invalid account code: {line.account_code}")
        
        return len(errors) == 0, errors


def default_coa() -> Dict[str, str]:
    """
    Return a default chart of accounts.
    
    Returns:
        Dictionary mapping account codes to account names.
    """
    return {
        # Assets (1000-1999)
        "1000": "Cash",
        "1100": "Accounts Receivable",
        "1200": "Inventory",
        "1500": "Equipment",
        "1600": "Accumulated Depreciation",
        
        # Liabilities (2000-2999)
        "2000": "Accounts Payable",
        "2100": "Notes Payable",
        "2200": "Accrued Expenses",
        "2500": "Long-term Debt",
        
        # Equity (3000-3999)
        "3000": "Owner's Equity",
        "3100": "Retained Earnings",
        "3200": "Dividends",
        
        # Revenue (4000-4999)
        "4000": "Service Revenue",
        "4100": "Sales Revenue",
        "4200": "Interest Income",
        
        # Expenses (5000-5999)
        "5000": "Cost of Goods Sold",
        "5100": "Salaries Expense",
        "5200": "Rent Expense",
        "5300": "Utilities Expense",
        "5400": "Depreciation Expense",
        "5500": "Interest Expense",
    }
