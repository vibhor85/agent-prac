from constants import TOOL_GET_ACCOUNT_BALANCE, TOOL_GET_MONTHLY_EXPENSE
from typing import Any

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": TOOL_GET_MONTHLY_EXPENSE,
            "description": "Return the monthly expense report for a given month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {
                        "type": "string",
                        "description": "The month to retrieve expenses for, e.g. 'May'.",
                    }
                },
                "required": ["month"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": TOOL_GET_ACCOUNT_BALANCE,
            "description": "Return the user account balance summary.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "The account identifier to query.",
                    }
                },
                "required": ["account_id"],
            },
        },
    }
]


def get_monthly_expense(month: str = "this month") -> dict[str, Any]:
    """Return dummy monthly expense data for the requested month."""
    print(f"[log] getMonthlyExpense called with month={month}")
    dummy_data = {
        "month": month,
        "currency": "USD",
        "total_spent": 1284.72,
        "categories": [
            {"name": "groceries", "amount": 432.10},
            {"name": "utilities", "amount": 210.45},
            {"name": "subscriptions", "amount": 95.00},
            {"name": "dining", "amount": 187.22},
            {"name": "transportation", "amount": 135.95},
        ],
    }
    print(f"[log] Returning dummy expense data: {dummy_data}")
    return dummy_data


def get_account_balance(account_id: str) -> dict[str, Any]:
    """Return dummy account balance data for the requested account."""
    print(f"[log] getAccountBalance called with account_id={account_id}")
    dummy_balance = {
        "account_id": account_id,
        "currency": "USD",
        "available_balance": 5230.40,
        "pending": 120.00,
        "last_updated": "2026-05-23T12:00:00Z",
    }
    print(f"[log] Returning dummy account balance: {dummy_balance}")
    return dummy_balance


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Dispatch tool calls to the matching local implementation."""
    print(
        f"[log] execute_tool called with tool_name={tool_name}, arguments={arguments}")
    if tool_name == TOOL_GET_MONTHLY_EXPENSE:
        month = arguments.get("month", "this month")
        return get_monthly_expense(month)
    if tool_name == TOOL_GET_ACCOUNT_BALANCE:
        account_id = arguments.get("account_id", "unknown")
        return get_account_balance(account_id)

    raise RuntimeError(f"Unknown tool requested: {tool_name}")
