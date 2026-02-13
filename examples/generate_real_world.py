import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.interface import OllamaInterface

async def generate_code():
    print("[INIT] Starting real-world code generation demo using local Ollama model...")
    
    # Initialize with local Ollama
    # Using llama3.2:latest as it was found in the inventory
    llm = OllamaInterface(model="llama3.2:latest")
    
    prompt = """
    Create a production-ready Python module for a User Management System.
    The module should include:
    1. A User dataclass with fields: id, username, email, created_at.
    2. A UserRepository class that handles:
       - Saving a user to a local SQLite database.
       - Fetching a user by ID.
       - Listing all users.
    3. Input validation for the email address using regex.
    4. Proper error handling with custom exceptions.
    5. Clean documentation (docstrings).
    
    Output ONLY THE CODE. No conversational text. Wrap the code in markdown blocks.
    """
    
    print(f"[PROCESS] Sending prompt to llama3.2:latest...")
    
    try:
        response = await llm.generate(
            prompt=prompt,
            system="You are an expert Python developer who writes clean, production-grade code.",
            temperature=0.2
        )
        
        content = response.content
        print("\n" + "="*50)
        print("GENERATED CODE:")
        print("="*50)
        print(content)
        print("="*50 + "\n")
        
        # Save the generated code
        output_path = os.path.join(os.path.dirname(__file__), 'generated_user_system.py')
        
        # Extract content from markdown if present
        if "```" in content:
            import re
            # Try to find a python block first
            python_match = re.search(r'```python\n(.*?)```', content, re.DOTALL)
            if python_match:
                content = python_match.group(1).strip()
            else:
                # Fallback to any code block
                any_match = re.search(r'```.*?\n(.*?)```', content, re.DOTALL)
                if any_match:
                    content = any_match.group(1).strip()
        
        with open(output_path, 'w') as f:
            f.write(content)
            
        print(f"[SUCCESS] Generated code saved to: {output_path}")
        
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")

if __name__ == "__main__":
    asyncio.run(generate_code())
