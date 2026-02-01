# tests/test_ledger.py
import pytest
from datetime import date
from backend.logic.ledger import JournalLine, JournalEntry, default_coa


def test_journal_line_validation():
    # Valid line
    jl = JournalLine(account_code="1000", account_name="Cash", debit=100, credit=0)
    assert jl.debit == 100
    assert jl.credit == 0
    # Invalid: both debit and credit
    with pytest.raises(ValueError):
        JournalLine(account_code="1000", account_name="Cash", debit=100, credit=100)
    # Invalid: negative debit
    with pytest.raises(ValueError):
        JournalLine(account_code="1000", account_name="Cash", debit=-10, credit=0)


def test_journal_entry_balanced():
    coa = default_coa()
    lines = [
        JournalLine(account_code="1000", account_name="Cash", debit=100, credit=0),
        JournalLine(account_code="2000", account_name="Accounts Payable", debit=0, credit=100),
    ]
    je = JournalEntry(entry_date=date.today(), description="Test", lines=lines)
    assert je.is_balanced()
    valid, errors = je.validate(chart_of_accounts=coa)
    assert valid
    assert errors == []


def test_journal_entry_unbalanced():
    lines = [
        JournalLine(account_code="1000", account_name="Cash", debit=100, credit=0),
        JournalLine(account_code="2000", account_name="Accounts Payable", debit=0, credit=50),
    ]
    je = JournalEntry(entry_date=date.today(), description="Test", lines=lines)
    assert not je.is_balanced()
    valid, errors = je.validate()
    assert not valid
    assert any("Entry not balanced" in e for e in errors)
