import os
from huggingface_hub import InferenceClient

token = "hf_INVALID_TOKEN"
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=token)

try:
    print("Testing HuggingFace connection...")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Hola"}],
        max_tokens=10
    )
    print("Success!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Failed: {e}")
