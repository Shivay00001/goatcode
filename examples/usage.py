#!/usr/bin/env python3
"""
GOATCODE - Example Usage

This script demonstrates how to use the GOATCODE agent programmatically.
"""

import asyncio
from goatcode import create_agent


async def example_basic_usage():
    """Example: Basic usage with Ollama."""
    
    # Create agent with Ollama (local model)
    agent = create_agent(
        llm_provider='ollama',
        llm_model='llama2',
        project_path='./my_project',
        config={
            'max_validation_retries': 3,
            'enable_memory': True
        }
    )
    
    # Execute a coding task
    result = await agent.execute(
        prompt="Create a Python function to calculate fibonacci numbers with memoization",
        project_path='./my_project'
    )
    
    # Check results
    if result.status.value == 'success':
        print("✅ Task completed successfully!")
        print(f"Confidence: {result.confidence_score:.0%}")
        print(f"Files modified: {len(result.files_modified)}")
        
        for file_info in result.files_modified:
            print(f"  - {file_info['path']}")
    else:
        print(f"❌ Task failed: {result.error_message}")


async def example_with_openai():
    """Example: Using OpenAI API."""
    
    agent = create_agent(
        llm_provider='openai',
        llm_model='gpt-4',
        project_path='./my_project',
        config={
            'api_key': 'your-api-key-here'  # Or set OPENAI_API_KEY env var
        }
    )
    
    result = await agent.execute(
        prompt="Refactor the auth module to use dependency injection",
        project_path='./my_project'
    )
    
    print(result)


async def example_batch_processing():
    """Example: Processing multiple tasks."""
    
    agent = create_agent(
        llm_provider='ollama',
        llm_model='codellama'
    )
    
    tasks = [
        "Create a REST API endpoint for user registration",
        "Add input validation to the login endpoint",
        "Write unit tests for the auth module",
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n{'='*60}")
        print(f"Task {i}/{len(tasks)}: {task}")
        print('='*60)
        
        result = await agent.execute(task, project_path='./my_project')
        
        print(f"Status: {result.status.value}")
        print(f"Confidence: {result.confidence_score:.0%}")


async def example_with_fallback():
    """Example: Multi-provider with automatic fallback."""
    
    from goatcode.llm.interface import create_multi_provider_router
    
    # Create router with multiple providers
    router = create_multi_provider_router([
        {'provider': 'ollama', 'model': 'llama2'},
        {'provider': 'openai', 'model': 'gpt-3.5-turbo', 'api_key': 'your-key'},
    ])
    
    # The router will try Ollama first, then fall back to OpenAI if it fails
    response = await router.generate(
        prompt="Create a Python class for a simple HTTP client",
        temperature=0.7
    )
    
    print(f"Response from: {response.provider}")
    print(response.content)


def main():
    """Run examples."""
    print("🐐 GOATCODE - Example Usage\n")
    print("Choose an example:")
    print("1. Basic usage with Ollama")
    print("2. Using OpenAI API")
    print("3. Batch processing")
    print("4. Multi-provider with fallback")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    examples = {
        '1': example_basic_usage,
        '2': example_with_openai,
        '3': example_batch_processing,
        '4': example_with_fallback,
    }
    
    if choice in examples:
        asyncio.run(examples[choice]())
    else:
        print("Invalid choice")


if __name__ == '__main__':
    main()
