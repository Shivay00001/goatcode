"""
GOATCODE - LLM Interface Module

Unified interface for multiple LLM providers including:
- Local Ollama models
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- And more...
"""

import json
import os
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, AsyncIterator
from dataclasses import dataclass
import aiohttp
import openai
from anthropic import AsyncAnthropic


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = None


class BaseLLMInterface(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate a single response."""
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming response."""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Chat completion with message history."""
        pass


class OllamaInterface(BaseLLMInterface):
    """Interface for local Ollama models."""
    
    def __init__(
        self,
        model: str = "llama2",
        base_url: str = "http://localhost",
        port: int = 11434
    ):
        self.model = model
        self.base_url = base_url
        self.port = port
        self.api_url = f"{base_url}:{port}/api"
    
    async def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/tags",
                    timeout=aiohttp.ClientTimeout(total=3)
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def list_models(self) -> List[str]:
        """List available local models."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        return [m['name'] for m in data.get('models', [])]
                    return []
        except:
            return []
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Ollama."""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        
        if system:
            payload["system"] = system
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/generate",
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"Ollama error: {response.status}")
                
                data = await response.json()
                
                return LLMResponse(
                    content=data.get('response', ''),
                    provider='ollama',
                    model=self.model,
                    tokens_used=data.get('eval_count'),
                    finish_reason='stop' if data.get('done') else None,
                    metadata={
                        'total_duration': data.get('total_duration'),
                        'load_duration': data.get('load_duration'),
                    }
                )
    
    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming completion."""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
            }
        }
        
        if system:
            payload["system"] = system
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/generate",
                json=payload
            ) as response:
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line)
                            if 'response' in data:
                                yield data['response']
                            if data.get('done'):
                                break
                        except json.JSONDecodeError:
                            continue
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Chat completion with message history."""
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/chat",
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"Ollama error: {response.status}")
                
                data = await response.json()
                
                return LLMResponse(
                    content=data['message'].get('content', ''),
                    provider='ollama',
                    model=self.model,
                    tokens_used=data.get('eval_count'),
                    finish_reason='stop' if data.get('done') else None
                )


class OpenAIInterface(BaseLLMInterface):
    """Interface for OpenAI API."""
    
    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using OpenAI."""
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return LLMResponse(
            content=response.choices[0].message.content or "",
            provider='openai',
            model=self.model,
            tokens_used=response.usage.total_tokens if response.usage else None,
            finish_reason=response.choices[0].finish_reason
        )
    
    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming completion."""
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True,
            **kwargs
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Chat completion with message history."""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return LLMResponse(
            content=response.choices[0].message.content or "",
            provider='openai',
            model=self.model,
            tokens_used=response.usage.total_tokens if response.usage else None,
            finish_reason=response.choices[0].finish_reason
        )


class AnthropicInterface(BaseLLMInterface):
    """Interface for Anthropic Claude API."""
    
    def __init__(
        self,
        model: str = "claude-3-opus-20240229",
        api_key: Optional[str] = None
    ):
        self.model = model
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        
        if not self.api_key:
            raise ValueError("Anthropic API key required")
        
        self.client = AsyncAnthropic(api_key=self.api_key)
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Claude."""
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens or 4096,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        return LLMResponse(
            content=response.content[0].text if response.content else "",
            provider='anthropic',
            model=self.model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens
            if response.usage else None,
            finish_reason=response.stop_reason
        )
    
    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming completion."""
        
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=4096,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        ) as stream:
            async for text in stream.text_stream:
                yield text
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Chat completion with message history."""
        
        # Convert to Claude format
        claude_messages = []
        for msg in messages:
            claude_messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens or 4096,
            temperature=temperature,
            messages=claude_messages,
            **kwargs
        )
        
        return LLMResponse(
            content=response.content[0].text if response.content else "",
            provider='anthropic',
            model=self.model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens
            if response.usage else None
        )


class LLMRouter:
    """Routes requests to appropriate LLM provider with fallback support."""
    
    def __init__(self, providers: List[BaseLLMInterface]):
        self.providers = providers
        self.current_provider = 0
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate with automatic fallback."""
        
        last_error = None
        
        for i in range(len(self.providers)):
            provider_idx = (self.current_provider + i) % len(self.providers)
            provider = self.providers[provider_idx]
            
            try:
                response = await provider.generate(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                # Update current provider on success
                self.current_provider = provider_idx
                return response
            except Exception as e:
                last_error = e
                continue
        
        raise Exception(f"All providers failed. Last error: {last_error}")


def create_llm_interface(
    provider: str = "ollama",
    model: Optional[str] = None,
    **kwargs
) -> BaseLLMInterface:
    """
    Factory function to create LLM interface.
    
    Args:
        provider: 'ollama', 'openai', 'anthropic'
        model: Model name
        **kwargs: Additional provider-specific options
    
    Returns:
        Configured LLM interface
    """
    if provider == "ollama":
        return OllamaInterface(
            model=model or "llama2",
            base_url=kwargs.get('base_url', 'http://localhost'),
            port=kwargs.get('port', 11434)
        )
    
    elif provider == "openai":
        return OpenAIInterface(
            model=model or "gpt-4",
            api_key=kwargs.get('api_key'),
            base_url=kwargs.get('base_url')
        )
    
    elif provider == "anthropic":
        return AnthropicInterface(
            model=model or "claude-3-opus-20240229",
            api_key=kwargs.get('api_key')
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


def create_multi_provider_router(
    config: List[Dict[str, Any]]
) -> LLMRouter:
    """
    Create a router with multiple providers for fallback.
    
    Args:
        config: List of provider configs, e.g.:
            [
                {'provider': 'ollama', 'model': 'llama2'},
                {'provider': 'openai', 'model': 'gpt-3.5-turbo'}
            ]
    
    Returns:
        LLMRouter instance
    """
    providers = []
    for cfg in config:
        provider = create_llm_interface(**cfg)
        providers.append(provider)
    
    return LLMRouter(providers)
