"""
GOATCODE - Tool Registry Module

Manages all available tools for the coding agent:
- File operations (read, write, list)
- Project search
- Git operations
- Testing and validation
- Semantic search
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio


@dataclass
class ToolResult:
    """Result from tool execution."""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class BaseTool(ABC):
    """Abstract base class for all tools."""
    
    name: str
    description: str
    parameters: Dict[str, Any]
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool."""
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate parameters against schema."""
        # Basic validation - can be enhanced with JSON Schema
        required = self.parameters.get('required', [])
        return all(param in params for param in required)


class ReadFileTool(BaseTool):
    """Read file contents."""
    
    name = "read_file"
    description = "Read the contents of a file"
    parameters = {
        "required": ["path"],
        "properties": {
            "path": {"type": "string", "description": "Path to the file"},
            "limit": {"type": "integer", "description": "Max lines to read"}
        }
    }
    
    async def execute(self, path: str, limit: Optional[int] = None) -> ToolResult:
        try:
            file_path = Path(path)
            if not file_path.exists():
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"File not found: {path}"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                if limit:
                    lines = f.readlines()[:limit]
                    content = ''.join(lines)
                else:
                    content = f.read()
            
            return ToolResult(
                success=True,
                data=content,
                metadata={
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'lines': content.count('\n')
                }
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class WriteFileTool(BaseTool):
    """Write content to a file."""
    
    name = "write_file"
    description = "Write or overwrite a file"
    parameters = {
        "required": ["path", "content"],
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"}
        }
    }
    
    async def execute(self, path: str, content: str) -> ToolResult:
        try:
            file_path = Path(path)
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Backup existing file
            if file_path.exists():
                backup_path = file_path.with_suffix('.bak')
                backup_path.write_text(file_path.read_text())
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return ToolResult(
                success=True,
                data=str(file_path),
                metadata={'bytes_written': len(content)}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class ListDirectoryTool(BaseTool):
    """List directory contents."""
    
    name = "list_directory"
    description = "List files and directories"
    parameters = {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"},
            "recursive": {"type": "boolean"}
        }
    }
    
    async def execute(
        self,
        path: str,
        recursive: bool = False
    ) -> ToolResult:
        try:
            dir_path = Path(path)
            if not dir_path.exists():
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Directory not found: {path}"
                )
            
            if recursive:
                items = []
                for item in dir_path.rglob('*'):
                    rel_path = item.relative_to(dir_path)
                    items.append({
                        'path': str(rel_path),
                        'type': 'directory' if item.is_dir() else 'file',
                        'size': item.stat().st_size if item.is_file() else None
                    })
            else:
                items = []
                for item in dir_path.iterdir():
                    items.append({
                        'name': item.name,
                        'type': 'directory' if item.is_dir() else 'file',
                        'size': item.stat().st_size if item.is_file() else None
                    })
            
            return ToolResult(success=True, data=items)
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class SearchProjectTool(BaseTool):
    """Search project files."""
    
    name = "search_project"
    description = "Search for files matching a pattern"
    parameters = {
        "required": ["query", "path"],
        "properties": {
            "query": {"type": "string", "description": "Search term"},
            "path": {"type": "string"},
            "file_pattern": {"type": "string"}
        }
    }
    
    async def execute(
        self,
        query: str,
        path: str,
        file_pattern: str = "*"
    ) -> ToolResult:
        try:
            import fnmatch
            
            results = []
            search_path = Path(path)
            
            for file_path in search_path.rglob(file_pattern):
                if file_path.is_file():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                # Find line numbers
                                lines = content.split('\n')
                                matches = []
                                for i, line in enumerate(lines, 1):
                                    if query.lower() in line.lower():
                                        matches.append({
                                            'line': i,
                                            'content': line.strip()
                                        })
                                
                                results.append({
                                    'file': str(file_path.relative_to(search_path)),
                                    'matches': matches[:5]  # Limit matches per file
                                })
                    except:
                        continue
            
            return ToolResult(success=True, data=results[:20])  # Limit total results
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class RunTestsTool(BaseTool):
    """Run project tests."""
    
    name = "run_tests"
    description = "Run test suite"
    parameters = {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"},
            "test_path": {"type": "string"}
        }
    }
    
    async def execute(
        self,
        path: str,
        test_path: Optional[str] = None
    ) -> ToolResult:
        try:
            # Detect test framework
            project_path = Path(path)
            
            # Python
            if (project_path / 'pytest.ini').exists() or \
               (project_path / 'setup.py').exists():
                cmd = ['python', '-m', 'pytest', '-v']
                if test_path:
                    cmd.append(test_path)
            
            # JavaScript/TypeScript
            elif (project_path / 'package.json').exists():
                cmd = ['npm', 'test']
            
            # Flutter
            elif (project_path / 'pubspec.yaml').exists():
                cmd = ['flutter', 'test']
            
            else:
                return ToolResult(
                    success=False,
                    data=None,
                    error="Could not detect test framework"
                )
            
            result = subprocess.run(
                cmd,
                cwd=path,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return ToolResult(
                success=result.returncode == 0,
                data={
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                },
                metadata={'command': ' '.join(cmd)}
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                data=None,
                error="Test execution timed out"
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class RunLinterTool(BaseTool):
    """Run code linter."""
    
    name = "run_linter"
    description = "Run code linting"
    parameters = {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"}
        }
    }
    
    async def execute(self, path: str) -> ToolResult:
        try:
            project_path = Path(path)
            
            # Python - flake8
            if (project_path / 'requirements.txt').exists():
                cmd = ['python', '-m', 'flake8', '.', '--format=json']
            
            # JavaScript - eslint
            elif (project_path / '.eslintrc').exists() or \
                 (project_path / '.eslintrc.js').exists():
                cmd = ['npx', 'eslint', '.', '--format=json']
            
            # Dart/Flutter
            elif (project_path / 'pubspec.yaml').exists():
                cmd = ['flutter', 'analyze', '--format=json']
            
            else:
                return ToolResult(
                    success=False,
                    data=None,
                    error="Could not detect linter"
                )
            
            result = subprocess.run(
                cmd,
                cwd=path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            try:
                issues = json.loads(result.stdout) if result.stdout else []
            except:
                issues = result.stdout
            
            return ToolResult(
                success=result.returncode == 0,
                data=issues,
                metadata={'command': ' '.join(cmd)}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class RunTypecheckTool(BaseTool):
    """Run type checker."""
    
    name = "run_typecheck"
    description = "Run type checking"
    parameters = {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"}
        }
    }
    
    async def execute(self, path: str) -> ToolResult:
        try:
            project_path = Path(path)
            
            # Python - mypy
            if list(project_path.glob('*.py')):
                cmd = ['python', '-m', 'mypy', '.', '--show-error-codes']
            
            # TypeScript
            elif (project_path / 'tsconfig.json').exists():
                cmd = ['npx', 'tsc', '--noEmit']
            
            # Dart
            elif (project_path / 'pubspec.yaml').exists():
                cmd = ['dart', 'analyze']
            
            else:
                return ToolResult(
                    success=True,
                    data="No type checker configured",
                    metadata={'note': 'No type checker found'}
                )
            
            result = subprocess.run(
                cmd,
                cwd=path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return ToolResult(
                success=result.returncode == 0,
                data=result.stdout,
                error=result.stderr if result.returncode != 0 else None
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class GitDiffTool(BaseTool):
    """Get git diff."""
    
    name = "git_diff"
    description = "Show git changes"
    parameters = {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"}
        }
    }
    
    async def execute(self, path: str) -> ToolResult:
        try:
            result = subprocess.run(
                ['git', 'diff'],
                cwd=path,
                capture_output=True,
                text=True
            )
            
            return ToolResult(
                success=True,
                data=result.stdout,
                metadata={'files_changed': len(result.stdout.split('diff --git')) - 1}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class SemanticSearchTool(BaseTool):
    """Semantic code search using embeddings."""
    
    name = "semantic_search"
    description = "Search code semantically"
    parameters = {
        "required": ["query", "path"],
        "properties": {
            "query": {"type": "string"},
            "path": {"type": "string"},
            "top_k": {"type": "integer"}
        }
    }
    
    async def execute(
        self,
        query: str,
        path: str,
        top_k: int = 5
    ) -> ToolResult:
        """
        Placeholder for semantic search.
        In production, this would use embeddings (FAISS, Chroma, etc.)
        """
        # Fallback to text search
        search_tool = SearchProjectTool()
        return await search_tool.execute(query, path)


class MemoryLookupTool(BaseTool):
    """Lookup past solutions from memory."""
    
    name = "memory_lookup"
    description = "Search memory for similar solutions"
    parameters = {
        "required": ["query"],
        "properties": {
            "query": {"type": "string"},
            "limit": {"type": "integer"}
        }
    }
    
    async def execute(
        self,
        query: str,
        limit: int = 3
    ) -> ToolResult:
        # This would integrate with the memory system
        return ToolResult(
            success=True,
            data=[],
            metadata={'note': 'Memory lookup not implemented yet'}
        )


class MemoryStoreTool(BaseTool):
    """Store solution in memory."""
    
    name = "memory_store"
    description = "Store a resolution pattern"
    parameters = {
        "required": ["pattern"],
        "properties": {
            "pattern": {"type": "object"}
        }
    }
    
    async def execute(self, pattern: Dict) -> ToolResult:
        # This would integrate with the memory system
        return ToolResult(
            success=True,
            data="Pattern stored",
            metadata={'pattern': pattern}
        )


class ToolRegistry:
    """Registry for all available tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register all default tools."""
        tools = [
            ReadFileTool(),
            WriteFileTool(),
            ListDirectoryTool(),
            SearchProjectTool(),
            RunTestsTool(),
            RunLinterTool(),
            RunTypecheckTool(),
            GitDiffTool(),
            SemanticSearchTool(),
            MemoryLookupTool(),
            MemoryStoreTool(),
        ]
        
        for tool in tools:
            self._tools[tool.name] = tool
    
    def register(self, tool: BaseTool):
        """Register a new tool."""
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    async def execute(self, name: str, params: Dict[str, Any]) -> ToolResult:
        """Execute a tool by name."""
        tool = self.get(name)
        if not tool:
            return ToolResult(
                success=False,
                data=None,
                error=f"Tool not found: {name}"
            )
        
        if not tool.validate_params(params):
            return ToolResult(
                success=False,
                data=None,
                error=f"Invalid parameters for tool {name}"
            )
        
        return await tool.execute(**params)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        return [
            {
                'name': tool.name,
                'description': tool.description,
                'parameters': tool.parameters
            }
            for tool in self._tools.values()
        ]
