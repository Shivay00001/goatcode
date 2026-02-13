import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.interface import OllamaInterface

async def check_ollama():
    print("Checking local Ollama status...")
    client = OllamaInterface()
    
    is_up = await client.is_available()
    if not is_up:
        print("[!] Ollama is not running on http://localhost:11434")
        return

    print("[SUCCESS] Ollama is up and running!")
    
    models = await client.list_models()
    if not models:
        print("[WARN] No models found in Ollama. Please pull a model (e.g., 'ollama pull llama3' or 'ollama pull codellama').")
    else:
        print(f"Available models ({len(models)}):")
        for model in models:
            print(f"  - {model}")

if __name__ == "__main__":
    asyncio.run(check_ollama())
