"""
GOATCODE - Deterministic, Tool-Augmented Coding Agent

A production-grade coding agent that beats prompt-only solutions through
real architecture: file indexing, context injection, test→fix loops,
diff patching, token budget management, and memory systems.
"""

__version__ = "1.1.2"
__author__ = "Shivay Singh"
__license__ = "MIT"

from .core.agent import GoatCodeAgent, create_agent, AgentResult
from .llm.interface import (
    create_llm_interface,
    create_multi_provider_router,
    OllamaInterface,
    OpenAIInterface,
    AnthropicInterface
)

__all__ = [
    'GoatCodeAgent',
    'create_agent',
    'AgentResult',
    'create_llm_interface',
    'create_multi_provider_router',
    'OllamaInterface',
    'OpenAIInterface',
    'AnthropicInterface',
]
