"""
GOATCODE - Command Line Interface

Main entry point for the GOATCODE coding agent system.
Supports both interactive and batch modes.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import create_agent, AgentStatus
from llm.interface import create_llm_interface


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


async def interactive_mode(agent, project_path: str):
    """Run in interactive REPL mode."""
    print("\n" + "="*60)
    print("🐐 GOATCODE - Production-Grade Coding Agent")
    print("="*60)
    print("\nInteractive Mode - Type your coding requests")
    print("Commands: /help, /exit, /status, /models")
    print("-"*60 + "\n")
    
    while True:
        try:
            prompt = input("📝 > ").strip()
            
            if not prompt:
                continue
            
            # Handle commands
            if prompt.startswith('/'):
                if prompt == '/exit':
                    print("\n👋 Goodbye!")
                    break
                elif prompt == '/help':
                    print_help()
                elif prompt == '/status':
                    print(f"Status: {agent.status.value}")
                elif prompt == '/models':
                    await list_models(agent.llm)
                continue
            
            # Execute task
            print("\n🚀 Starting execution...\n")
            result = await agent.execute(prompt, project_path)
            
            # Display results
            display_result(result)
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def print_help():
    """Print help message."""
    print("""
Available Commands:
  /help     - Show this help
  /exit     - Exit the program
  /status   - Show agent status
  /models   - List available models

Usage:
  Simply type your coding request, e.g.:
  - "Create a Python function to calculate fibonacci"
  - "Add error handling to src/utils.py"
  - "Write unit tests for the auth module"
""")


async def list_models(llm):
    """List available models."""
    try:
        if hasattr(llm, 'list_models'):
            models = await llm.list_models()
            print("\n📚 Available Models:")
            for model in models:
                print(f"  • {model}")
        else:
            print(f"\n📚 Current Model: {llm.model}")
    except Exception as e:
        print(f"❌ Could not list models: {e}")


def display_result(result):
    """Display execution result."""
    print("\n" + "="*60)
    print(f"Status: {result.status.value.upper()}")
    print("="*60)
    
    if result.error_message:
        print(f"\n❌ Error: {result.error_message}")
        return
    
    print(f"\n📊 Analysis Summary:")
    print(f"{result.analysis_summary}\n")
    
    print(f"📋 Implementation Plan:")
    for i, step in enumerate(result.implementation_plan, 1):
        print(f"  {i}. {step}")
    
    print(f"\n📝 Files Modified:")
    for file_info in result.files_modified:
        action = file_info.get('action', 'modify')
        path = file_info.get('path', 'unknown')
        print(f"  [{action.upper()}] {path}")
    
    print(f"\n✅ Validation Report:")
    validation = result.validation_report
    if validation.get('all_passed'):
        print("  ✓ All validations passed")
    else:
        print(f"  ⚠️  Issues found: {validation.get('failures', [])}")
    
    print(f"\n🎯 Confidence Score: {result.confidence_score:.0%}")
    
    # Show execution logs
    if result.logs:
        print(f"\n📜 Execution Logs:")
        for log in result.logs[-5:]:  # Show last 5 logs
            print(f"  [{log.phase.value}] {log.message}")
    
    print("\n" + "="*60 + "\n")


async def batch_mode(agent, prompt: str, project_path: str, output: Optional[str]):
    """Run in batch mode for single execution."""
    print(f"🐐 GOATCODE - Processing: {prompt[:50]}...")
    
    result = await agent.execute(prompt, project_path)
    
    # Output results
    output_data = {
        'status': result.status.value,
        'analysis_summary': result.analysis_summary,
        'implementation_plan': result.implementation_plan,
        'files_modified': result.files_modified,
        'validation_report': result.validation_report,
        'confidence_score': result.confidence_score,
        'error': result.error_message
    }
    
    if output:
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"✅ Results saved to: {output}")
    else:
        print(json.dumps(output_data, indent=2))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='GOATCODE - Production-Grade Coding Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with Ollama
  python -m goatcode --provider ollama --model llama2
  
  # Batch mode with OpenAI
  python -m goatcode --provider openai --model gpt-4 -p "Create a REST API"
  
  # With specific project
  python -m goatcode --provider ollama --project /path/to/project
        """
    )
    
    parser.add_argument(
        '--provider',
        choices=['ollama', 'openai', 'anthropic'],
        default='ollama',
        help='LLM provider (default: ollama)'
    )
    
    parser.add_argument(
        '--model',
        default='llama2',
        help='Model name (default: llama2 for Ollama, gpt-4 for OpenAI)'
    )
    
    parser.add_argument(
        '--project',
        default='.',
        help='Project path (default: current directory)'
    )
    
    parser.add_argument(
        '-p', '--prompt',
        help='Single prompt for batch mode (if not provided, runs interactive)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file for batch mode results (JSON)'
    )
    
    parser.add_argument(
        '--api-key',
        help='API key for SaaS providers (or set env var)'
    )
    
    parser.add_argument(
        '--ollama-url',
        default='http://localhost:11434',
        help='Ollama server URL (default: http://localhost:11434)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Validate project path
    project_path = Path(args.project).resolve()
    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        sys.exit(1)
    
    print(f"📁 Project: {project_path}")
    print(f"🤖 Provider: {args.provider}")
    print(f"🧠 Model: {args.model}")
    
    # Parse Ollama URL
    if args.provider == 'ollama':
        from urllib.parse import urlparse
        parsed = urlparse(args.ollama_url)
        ollama_config = {
            'base_url': f"{parsed.scheme}://{parsed.hostname}",
            'port': parsed.port or 11434
        }
    else:
        ollama_config = {}
    
    # Create agent
    try:
        agent = create_agent(
            llm_provider=args.provider,
            llm_model=args.model,
            project_path=str(project_path),
            config={
                'api_key': args.api_key,
                **ollama_config
            }
        )
        
        # Check LLM availability
        print("\n🔌 Checking LLM connection...")
        if hasattr(agent.llm, 'is_available'):
            import asyncio
            loop = asyncio.get_event_loop()
            is_available = loop.run_until_complete(agent.llm.is_available())
            if not is_available:
                print(f"❌ Cannot connect to {args.provider}")
                if args.provider == 'ollama':
                    print("\n💡 Make sure Ollama is running:")
                    print("   ollama serve")
                    print("\n💡 Or pull a model:")
                    print("   ollama pull llama2")
                sys.exit(1)
        
        print(f"✅ Connected to {args.provider}\n")
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        sys.exit(1)
    
    # Run in appropriate mode
    try:
        if args.prompt:
            # Batch mode
            asyncio.run(batch_mode(agent, args.prompt, str(project_path), args.output))
        else:
            # Interactive mode
            asyncio.run(interactive_mode(agent, str(project_path)))
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
