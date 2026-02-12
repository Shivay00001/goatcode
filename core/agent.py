"""
GOATCODE - Deterministic, Tool-Augmented Coding Agent
Core Orchestrator Module

This module manages the entire agent execution pipeline following
the Think → Plan → Execute → Verify loop.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging

from .llm_interface import LLMInterface, LLMResponse
from .tool_registry import ToolRegistry
from .context_manager import ContextManager
from .memory_system import MemorySystem
from .validation_engine import ValidationEngine


class ExecutionPhase(Enum):
    INTENT_ANALYSIS = "intent_analysis"
    PROJECT_CONTEXT = "project_context"
    RISK_ANALYSIS = "risk_analysis"
    IMPLEMENTATION_PLAN = "implementation_plan"
    CODE_GENERATION = "code_generation"
    VALIDATION = "validation"
    COMPLETE = "complete"


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ERROR = "error"


@dataclass
class ExecutionLog:
    phase: ExecutionPhase
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    status: AgentStatus
    analysis_summary: str
    implementation_plan: List[str]
    files_modified: List[Dict[str, Any]]
    validation_report: Dict[str, Any]
    confidence_score: float
    logs: List[ExecutionLog]
    error_message: Optional[str] = None


class GoatCodeAgent:
    """
    Main orchestrator for the GOATCODE coding agent.
    
    Implements the complete execution pipeline:
    1. Intent Analysis
    2. Project Context Analysis
    3. Risk & Edge Case Analysis
    4. Implementation Plan Generation
    5. Code Generation
    6. Self-Validation
    """
    
    def __init__(
        self,
        llm_interface: LLMInterface,
        tool_registry: ToolRegistry,
        context_manager: ContextManager,
        memory_system: MemorySystem,
        validation_engine: ValidationEngine,
        config: Optional[Dict[str, Any]] = None
    ):
        self.llm = llm_interface
        self.tools = tool_registry
        self.context = context_manager
        self.memory = memory_system
        self.validator = validation_engine
        self.config = config or {}
        
        self.status = AgentStatus.IDLE
        self.current_task: Optional[str] = None
        self.logs: List[ExecutionLog] = []
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure structured logging for the agent."""
        self.logger = logging.getLogger("goatcode")
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log(self, phase: ExecutionPhase, message: str, metadata: Optional[Dict] = None):
        """Add execution log entry."""
        log_entry = ExecutionLog(
            phase=phase,
            message=message,
            metadata=metadata or {}
        )
        self.logs.append(log_entry)
        self.logger.info(f"[{phase.value}] {message}")
    
    async def execute(self, prompt: str, project_path: str) -> AgentResult:
        """
        Execute the complete coding agent pipeline.
        
        Args:
            prompt: The user's coding request
            project_path: Path to the project directory
            
        Returns:
            AgentResult with status, code changes, and validation report
        """
        self.status = AgentStatus.RUNNING
        self.current_task = prompt
        self.logs = []
        
        try:
            # STEP 1: Intent Analysis
            self._log(ExecutionPhase.INTENT_ANALYSIS, "Analyzing user intent...")
            intent = await self._analyze_intent(prompt)
            
            # STEP 2: Project Context Analysis
            self._log(ExecutionPhase.PROJECT_CONTEXT, "Gathering project context...")
            context = await self._gather_context(project_path, intent)
            
            # STEP 3: Risk Analysis
            self._log(ExecutionPhase.RISK_ANALYSIS, "Analyzing risks and edge cases...")
            risks = await self._analyze_risks(intent, context)
            
            # Check memory for similar patterns
            self._log(ExecutionPhase.PROJECT_CONTEXT, "Checking memory for similar solutions...")
            memory_hints = await self._check_memory(intent, context)
            
            # STEP 4: Implementation Plan
            self._log(ExecutionPhase.IMPLEMENTATION_PLAN, "Generating implementation plan...")
            plan = await self._create_implementation_plan(intent, context, risks, memory_hints)
            
            # STEP 5: Code Generation
            self._log(ExecutionPhase.CODE_GENERATION, "Generating code...")
            generated_code = await self._generate_code(intent, context, plan)
            
            # STEP 6: Validation Loop
            self._log(ExecutionPhase.VALIDATION, "Running validation suite...")
            validated_result = await self._validate_and_fix(
                generated_code, project_path, plan
            )
            
            # Store successful pattern in memory
            if validated_result['validation_report']['all_passed']:
                await self._store_success_pattern(intent, validated_result)
            
            self.status = AgentStatus.SUCCESS
            
            return AgentResult(
                status=self.status,
                analysis_summary=intent['summary'],
                implementation_plan=plan['steps'],
                files_modified=validated_result['files'],
                validation_report=validated_result['validation_report'],
                confidence_score=validated_result['confidence'],
                logs=self.logs
            )
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.logger.error(f"Agent execution failed: {str(e)}")
            
            return AgentResult(
                status=self.status,
                analysis_summary="",
                implementation_plan=[],
                files_modified=[],
                validation_report={},
                confidence_score=0.0,
                logs=self.logs,
                error_message=str(e)
            )
    
    async def _analyze_intent(self, prompt: str) -> Dict[str, Any]:
        """Step 1: Extract and analyze user intent."""
        system_prompt = """You are an intent analysis engine. Extract the following from the user's request:
        1. Primary goal/objective
        2. Target programming language/framework
        3. Constraints (performance, security, compatibility)
        4. Expected output format
        5. Success criteria
        
        Return ONLY a JSON object with these fields."""
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.1  # Low temperature for deterministic analysis
        )
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback: use LLM to fix JSON
            fixed = await self.llm.generate(
                prompt=f"Fix this malformed JSON: {response.content}",
                temperature=0.1
            )
            return json.loads(fixed.content)
    
    async def _gather_context(self, project_path: str, intent: Dict) -> Dict[str, Any]:
        """Step 2: Gather relevant project context using tools."""
        context = {
            'project_structure': [],
            'relevant_files': [],
            'dependencies': {},
            'existing_code': {},
            'framework': None
        }
        
        # List project structure
        try:
            structure = await self.tools.execute('list_directory', {'path': project_path})
            context['project_structure'] = structure
        except Exception as e:
            self.logger.warning(f"Could not list directory: {e}")
        
        # Search for relevant files based on intent
        if 'language' in intent:
            search_results = await self.tools.execute('search_project', {
                'query': intent['language'],
                'path': project_path
            })
            context['relevant_files'] = search_results[:10]  # Top 10 relevant files
        
        # Read key configuration files
        config_files = ['package.json', 'requirements.txt', 'Cargo.toml', 'pubspec.yaml', 'pom.xml']
        for config in config_files:
            try:
                content = await self.tools.execute('read_file', {
                    'path': f"{project_path}/{config}"
                })
                context['dependencies'][config] = content
            except:
                pass
        
        # Detect framework
        context['framework'] = self._detect_framework(context['dependencies'])
        
        return context
    
    def _detect_framework(self, dependencies: Dict) -> Optional[str]:
        """Detect the framework from dependencies."""
        if 'package.json' in dependencies:
            if 'react' in dependencies['package.json'].lower():
                return 'react'
            elif 'vue' in dependencies['package.json'].lower():
                return 'vue'
            elif 'next' in dependencies['package.json'].lower():
                return 'nextjs'
        elif 'pubspec.yaml' in dependencies:
            return 'flutter'
        elif 'requirements.txt' in dependencies:
            content = dependencies['requirements.txt'].lower()
            if 'django' in content:
                return 'django'
            elif 'flask' in content:
                return 'flask'
            elif 'fastapi' in content:
                return 'fastapi'
        
        return None
    
    async def _analyze_risks(self, intent: Dict, context: Dict) -> Dict[str, Any]:
        """Step 3: Analyze risks, edge cases, and security concerns."""
        system_prompt = """Analyze the following coding task for:
        1. Security risks (injection, unsafe eval, hardcoded secrets)
        2. Performance concerns (inefficient algorithms, memory leaks)
        3. Edge cases (null values, empty inputs, extreme values)
        4. Concurrency issues (race conditions, deadlocks)
        5. Breaking changes (API compatibility, data migration)
        
        Return a JSON object with risks categorized by severity."""
        
        prompt = f"Intent: {json.dumps(intent)}\nContext: {json.dumps(context)}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.2
        )
        
        try:
            return json.loads(response.content)
        except:
            return {'risks': [], 'severity': 'unknown'}
    
    async def _check_memory(self, intent: Dict, context: Dict) -> List[Dict]:
        """Check memory system for similar past solutions."""
        try:
            # Create search key from intent
            search_key = f"{intent.get('language', '')} {intent.get('goal', '')}"
            
            memories = await self.memory.lookup(search_key, limit=3)
            
            if memories:
                self._log(
                    ExecutionPhase.PROJECT_CONTEXT,
                    f"Found {len(memories)} similar patterns in memory",
                    {'patterns': [m.get('resolution_pattern', '') for m in memories]}
                )
            
            return memories
        except Exception as e:
            self.logger.warning(f"Memory lookup failed: {e}")
            return []
    
    async def _create_implementation_plan(
        self,
        intent: Dict,
        context: Dict,
        risks: Dict,
        memory_hints: List[Dict]
    ) -> Dict[str, Any]:
        """Step 4: Generate detailed implementation plan."""
        
        # Include memory hints in prompt if available
        memory_context = ""
        if memory_hints:
            memory_context = "\n\nPreviously successful patterns:\n"
            for hint in memory_hints:
                memory_context += f"- {hint.get('resolution_pattern', '')}\n"
        
        system_prompt = f"""Create a detailed implementation plan for the coding task.
        
        Your plan must include:
        1. List of files to modify/create
        2. Functions/classes to implement
        3. Dependencies to add
        4. Validation steps
        5. Rollback strategy
        
        Consider these risks: {json.dumps(risks)}
        {memory_context}
        
        Return JSON with: steps (list), files (list), validation_steps (list)"""
        
        prompt = f"Intent: {json.dumps(intent)}\nContext: {json.dumps(context)}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.2
        )
        
        try:
            return json.loads(response.content)
        except:
            # Fallback: create a basic plan
            return {
                'steps': ['Create implementation', 'Add tests', 'Validate'],
                'files': [],
                'validation_steps': ['Run tests', 'Check types']
            }
    
    async def _generate_code(
        self,
        intent: Dict,
        context: Dict,
        plan: Dict
    ) -> Dict[str, Any]:
        """Step 5: Generate complete, correct code."""
        
        system_prompt = """You are a code generation engine. Generate complete, production-ready code.
        
        Rules:
        1. Include ALL necessary imports
        2. Include type hints where applicable
        3. Include docstrings
        4. Include error handling
        5. NO placeholder code
        6. NO TODO comments
        7. Follow existing code style
        8. Make minimal changes
        
        Return JSON with: files (array of {path, content, action: create|update})"""
        
        prompt = f"""Generate code for:
Intent: {json.dumps(intent)}
Context: {json.dumps(context)}
Plan: {json.dumps(plan)}

Generate the complete implementation."""
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.3,
            max_tokens=4000
        )
        
        try:
            result = json.loads(response.content)
            return result
        except:
            # Try to extract code blocks if JSON parsing fails
            return self._extract_code_from_text(response.content)
    
    def _extract_code_from_text(self, text: str) -> Dict[str, Any]:
        """Extract code blocks from non-JSON response."""
        import re
        
        files = []
        # Pattern for code blocks with file paths
        pattern = r'```[\w]*\n?(.*?)\n?```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for i, code in enumerate(matches):
            files.append({
                'path': f'generated_file_{i}.py',
                'content': code.strip(),
                'action': 'create'
            })
        
        return {'files': files}
    
    async def _validate_and_fix(
        self,
        generated_code: Dict,
        project_path: str,
        plan: Dict
    ) -> Dict[str, Any]:
        """Step 6: Validate code and fix issues iteratively."""
        
        max_retries = self.config.get('max_validation_retries', 3)
        attempt = 0
        
        files = generated_code.get('files', [])
        
        while attempt < max_retries:
            attempt += 1
            self._log(
                ExecutionPhase.VALIDATION,
                f"Validation attempt {attempt}/{max_retries}"
            )
            
            # Write files temporarily
            temp_files = []
            for file_info in files:
                try:
                    await self.tools.execute('write_file', {
                        'path': f"{project_path}/{file_info['path']}",
                        'content': file_info['content']
                    })
                    temp_files.append(file_info['path'])
                except Exception as e:
                    self.logger.error(f"Failed to write {file_info['path']}: {e}")
            
            # Run validation suite
            validation_results = await self.validator.validate_all(
                project_path,
                files,
                plan.get('validation_steps', [])
            )
            
            if validation_results['all_passed']:
                self._log(ExecutionPhase.VALIDATION, "All validations passed!")
                return {
                    'files': files,
                    'validation_report': validation_results,
                    'confidence': 0.95
                }
            
            # If validation failed, attempt to fix
            self._log(
                ExecutionPhase.VALIDATION,
                f"Validation failed: {validation_results['failures']}"
            )
            
            if attempt < max_retries:
                # Generate fixes
                files = await self._generate_fixes(files, validation_results)
        
        # If we exhausted retries, return with partial success
        return {
            'files': files,
            'validation_report': validation_results,
            'confidence': 0.5 if validation_results['some_passed'] else 0.2
        }
    
    async def _generate_fixes(
        self,
        files: List[Dict],
        validation_results: Dict
    ) -> List[Dict]:
        """Generate fixes for validation failures."""
        
        system_prompt = """Fix the code based on validation errors.
        
        Return the corrected files in the same format.
        Make minimal, surgical changes to fix only the reported issues."""
        
        prompt = f"Files: {json.dumps(files)}\nValidation Errors: {json.dumps(validation_results)}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.2
        )
        
        try:
            result = json.loads(response.content)
            return result.get('files', files)
        except:
            return files
    
    async def _store_success_pattern(self, intent: Dict, result: Dict):
        """Store successful resolution pattern in memory."""
        try:
            pattern = {
                'intent_type': intent.get('goal', 'unknown'),
                'language': intent.get('language', 'unknown'),
                'framework': intent.get('framework', 'unknown'),
                'resolution_pattern': result['validation_report'],
                'files_modified': [f['path'] for f in result['files']],
                'timestamp': datetime.now().isoformat()
            }
            
            await self.memory.store(pattern)
            self._log(ExecutionPhase.COMPLETE, "Stored success pattern in memory")
        except Exception as e:
            self.logger.warning(f"Failed to store memory: {e}")


# Factory function for easy instantiation
def create_agent(
    llm_provider: str = "ollama",
    llm_model: str = "llama2",
    project_path: str = ".",
    config: Optional[Dict] = None
) -> GoatCodeAgent:
    """
    Factory function to create a fully configured GOATCODE agent.
    
    Args:
        llm_provider: 'ollama', 'openai', 'anthropic', etc.
        llm_model: Model name (e.g., 'llama2', 'gpt-4', 'claude-3')
        project_path: Path to the project being worked on
        config: Additional configuration options
    
    Returns:
        Configured GoatCodeAgent instance
    """
    from .llm_interface import create_llm_interface
    from .tool_registry import ToolRegistry
    from .context_manager import ContextManager
    from .memory_system import MemorySystem
    from .validation_engine import ValidationEngine
    
    # Initialize components
    llm = create_llm_interface(provider=llm_provider, model=llm_model)
    tools = ToolRegistry()
    context = ContextManager(project_path)
    memory = MemorySystem()
    validator = ValidationEngine(tools)
    
    return GoatCodeAgent(
        llm_interface=llm,
        tool_registry=tools,
        context_manager=context,
        memory_system=memory,
        validation_engine=validator,
        config=config
    )
