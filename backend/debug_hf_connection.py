import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

token = os.getenv("HF_TOKEN")
model = "mistralai/Mistral-7B-Instruct-v0.2"

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

try:
    print("\nTesting text_generation...")
    response = client.text_generation(
        "User: Say hello in one word\nAssistant:",
        max_new_tokens=10
    )
    print("text_generation Success!")
    print(f"Response: {response}")
except Exception as e:
    print(f"text_generation Failed: {e}")
