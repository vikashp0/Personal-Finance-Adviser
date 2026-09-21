"""
finance_utils.py
Calculates financial ratios and remaining balance.
"""

def calculate_ratios(income: float, expenses: float, savings: float, debt: float) -> dict:
    if income <= 0:
        return {
            "valid": False,
            "error": "Income must be greater than zero.",
            "expense_ratio": 0.0,
            "savings_ratio": 0.0,
            "debt_ratio": 0.0,
            "remaining_balance": 0.0
        }

    expense_ratio = min((expenses / income) * 100, 100.0)
    savings_ratio = min((savings / income) * 100, 100.0)
    debt_ratio = min((debt / income) * 100, 100.0)
    remaining_balance = income - (expenses + savings + debt)

    return {
        "valid": True,
        "error": None,
        "expense_ratio": round(expense_ratio, 2),
        "savings_ratio": round(savings_ratio, 2),
        "debt_ratio": round(debt_ratio, 2),
        "remaining_balance": round(remaining_balance, 2)
    }