
import asyncio
import os
import json
import time

from dotenv import load_dotenv
load_dotenv()

from langfuse import observe, get_client
from langfuse.openai import OpenAI
from banking_tools import get_account_balance, get_recent_transactions

langfuse = get_client()

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_account_balance",
            "description": "Get the authenticated user's account balance",
            "parameters": {
                "type":"object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    }
]

@observe(name="banking_assistant")
def run_assistant(question: str):
    messages = [
        {
            "role" :"system",
            "content": (
                "You are a banking assistant. "
                "Use the account balance tool for balance questions. "
                "Never invent account balances."
            ),
        },
        {"role": "user", "content": question},
    ]
    
    response = client.chat.completions.create(
         model="openai/gpt-oss-120b",
         messages=messages,
         tools=tools,
         tool_choice="auto",
         max_completion_tokens=1000,
    )
    
    message = response.choices[0].message
    
    if not message.tool_calls:
        return message.content
    
    messages.append(message.model_dump(exclude_none=True))
    
    for tool_call in message.tool_calls:
        if tool_call.function.name != "get_account_balance":
            raise ValueError("Unsupported tool")

        arguments = json.loads(tool_call.function.arguments)
        
        if arguments : 
            raise  ValueError("get_account_balance does not take any arguments")
        
        result = get_account_balance("DEMO-C101")
         
        messages.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content": json.dumps(result),  
        })
        
        
    final_response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        max_completion_tokens=500,
    )
    return final_response.choices[0].message.content

@observe(name="parallel_banking_workflow")
async def run_workflow():
    start = time.perf_counter()

    balance, transactions = await asyncio.gather(
        get_account_balance("DEMO-C101"),
        get_recent_transactions("DEMO-C101"),
    )

    elapsed = time.perf_counter() - start

    print("Balance:", balance)
    print("Transactions:", transactions)
    print(f"Elapsed: {elapsed:.2f} seconds")
    

if __name__ == "__main__":
    try:
      asyncio.run(run_workflow())
    finally:
        langfuse.flush()
        

    
