import time 
from langfuse import observe

@observe(name="get_account_balance")
async def get_account_balance(customer_id: str) -> dict:
    time.sleep(1)  # Simulate a delay in fetching the account balance
    return {
        "customer_id": customer_id,
        "balance": 25000,
        "currency": "INR"
    }

@observe(name="get_recent_transactions")
async def get_recent_transactions(customer_id: str) -> list:
    time.sleep(3)  # Simulate a delay in fetching recent transactions
    return [
        {
            "customer_id": customer_id,
            "transactions": [
                {"amount": -500, "type": "debit"},
                {"amount": 2000, "type": "credit"},
            ],
        }
    ]