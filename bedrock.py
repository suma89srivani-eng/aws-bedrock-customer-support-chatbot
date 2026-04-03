import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

def get_bedrock_response(user_message, chat_history=None):
    if chat_history is None:
        chat_history = []

    client = boto3.client(
        "bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    system_prompt = """
You are an AI customer support assistant.

Your role:
- Help users with customer support related queries
- Be polite, professional, and concise
- Use conversation memory when relevant
- Provide step-by-step help when needed
- If a request is unclear, ask follow-up questions
"""

    messages = []

    for msg in chat_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": user_message
    })

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "system": system_prompt,
        "messages": messages
    }

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
