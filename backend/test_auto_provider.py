import os
from dotenv import load_dotenv
from aphra_blogger.llm.factory import create_llm_provider

load_dotenv()

print(f"GEMINI_API_KEY present: {bool(os.getenv('GEMINI_API_KEY'))}")
print(f"HF_TOKEN present: {bool(os.getenv('HF_TOKEN'))}")

try:
    provider = create_llm_provider(provider="auto")
    print(f"Selected provider in 'auto' mode: {type(provider).__name__}")
    if hasattr(provider, 'config'):
        print(f"Model: {provider.config.model}")
except Exception as e:
    print(f"Error creating provider: {e}")
