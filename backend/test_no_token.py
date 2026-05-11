import os
from huggingface_hub import InferenceClient

print("Testing HF with NO token...")
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2")

try:
    print("Testing chat_completion...")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")
