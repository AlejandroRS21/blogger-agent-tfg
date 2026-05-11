import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

token = os.getenv("HF_TOKEN")
model = "Qwen/Qwen2.5-72B-Instruct"

print(f"Testing HF with token starting with: {token[:10]}...")
print(f"Model: {model}")

client = InferenceClient(model=model, token=token)

try:
    print("Testing chat_completion...")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Say hello in one word"}],
        max_tokens=10
    )
    print("chat_completion Success!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"chat_completion Failed: {e}")
