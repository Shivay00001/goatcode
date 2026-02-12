"""
GOATCODE v2.0 - Enhanced Agent with Advanced Capabilities
Integration of architecture, security, and domain expertise.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio

from .agent import GoatCodeAgent, create_agent as base_create_agent
from .advanced_modules import (
    AdvancedGoatCodeAgent,
    AgentCapability,
    ArchitectureEngine,
    SecurityAuditEngine,
    DomainExpertSystem,
    AmbiguityResolver
)


class AgentMode(Enum):
    """Agent operating modes."""
    STANDARD = "standard"  # Original capabilities
    ARCHITECT = "architect"  # System design mode
    SECURITY_AUDITOR = "security"  # Security review mode
    DOMAIN_EXPERT = "domain"  # Domain-specific mode
    FULL_STACK = "full_stack"  # All capabilities


@dataclass
class EnhancedAgentResult:
    """Enhanced result with all capabilities."""
    # Original fields
    status: str
    analysis_summary: str
    implementation_plan: List[str]
    files_modified: List[Dict[str, Any]]
    validation_report: Dict[str, Any]
    confidence_score: float
    
    # New fields
    architecture_design: Optional[Dict[str, Any]] = None
    security_audit: Optional[Dict[str, Any]] = None
    domain_analysis: Optional[Dict[str, Any]] = None
    ambiguity_resolution: Optional[Dict[str, Any]] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []


class ProductionGradeGoatCodeAgent(GoatCodeAgent):
    """
    Production-grade agent with senior architect capabilities.
    
    Capabilities:
    - Complex system architecture design
    - Security audits (OWASP, CWE)
    - Domain expertise (healthcare, finance, etc.)
    - Ambiguity resolution
    - Multi-file coordination
    - Formal verification hints
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize advanced modules
        self.advanced = AdvancedGoatCodeAgent(self.llm, self.config)
        self.mode = AgentMode.FULL_STACK
    
    async def execute_production_grade(
        self,
        prompt: str,
        project_path: str,
        mode: AgentMode = AgentMode.FULL_STACK,
        domain: Optional[str] = None
    ) -> EnhancedAgentResult:
        """
        Execute with production-grade capabilities.
        
        Args:
            prompt: User request
            project_path: Project path
            mode: Operating mode
            domain: Specific domain (healthcare, finance, ecommerce)
        
        Returns:
            Enhanced result with all analyses
        """
        print(f"🐐 GOATCODE v2.0 - {mode.value.upper()} MODE")
        print("=" * 60)
        
        # Phase 1: Ambiguity Resolution
        print("\n📋 Phase 1: Resolving Ambiguities...")
        ambiguity_result = await self._handle_ambiguity(prompt)
        
        if ambiguity_result.get('status') == 'clarification_needed':
            return EnhancedAgentResult(
                status="clarification_needed",
                analysis_summary="Need more information to proceed",
                implementation_plan=[],
                files_modified=[],
                validation_report={},
                confidence_score=0.0,
                ambiguity_resolution=ambiguity_result
            )
        
        # Phase 2: Domain Analysis
        print("\n🏛️  Phase 2: Domain Analysis...")
        domain_analysis = await self._analyze_domain(prompt, domain)
        
        # Phase 3: Architecture Design (if needed)
        print("\n🏗️  Phase 3: Architecture Design...")
        architecture = None
        if self._is_architecture_request(prompt):
            architecture = await self._design_architecture(prompt, project_path)
        
        # Phase 4: Security Audit
        print("\n🔒 Phase 4: Security Audit...")
        security_audit = await self._perform_security_audit(project_path)
        
        # Phase 5: Standard Code Generation
        print("\n💻 Phase 5: Code Generation...")
        base_result = await super().execute(prompt, project_path)
        
        # Phase 6: Integration & Validation
        print("\n✅ Phase 6: Integration & Validation...")
        recommendations = self._generate_recommendations(
            base_result, architecture, security_audit, domain_analysis
        )
        
        return EnhancedAgentResult(
            status=base_result.status.value,
            analysis_summary=base_result.analysis_summary,
            implementation_plan=base_result.implementation_plan,
            files_modified=base_result.files_modified,
            validation_report=base_result.validation_report,
            confidence_score=base_result.confidence_score,
            architecture_design=architecture,
            security_audit=security_audit,
            domain_analysis=domain_analysis,
            ambiguity_resolution=ambiguity_result,
            recommendations=recommendations
        )
    
    async def _handle_ambiguity(self, prompt: str) -> Dict[str, Any]:
        """Handle ambiguous requirements."""
        return await self.advanced.ambiguity.resolve_ambiguity(prompt, {})
    
    async def _analyze_domain(self, prompt: str, domain: Optional[str]) -> Dict[str, Any]:
        """Analyze domain-specific requirements."""
        return await self.advanced.domain.analyze_domain_requirements(prompt, domain)
    
    def _is_architecture_request(self, prompt: str) -> bool:
        """Determine if request involves architecture."""
        architecture_keywords = [
            'architecture', 'system design', 'microservices', 'database design',
            'scalability', 'distributed', 'service', 'component', 'api design',
            'data model', 'integration', 'deployment'
        ]
        return any(kw in prompt.lower() for kw in architecture_keywords)
    
    async def _design_architecture(
        self,
        prompt: str,
        project_path: str
    ) -> Optional[Dict[str, Any]]:
        """Design system architecture."""
        requirements = {
            'functional': prompt,
            'constraints': {'project_path': project_path}
        }
        
        return await self.advanced.architecture.design_system_architecture(
            requirements=requirements,
            constraints={'existing_codebase': True}
        )
    
    async def _perform_security_audit(self, project_path: str) -> Optional[Dict[str, Any]]:
        """Perform security audit."""
        import os
        
        # Find source files
        files = []
        for root, dirs, filenames in os.walk(project_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.git', '__pycache__']]
            
            for f in filenames:
                if f.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs')):
                    files.append(os.path.join(root, f))
        
        if files:
            # Limit to first 50 files for performance
            return await self.advanced.security.perform_security_audit(
                project_path, files[:50]
            )
        
        return None
    
    def _generate_recommendations(
        self,
        base_result: Any,
        architecture: Optional[Dict],
        security: Optional[Dict],
        domain: Optional[Dict]
    ) -> List[str]:
        """Generate comprehensive recommendations."""
        recommendations = []
        
        # Security recommendations
        if security and security.get('summary', {}).get('critical', 0) > 0:
            recommendations.append(
                f"⚠️  CRITICAL: {security['summary']['critical']} security vulnerabilities found. "
                f"Fix before deployment."
            )
        
        # Architecture recommendations
        if architecture:
            patterns = [p['name'] for p in architecture.get('selected_patterns', [])]
            recommendations.append(
                f"🏗️  Architecture: Consider {', '.join(patterns)} patterns"
            )
        
        # Domain recommendations
        if domain and domain.get('compliance_requirements'):
            recommendations.append(
                f"📋 Compliance: Ensure adherence to {', '.join(domain['compliance_requirements'][:3])}"
            )
        
        # Code quality
        if base_result.validation_report.get('all_passed'):
            recommendations.append("✅ All validations passed - code is production-ready")
        else:
            recommendations.append("⚠️  Some validations failed - review before deployment")
        
        return recommendations


def create_production_agent(
    llm_provider: str = "ollama",
    llm_model: str = "llama2",
    project_path: str = ".",
    config: Optional[Dict] = None
) -> ProductionGradeGoatCodeAgent:
    """
    Factory for production-grade agent.
    
    Args:
        llm_provider: LLM provider
        llm_model: Model name
        project_path: Project directory
        config: Additional configuration
    
    Returns:
        Production-grade agent instance
    """
    # Create base agent
    base_agent = base_create_agent(
        llm_provider=llm_provider,
        llm_model=llm_model,
        project_path=project_path,
        config=config
    )
    
    # Enhance with production capabilities
    production_agent = ProductionGradeGoatCodeAgent(
        llm_interface=base_agent.llm,
        tool_registry=base_agent.tools,
        context_manager=base_agent.context,
        memory_system=base_agent.memory,
        validation_engine=base_agent.validator,
        config=config
    )
    
    return production_agent


# CLI Integration
async def main_production():
    """Production-mode CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='GOATCODE v2.0 - Production-Grade Coding Agent'
    )
    parser.add_argument('--mode', choices=[m.value for m in AgentMode], default='full_stack')
    parser.add_argument('--domain', choices=['healthcare', 'finance', 'ecommerce', 'generic'])
    parser.add_argument('--provider', default='ollama')
    parser.add_argument('--model', default='llama2')
    parser.add_argument('--project', default='.')
    parser.add_argument('-p', '--prompt', required=True)
    
    args = parser.parse_args()
    
    # Create production agent
    agent = create_production_agent(
        llm_provider=args.provider,
        llm_model=args.model,
        project_path=args.project
    )
    
    # Execute
    result = await agent.execute_production_grade(
        prompt=args.prompt,
        project_path=args.project,
        mode=AgentMode(args.mode),
        domain=args.domain
    )
    
    # Display results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    print(f"\nStatus: {result.status}")
    print(f"Confidence: {result.confidence_score:.0%}")
    
    if result.architecture_design:
        print("\n🏗️  Architecture Design:")
        patterns = [p['name'] for p in result.architecture_design.get('selected_patterns', [])]
        print(f"  Patterns: {', '.join(patterns)}")
        print(f"  Components: {len(result.architecture_design.get('components', []))}")
    
    if result.security_audit:
        print("\n🔒 Security Audit:")
        summary = result.security_audit.get('summary', {})
        print(f"  Score: {summary.get('security_score', 'N/A')}/100")
        print(f"  Grade: {summary.get('grade', 'N/A')}")
        print(f"  Critical: {summary.get('critical', 0)}")
        print(f"  High: {summary.get('high', 0)}")
    
    if result.domain_analysis:
        print("\n🏛️  Domain Analysis:")
        print(f"  Domain: {result.domain_analysis.get('domain', 'generic')}")
        compliance = result.domain_analysis.get('compliance_requirements', [])
        if compliance:
            print(f"  Compliance: {', '.join(compliance[:3])}")
    
    print("\n📋 Recommendations:")
    for rec in result.recommendations:
        print(f"  • {rec}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    asyncio.run(main_production())
