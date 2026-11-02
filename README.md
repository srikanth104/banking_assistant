tool_results = [
    {
        "tool_call_id": "call_balance",
        "content": {
            "status": "success",
            "balance": 25000,
            "currency": "INR"
        }
    },
    {
        "tool_call_id": "call_transactions",
        "content": {
            "status": "error",
            "error_code": "SERVICE_TIMEOUT",
            "retryable": True
        }
    }
]


Execution: Should independent tools run concurrently?
Failure policy: Can one tool fail without failing the entire request?
Response policy: Is the LLM allowed to provide a partial answer?


asyncio.sleep() suspends the current coroutine, allowing the event loop to run the other banking operation.