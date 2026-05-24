from constants import TOOL_GET_ACCOUNT_BALANCE, TOOL_GET_MONTHLY_EXPENSE, TOOL_ADD_EXPENSE, TOOL_UPDATE_BALANCE
from debug import log
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
    },
    {
        "type": "function",
        "function": {
            "name": TOOL_ADD_EXPENSE,
            "description": "Add a new expense to the user's account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The expense category (e.g., 'groceries', 'utilities').",
                    },
                    "amount": {
                        "type": "number",
                        "description": "The expense amount in USD.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the expense.",
                    }
                },
                "required": ["category", "amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": TOOL_UPDATE_BALANCE,
            "description": "Add or remove money from the user's account balance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "The account identifier to update.",
                    },
                    "amount": {
                        "type": "number",
                        "description": "The amount in USD to add or remove.",
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["add", "remove"],
                        "description": "Whether to add or remove money from the account.",
                    }
                },
                "required": ["account_id", "amount", "operation"],
            },
        },
    }
]


def get_monthly_expense(month: str = "this month") -> dict[str, Any]:
    """Return dummy monthly expense data for the requested month."""
    log(f"[log] getMonthlyExpense called with month={month}")
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
    log(f"[log] Returning dummy expense data: {dummy_data}")
    return dummy_data


def get_account_balance(account_id: str) -> dict[str, Any]:
    """Return dummy account balance data for the requested account."""
    log(f"[log] getAccountBalance called with account_id={account_id}")
    dummy_balance = {
        "account_id": account_id,
        "currency": "USD",
        "available_balance": 5230.40,
        "pending": 120.00,
        "last_updated": "2026-05-23T12:00:00Z",
    }
    log(f"[log] Returning dummy account balance: {dummy_balance}")
    return dummy_balance


def add_expense(category: str, amount: float, description: str = "") -> dict[str, Any]:
    """Add a new expense to the user's account."""
    log(
        f"[log] addExpense called with category={category}, amount={amount}, description={description}")
    result = {
        "status": "success",
        "message": f"Expense of ${amount:.2f} added to {category}",
        "category": category,
        "amount": amount,
        "description": description,
        "timestamp": "2026-05-24T12:00:00Z",
    }
    log(f"[log] Expense added successfully: {result}")
    return result


def update_balance(account_id: str, amount: float, operation: str) -> dict[str, Any]:
    """Add or remove money from the user's account balance."""
    log(
        f"[log] updateBalance called with account_id={account_id}, amount={amount}, operation={operation}")

    if operation == "add":
        new_balance = 5230.40 + amount
        action = "added to"
    elif operation == "remove":
        new_balance = 5230.40 - amount
        action = "removed from"
    else:
        raise ValueError(
            f"Invalid operation: {operation}. Must be 'add' or 'remove'.")

    result = {
        "status": "success",
        "message": f"${amount:.2f} {action} account {account_id}",
        "account_id": account_id,
        "operation": operation,
        "amount": amount,
        "previous_balance": 5230.40,
        "new_balance": new_balance,
        "timestamp": "2026-05-24T12:00:00Z",
    }
    log(f"[log] Balance updated successfully: {result}")
    return result


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Dispatch tool calls to the matching local implementation."""
    log(
        f"[log] execute_tool called with tool_name={tool_name}, arguments={arguments}")
    if tool_name == TOOL_GET_MONTHLY_EXPENSE:
        month = arguments.get("month", "this month")
        return get_monthly_expense(month)
    if tool_name == TOOL_GET_ACCOUNT_BALANCE:
        account_id = arguments.get("account_id", "unknown")
        return get_account_balance(account_id)
    if tool_name == TOOL_ADD_EXPENSE:
        category = arguments.get("category")
        amount = arguments.get("amount")
        description = arguments.get("description", "")
        return add_expense(category, amount, description)
    if tool_name == TOOL_UPDATE_BALANCE:
        account_id = arguments.get("account_id")
        amount = arguments.get("amount")
        operation = arguments.get("operation")
        return update_balance(account_id, amount, operation)

    raise RuntimeError(f"Unknown tool requested: {tool_name}")
