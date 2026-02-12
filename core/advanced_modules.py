#!/usr/bin/env python3
"""
GOATCODE v2.0 - Production-Grade Architecture & Security Agent
Advanced capabilities for senior architects and complex systems.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime
import json
import asyncio
from pathlib import Path


class AgentCapability(Enum):
    """Advanced agent capabilities."""
    ARCHITECTURE_DESIGN = "architecture_design"
    SECURITY_AUDIT = "security_audit"
    DOMAIN_EXPERTISE = "domain_expertise"
    SYSTEM_DESIGN = "system_design"
    COMPLEX_REFACTORING = "complex_refactoring"


@dataclass
class ArchitecturePattern:
    """Architecture pattern template."""
    name: str
    category: str  # microservices, monolith, serverless, etc.
    description: str
    components: List[Dict[str, Any]]
    data_flow: List[Dict[str, str]]
    pros: List[str]
    cons: List[str]
    best_for: List[str]
    anti_patterns: List[str]
    implementation_steps: List[str]


@dataclass
class SecurityVulnerability:
    """Security vulnerability finding."""
    severity: str  # critical, high, medium, low
    category: str  # injection, auth, crypto, etc.
    file_path: str
    line_number: int
    description: str
    cwe_id: Optional[str] = None
    owasp_category: Optional[str] = None
    remediation: Optional[str] = None
    code_snippet: Optional[str] = None
    false_positive: bool = False


@dataclass
class DomainModel:
    """Domain-specific knowledge model."""
    domain: str  # healthcare, finance, e-commerce, etc.
    entities: List[Dict[str, Any]]
    business_rules: List[str]
    compliance_requirements: List[str]
    data_sensitivity_levels: Dict[str, str]
    common_patterns: List[ArchitecturePattern]
    regulatory_frameworks: List[str]


@dataclass
class SystemComponent:
    """System architecture component."""
    name: str
    type: str  # service, database, queue, cache, etc.
    responsibilities: List[str]
    interfaces: List[Dict[str, Any]]
    dependencies: List[str]
    scalability_profile: str
    data_stores: List[str]
    tech_stack: List[str]
    deployment_strategy: str


@dataclass
class DesignDecision:
    """Architecture design decision record (ADR)."""
    id: str
    title: str
    context: str
    decision: str
    consequences: List[str]
    alternatives_considered: List[str]
    date: datetime = field(default_factory=datetime.now)
    status: str = "proposed"  # proposed, accepted, deprecated, superseded


class ArchitectureEngine:
    """
    Advanced architecture design engine for complex systems.
    Handles microservices, distributed systems, database design.
    """
    
    def __init__(self, llm_interface):
        self.llm = llm_interface
        self.patterns_db = self._load_architecture_patterns()
    
    def _load_architecture_patterns(self) -> Dict[str, ArchitecturePattern]:
        """Load architecture pattern database."""
        return {
            "microservices": ArchitecturePattern(
                name="Microservices Architecture",
                category="distributed",
                description="Decompose application into loosely coupled services",
                components=[
                    {"name": "API Gateway", "type": "gateway", "responsibilities": ["routing", "auth", "rate_limiting"]},
                    {"name": "Service Registry", "type": "registry", "responsibilities": ["service_discovery"]},
                    {"name": "Config Server", "type": "config", "responsibilities": ["centralized_config"]},
                ],
                data_flow=[
                    {"from": "client", "to": "api_gateway", "protocol": "https"},
                    {"from": "api_gateway", "to": "services", "protocol": "grpc/http"},
                    {"from": "services", "to": "database", "protocol": "tcp"},
                ],
                pros=["scalability", "technology_diversity", "fault_isolation", "independent_deployment"],
                cons=["complexity", "distributed_system_challenges", "data_consistency", "operational_overhead"],
                best_for=["large_teams", "complex_domains", "high_scale", "evolutionary_architecture"],
                anti_patterns=["distributed_monolith", "shared_database", "tight_coupling"],
                implementation_steps=[
                    "Identify bounded contexts",
                    "Define service boundaries",
                    "Design inter-service communication",
                    "Implement service discovery",
                    "Set up distributed tracing",
                    "Implement circuit breakers"
                ]
            ),
            "event_driven": ArchitecturePattern(
                name="Event-Driven Architecture",
                category="async",
                description="Components communicate through events",
                components=[
                    {"name": "Event Bus", "type": "messaging", "responsibilities": ["event_routing"]},
                    {"name": "Event Store", "type": "database", "responsibilities": ["event_persistence"]},
                    {"name": "Event Processors", "type": "consumers", "responsibilities": ["event_handling"]},
                ],
                data_flow=[
                    {"from": "producers", "to": "event_bus", "protocol": "async"},
                    {"from": "event_bus", "to": "consumers", "protocol": "pub_sub"},
                ],
                pros=["loose_coupling", "scalability", "audit_trail", "temporal_decoupling"],
                cons=["eventual_consistency", "complexity", "debugging_difficulty"],
                best_for=["async_processing", "audit_requirements", "complex_workflows"],
                anti_patterns=["synchronous_event_handling", "missing_error_handling"],
                implementation_steps=[
                    "Design event schema",
                    "Choose event broker",
                    "Implement event producers",
                    "Implement event consumers",
                    "Add dead letter queues",
                    "Implement idempotency"
                ]
            ),
            "cqrs": ArchitecturePattern(
                name="CQRS (Command Query Responsibility Segregation)",
                category="data",
                description="Separate read and write models",
                components=[
                    {"name": "Command Handler", "type": "service", "responsibilities": ["write_operations"]},
                    {"name": "Query Handler", "type": "service", "responsibilities": ["read_operations"]},
                    {"name": "Event Store", "type": "database", "responsibilities": ["source_of_truth"]},
                    {"name": "Read Model", "type": "database", "responsibilities": ["optimized_queries"]},
                ],
                data_flow=[
                    {"from": "commands", "to": "command_handler", "protocol": "sync"},
                    {"from": "command_handler", "to": "event_store", "protocol": "sync"},
                    {"from": "event_store", "to": "projections", "protocol": "async"},
                    {"from": "queries", "to": "query_handler", "protocol": "sync"},
                ],
                pros=["optimized_reads", "scalability", "event_sourcing_compatible"],
                cons=["complexity", "eventual_consistency", "data_synchronization"],
                best_for=["high_read_scenarios", "complex_domains", "audit_requirements"],
                anti_patterns=["premature_optimization", "unnecessary_complexity"],
                implementation_steps=[
                    "Identify command and query paths",
                    "Design event schema",
                    "Implement command handlers",
                    "Implement projections",
                    "Optimize read models"
                ]
            ),
            "hexagonal": ArchitecturePattern(
                name="Hexagonal Architecture (Ports & Adapters)",
                category="structural",
                description="Isolate business logic from external concerns",
                components=[
                    {"name": "Domain Layer", "type": "core", "responsibilities": ["business_logic"]},
                    {"name": "Application Layer", "type": "core", "responsibilities": ["use_cases"]},
                    {"name": "Adapters", "type": "infrastructure", "responsibilities": ["external_interfaces"]},
                ],
                data_flow=[
                    {"from": "adapters", "to": "application", "protocol": "ports"},
                    {"from": "application", "to": "domain", "protocol": "direct"},
                ],
                pros=["testability", "technology_independence", "clear_boundaries"],
                cons=["initial_complexity", "learning_curve"],
                best_for=["testability_critical", "long_term_maintenance", "complex_domains"],
                anti_patterns=["leaking_infrastructure", "anemic_domain_model"],
                implementation_steps=[
                    "Define domain model",
                    "Identify ports (interfaces)",
                    "Implement adapters",
                    "Wire dependencies"
                ]
            ),
        }
    
    async def design_system_architecture(
        self,
        requirements: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Design complete system architecture from requirements.
        
        Args:
            requirements: Functional and non-functional requirements
            constraints: Technical and business constraints
            
        Returns:
            Complete architecture design with components, data flow, decisions
        """
        # Step 1: Analyze requirements
        analysis = await self._analyze_requirements(requirements, constraints)
        
        # Step 2: Select appropriate patterns
        patterns = await self._select_patterns(analysis)
        
        # Step 3: Design components
        components = await self._design_components(analysis, patterns)
        
        # Step 4: Design data architecture
        data_architecture = await self._design_data_architecture(analysis, components)
        
        # Step 5: Design integration points
        integrations = await self._design_integrations(components)
        
        # Step 6: Create deployment architecture
        deployment = await self._design_deployment(components, constraints)
        
        # Step 7: Generate architecture decision records
        decisions = await self._generate_adrs(patterns, analysis)
        
        return {
            "analysis": analysis,
            "selected_patterns": patterns,
            "components": components,
            "data_architecture": data_architecture,
            "integrations": integrations,
            "deployment": deployment,
            "decisions": decisions,
            "diagrams": await self._generate_diagrams(components, patterns),
            "implementation_roadmap": await self._create_roadmap(components)
        }
    
    async def _analyze_requirements(
        self,
        requirements: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep analysis of requirements."""
        system_prompt = """You are a senior architect analyzing system requirements.
        
        Analyze the following requirements and constraints:
        1. Identify functional requirements (what the system must do)
        2. Identify non-functional requirements (performance, security, scalability)
        3. Identify constraints (budget, timeline, technology restrictions)
        4. Identify stakeholders and their concerns
        5. Identify quality attributes (availability, maintainability, etc.)
        6. Identify risks and mitigation strategies
        
        Return a structured analysis with recommendations."""
        
        prompt = f"Requirements: {json.dumps(requirements)}\nConstraints: {json.dumps(constraints)}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.2
        )
        
        try:
            return json.loads(response.content)
        except:
            return {"analysis": response.content, "raw": True}
    
    async def _select_patterns(
        self,
        analysis: Dict[str, Any]
    ) -> List[ArchitecturePattern]:
        """Select appropriate architecture patterns."""
        # Match patterns to requirements
        selected = []
        
        # Check for microservices indicators
        if analysis.get('scalability_needs') == 'high' or \
           analysis.get('team_size', 0) > 10 or \
           analysis.get('deployment_frequency') == 'high':
            selected.append(self.patterns_db['microservices'])
        
        # Check for event-driven indicators
        if analysis.get('async_processing', False) or \
           analysis.get('event_sourcing', False):
            selected.append(self.patterns_db['event_driven'])
        
        # Check for CQRS indicators
        if analysis.get('read_write_ratio', 1) > 10:
            selected.append(self.patterns_db['cqrs'])
        
        # Default to hexagonal for testability
        if analysis.get('testability_critical', False):
            selected.append(self.patterns_db['hexagonal'])
        
        return selected if selected else [self.patterns_db['hexagonal']]
    
    async def _design_components(
        self,
        analysis: Dict[str, Any],
        patterns: List[ArchitecturePattern]
    ) -> List[SystemComponent]:
        """Design system components."""
        components = []
        
        # Generate components based on patterns
        for pattern in patterns:
            for comp_def in pattern.components:
                component = SystemComponent(
                    name=comp_def['name'],
                    type=comp_def['type'],
                    responsibilities=comp_def.get('responsibilities', []),
                    interfaces=[],
                    dependencies=[],
                    scalability_profile="horizontal" if pattern.name == "Microservices" else "vertical",
                    data_stores=[],
                    tech_stack=[],
                    deployment_strategy="container"
                )
                components.append(component)
        
        # Use LLM to refine and add domain-specific components
        system_prompt = """You are designing system components. 
        
        Based on the analysis and selected patterns, identify:
        1. Domain-specific services needed
        2. Data stores required
        3. External integrations
        4. Supporting infrastructure
        
        Return a list of components with their responsibilities."""
        
        prompt = f"Analysis: {json.dumps(analysis)}\nPatterns: {[p.name for p in patterns]}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.3
        )
        
        # Parse and add domain-specific components
        try:
            domain_components = json.loads(response.content)
            for comp in domain_components.get('components', []):
                components.append(SystemComponent(
                    name=comp['name'],
                    type=comp.get('type', 'service'),
                    responsibilities=comp.get('responsibilities', []),
                    interfaces=comp.get('interfaces', []),
                    dependencies=comp.get('dependencies', []),
                    scalability_profile=comp.get('scalability', 'horizontal'),
                    data_stores=comp.get('data_stores', []),
                    tech_stack=comp.get('tech_stack', []),
                    deployment_strategy=comp.get('deployment', 'container')
                ))
        except:
            pass
        
        return components
    
    async def _design_data_architecture(
        self,
        analysis: Dict[str, Any],
        components: List[SystemComponent]
    ) -> Dict[str, Any]:
        """Design data architecture (databases, caching, etc.)."""
        system_prompt = """You are a data architect designing the data layer.
        
        Design:
        1. Database selection (SQL vs NoSQL, specific technologies)
        2. Data modeling (entities, relationships)
        3. Caching strategy
        4. Data partitioning/sharding approach
        5. Backup and recovery strategy
        6. Data consistency model
        
        Consider CAP theorem, data volume, access patterns."""
        
        prompt = f"Analysis: {json.dumps(analysis)}\nComponents: {[c.name for c in components]}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.3
        )
        
        try:
            return json.loads(response.content)
        except:
            return {"design": response.content, "raw": True}
    
    async def _design_integrations(
        self,
        components: List[SystemComponent]
    ) -> Dict[str, Any]:
        """Design integration points between components."""
        integrations = {
            "synchronous": [],
            "asynchronous": [],
            "external_apis": [],
            "communication_patterns": []
        }
        
        # Generate integration matrix
        for i, comp1 in enumerate(components):
            for comp2 in components[i+1:]:
                # Determine if integration is needed
                if any(dep in comp2.name for dep in comp1.dependencies):
                    integrations["synchronous"].append({
                        "from": comp1.name,
                        "to": comp2.name,
                        "protocol": "REST/gRPC"
                    })
        
        return integrations
    
    async def _design_deployment(
        self,
        components: List[SystemComponent],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Design deployment architecture."""
        return {
            "strategy": "container_orchestration",
            "platform": constraints.get('cloud_provider', 'kubernetes'),
            "environments": ["dev", "staging", "prod"],
            "ci_cd": {
                "pipeline": "automated",
                "testing": "comprehensive",
                "deployment": "blue_green"
            },
            "monitoring": {
                "metrics": "prometheus",
                "logging": "elasticsearch",
                "tracing": "jaeger"
            }
        }
    
    async def _generate_adrs(
        self,
        patterns: List[ArchitecturePattern],
        analysis: Dict[str, Any]
    ) -> List[DesignDecision]:
        """Generate Architecture Decision Records."""
        decisions = []
        
        for i, pattern in enumerate(patterns):
            decision = DesignDecision(
                id=f"ADR-{i+1:03d}",
                title=f"Adopt {pattern.name}",
                context=analysis.get('rationale', 'Architecture design'),
                decision=f"We will use {pattern.name} to address {', '.join(pattern.best_for)}",
                consequences=pattern.pros + [f"CON: {con}" for con in pattern.cons],
                alternatives_considered=[p.name for p in self.patterns_db.values() if p != pattern][:3]
            )
            decisions.append(decision)
        
        return decisions
    
    async def _generate_diagrams(
        self,
        components: List[SystemComponent],
        patterns: List[ArchitecturePattern]
    ) -> Dict[str, str]:
        """Generate architecture diagrams (as code)."""
        # Generate Mermaid diagrams
        diagrams = {}
        
        # Component diagram
        mermaid = "graph TD\n"
        for comp in components:
            mermaid += f"    {comp.name}[{comp.name}]\n"
        
        # Add connections
        for comp in components:
            for dep in comp.dependencies:
                mermaid += f"    {comp.name} --> {dep}\n"
        
        diagrams["component"] = mermaid
        
        return diagrams
    
    async def _create_roadmap(
        self,
        components: List[SystemComponent]
    ) -> List[Dict[str, Any]]:
        """Create implementation roadmap."""
        roadmap = []
        
        # Phase 1: Foundation
        roadmap.append({
            "phase": 1,
            "name": "Foundation",
            "duration": "2-3 weeks",
            "tasks": [
                "Set up CI/CD pipeline",
                "Create base project structure",
                "Implement core infrastructure",
                "Set up monitoring and logging"
            ]
        })
        
        # Phase 2: Core Services
        roadmap.append({
            "phase": 2,
            "name": "Core Services",
            "duration": "4-6 weeks",
            "tasks": [f"Implement {comp.name}" for comp in components[:3]]
        })
        
        # Phase 3: Integration
        roadmap.append({
            "phase": 3,
            "name": "Integration & Testing",
            "duration": "3-4 weeks",
            "tasks": [
                "Service integration",
                "End-to-end testing",
                "Performance testing",
                "Security audit"
            ]
        })
        
        return roadmap


class SecurityAuditEngine:
    """
    Advanced security audit engine for vulnerability detection.
    Performs static analysis, dependency scanning, and secure code review.
    """
    
    # OWASP Top 10 2021
    OWASP_CATEGORIES = {
        "A01": "Broken Access Control",
        "A02": "Cryptographic Failures",
        "A03": "Injection",
        "A04": "Insecure Design",
        "A05": "Security Misconfiguration",
        "A06": "Vulnerable and Outdated Components",
        "A07": "Identification and Authentication Failures",
        "A08": "Software and Data Integrity Failures",
        "A09": "Security Logging and Monitoring Failures",
        "A10": "Server-Side Request Forgery (SSRF)"
    }
    
    # CWE Top 25
    CRITICAL_VULNERABILITIES = [
        "CWE-79",   # XSS
        "CWE-787",  # Out-of-bounds Write
        "CWE-20",   # Improper Input Validation
        "CWE-125",  # Out-of-bounds Read
        "CWE-78",   # OS Command Injection
        "CWE-89",   # SQL Injection
        "CWE-416",  # Use After Free
        "CWE-22",   # Path Traversal
        "CWE-352",  # CSRF
        "CWE-434",  # Unrestricted File Upload
    ]
    
    def __init__(self, llm_interface):
        self.llm = llm_interface
        self.vulnerability_db = self._load_vulnerability_patterns()
    
    def _load_vulnerability_patterns(self) -> Dict[str, Any]:
        """Load vulnerability detection patterns."""
        return {
            "sql_injection": {
                "pattern": r"(SELECT|INSERT|UPDATE|DELETE).*\+.*\$",
                "severity": "critical",
                "cwe": "CWE-89",
                "owasp": "A03"
            },
            "command_injection": {
                "pattern": r"(exec|system|eval)\s*\(.*\$",
                "severity": "critical",
                "cwe": "CWE-78",
                "owasp": "A03"
            },
            "hardcoded_secrets": {
                "pattern": r"(password|secret|key|token)\s*=\s*[\"'][^\"']+[\"']",
                "severity": "high",
                "cwe": "CWE-798",
                "owasp": "A02"
            },
            "insecure_random": {
                "pattern": r"Math\.random\(\)|random\.random\(",
                "severity": "medium",
                "cwe": "CWE-338",
                "owasp": "A02"
            },
            "xss_vulnerability": {
                "pattern": r"innerHTML.*\+|document\.write.*\+",
                "severity": "high",
                "cwe": "CWE-79",
                "owasp": "A03"
            },
            "path_traversal": {
                "pattern": r"open\s*\(.*\+.*\)|readFile.*\+",
                "severity": "high",
                "cwe": "CWE-22",
                "owasp": "A01"
            },
        }
    
    async def perform_security_audit(
        self,
        project_path: str,
        file_paths: List[str]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive security audit.
        
        Args:
            project_path: Path to project
            file_paths: List of files to audit
            
        Returns:
            Complete security audit report
        """
        findings = []
        
        # 1. Static analysis
        for file_path in file_paths:
            file_findings = await self._analyze_file_security(file_path)
            findings.extend(file_findings)
        
        # 2. Dependency scanning
        dependency_findings = await self._scan_dependencies(project_path)
        findings.extend(dependency_findings)
        
        # 3. Configuration audit
        config_findings = await self._audit_configuration(project_path)
        findings.extend(config_findings)
        
        # 4. Architecture security review
        architecture_findings = await self._review_architecture_security(project_path)
        findings.extend(architecture_findings)
        
        # 5. Generate report
        report = self._generate_security_report(findings)
        
        return report
    
    async def _analyze_file_security(self, file_path: str) -> List[SecurityVulnerability]:
        """Analyze single file for security issues."""
        findings = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Pattern-based detection
            for vuln_name, vuln_info in self.vulnerability_db.items():
                import re
                pattern = re.compile(vuln_info['pattern'], re.IGNORECASE)
                
                for i, line in enumerate(lines, 1):
                    if pattern.search(line):
                        finding = SecurityVulnerability(
                            severity=vuln_info['severity'],
                            category=vuln_name,
                            file_path=file_path,
                            line_number=i,
                            description=f"Potential {vuln_name.replace('_', ' ')} detected",
                            cwe_id=vuln_info.get('cwe'),
                            owasp_category=vuln_info.get('owasp'),
                            code_snippet=line.strip()
                        )
                        findings.append(finding)
            
            # LLM-based deep analysis
            llm_findings = await self._llm_security_analysis(file_path, content)
            findings.extend(llm_findings)
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return findings
    
    async def _llm_security_analysis(
        self,
        file_path: str,
        content: str
    ) -> List[SecurityVulnerability]:
        """Use LLM for advanced security analysis."""
        system_prompt = """You are a security expert performing code review.
        
        Analyze the code for:
        1. Injection vulnerabilities (SQL, NoSQL, Command, LDAP)
        2. Authentication/authorization flaws
        3. Sensitive data exposure
        4. XML/XXE vulnerabilities
        5. Broken access control
        6. Security misconfigurations
        7. Insecure deserialization
        8. Insufficient logging
        9. SSRF vulnerabilities
        10. Cryptographic weaknesses
        
        For each finding, provide:
        - Severity (critical/high/medium/low)
        - Line number
        - Description of vulnerability
        - CWE ID if applicable
        - Remediation advice
        
        Return findings as JSON array."""
        
        prompt = f"File: {file_path}\n\n```\n{content[:4000]}\n```"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.2
        )
        
        findings = []
        try:
            data = json.loads(response.content)
            for finding in data.get('findings', []):
                vuln = SecurityVulnerability(
                    severity=finding['severity'],
                    category=finding.get('category', 'unknown'),
                    file_path=file_path,
                    line_number=finding['line_number'],
                    description=finding['description'],
                    cwe_id=finding.get('cwe_id'),
                    owasp_category=finding.get('owasp_category'),
                    remediation=finding.get('remediation'),
                    code_snippet=finding.get('code_snippet')
                )
                findings.append(vuln)
        except:
            pass
        
        return findings
    
    async def _scan_dependencies(self, project_path: str) -> List[SecurityVulnerability]:
        """Scan dependencies for known vulnerabilities."""
        findings = []
        
        # Check for requirements.txt (Python)
        req_file = Path(project_path) / "requirements.txt"
        if req_file.exists():
            # This would integrate with safety-db or similar
            # For now, check for common vulnerable packages
            content = req_file.read_text()
            
            vulnerable_packages = [
                ("django<3.0", "CVE-2021-35042", "critical"),
                ("flask<1.0", "CVE-2018-1000656", "high"),
                ("requests<2.20", "CVE-2018-18074", "medium"),
            ]
            
            for package, cve, severity in vulnerable_packages:
                if package.split('<')[0] in content.lower():
                    findings.append(SecurityVulnerability(
                        severity=severity,
                        category="vulnerable_dependency",
                        file_path=str(req_file),
                        line_number=0,
                        description=f"Potentially vulnerable package: {package} ({cve})",
                        cwe_id="CWE-1035",
                        owasp_category="A06"
                    ))
        
        # Check for package.json (Node.js)
        pkg_file = Path(project_path) / "package.json"
        if pkg_file.exists():
            content = pkg_file.read_text()
            
            vulnerable_npm = [
                ("lodash", "CVE-2019-10744", "critical"),
                ("minimatch", "CVE-2022-3517", "high"),
            ]
            
            for package, cve, severity in vulnerable_npm:
                if package in content.lower():
                    findings.append(SecurityVulnerability(
                        severity=severity,
                        category="vulnerable_dependency",
                        file_path=str(pkg_file),
                        line_number=0,
                        description=f"Potentially vulnerable package: {package} ({cve})",
                        cwe_id="CWE-1035",
                        owasp_category="A06"
                    ))
        
        return findings
    
    async def _audit_configuration(self, project_path: str) -> List[SecurityVulnerability]:
        """Audit configuration files for security issues."""
        findings = []
        
        # Check .env files
        env_files = list(Path(project_path).glob("**/.env*"))
        for env_file in env_files:
            if '.gitignore' not in str(env_file):
                # Check if .env is in .gitignore
                gitignore = Path(project_path) / ".gitignore"
                if gitignore.exists():
                    gitignore_content = gitignore.read_text()
                    if '.env' not in gitignore_content:
                        findings.append(SecurityVulnerability(
                            severity="high",
                            category="security_misconfiguration",
                            file_path=str(env_file),
                            line_number=0,
                            description=".env file may be committed to version control",
                            cwe_id="CWE-798",
                            owasp_category="A05"
                        ))
        
        # Check for debug mode in production
        settings_files = list(Path(project_path).glob("**/settings.py")) + \
                        list(Path(project_path).glob("**/config.py"))
        
        for settings_file in settings_files:
            content = settings_file.read_text()
            if 'DEBUG = True' in content:
                findings.append(SecurityVulnerability(
                    severity="high",
                    category="security_misconfiguration",
                    file_path=str(settings_file),
                    line_number=0,
                    description="DEBUG mode enabled - should be False in production",
                    cwe_id="CWE-489",
                    owasp_category="A05"
                ))
        
        return findings
    
    async def _review_architecture_security(self, project_path: str) -> List[SecurityVulnerability]:
        """Review overall architecture for security."""
        findings = []
        
        # Check for authentication mechanisms
        auth_files = list(Path(project_path).glob("**/auth*.py")) + \
                    list(Path(project_path).glob("**/authentication*.py"))
        
        if not auth_files:
            findings.append(SecurityVulnerability(
                severity="medium",
                category="missing_authentication",
                file_path=project_path,
                line_number=0,
                description="No authentication module found - ensure all endpoints are protected",
                cwe_id="CWE-306",
                owasp_category="A07"
            ))
        
        return findings
    
    def _generate_security_report(self, findings: List[SecurityVulnerability]) -> Dict[str, Any]:
        """Generate comprehensive security report."""
        critical = [f for f in findings if f.severity == "critical"]
        high = [f for f in findings if f.severity == "high"]
        medium = [f for f in findings if f.severity == "medium"]
        low = [f for f in findings if f.severity == "low"]
        
        # Group by OWASP category
        owasp_summary = {}
        for finding in findings:
            category = finding.owasp_category or "Unknown"
            if category not in owasp_summary:
                owasp_summary[category] = []
            owasp_summary[category].append(finding)
        
        # Calculate security score
        score = 100
        score -= len(critical) * 20
        score -= len(high) * 10
        score -= len(medium) * 3
        score -= len(low) * 1
        score = max(0, score)
        
        return {
            "summary": {
                "total_findings": len(findings),
                "critical": len(critical),
                "high": len(high),
                "medium": len(medium),
                "low": len(low),
                "security_score": score,
                "grade": self._calculate_grade(score)
            },
            "findings": [
                {
                    "severity": f.severity,
                    "category": f.category,
                    "file": f.file_path,
                    "line": f.line_number,
                    "description": f.description,
                    "cwe": f.cwe_id,
                    "owasp": f.owasp_category,
                    "remediation": f.remediation,
                    "code": f.code_snippet
                }
                for f in findings
            ],
            "owasp_summary": {
                cat: len(items) for cat, items in owasp_summary.items()
            },
            "recommendations": self._generate_recommendations(findings)
        }
    
    def _calculate_grade(self, score: int) -> str:
        """Calculate letter grade from score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _generate_recommendations(self, findings: List[SecurityVulnerability]) -> List[str]:
        """Generate prioritized recommendations."""
        recommendations = []
        
        # Critical recommendations
        critical_cats = set(f.category for f in findings if f.severity == "critical")
        if critical_cats:
            recommendations.append(f"IMMEDIATE: Fix {len(critical_cats)} critical vulnerabilities")
        
        if any(f.cwe_id == "CWE-89" for f in findings):
            recommendations.append("Implement parameterized queries to prevent SQL injection")
        
        if any(f.cwe_id == "CWE-78" for f in findings):
            recommendations.append("Avoid using exec/system calls with user input")
        
        if any(f.category == "vulnerable_dependency" for f in findings):
            recommendations.append("Update dependencies to latest secure versions")
        
        if not any(f.category == "security_logging" for f in findings):
            recommendations.append("Add comprehensive security logging and monitoring")
        
        return recommendations


class DomainExpertSystem:
    """
    Domain-specific expertise system for specialized industries.
    Provides regulatory compliance, business rules, and domain patterns.
    """
    
    def __init__(self):
        self.domains = self._initialize_domains()
    
    def _initialize_domains(self) -> Dict[str, DomainModel]:
        """Initialize domain knowledge bases."""
        return {
            "healthcare": DomainModel(
                domain="healthcare",
                entities=[
                    {"name": "Patient", "sensitivity": "PHI", "attributes": ["id", "name", "dob", "medical_history"]},
                    {"name": "Provider", "sensitivity": "PII", "attributes": ["id", "name", "npi", "specialty"]},
                    {"name": "Encounter", "sensitivity": "PHI", "attributes": ["id", "patient_id", "date", "diagnosis"]},
                    {"name": "Prescription", "sensitivity": "PHI", "attributes": ["id", "patient_id", "medication", "dosage"]},
                ],
                business_rules=[
                    "Patient data must be encrypted at rest and in transit",
                    "Access to PHI requires authentication and authorization",
                    "Audit logs must record all access to patient data",
                    "Data retention policies must comply with state laws",
                ],
                compliance_requirements=[
                    "HIPAA Privacy Rule",
                    "HIPAA Security Rule",
                    "HITECH Act",
                    "State medical privacy laws",
                ],
                data_sensitivity_levels={
                    "PHI": "high",  # Protected Health Information
                    "PII": "medium",  # Personally Identifiable Information
                    "general": "low"
                },
                common_patterns=[
                    ArchitecturePattern(
                        name="FHIR Integration",
                        category="integration",
                        description="Integrate with FHIR APIs for healthcare data exchange",
                        components=[],
                        data_flow=[],
                        pros=["interoperability", "standards_compliance"],
                        cons=["complexity"],
                        best_for=["healthcare_apps"],
                        anti_patterns=["custom_protocols"],
                        implementation_steps=[]
                    )
                ],
                regulatory_frameworks=["HIPAA", "HITECH", "FDA"]
            ),
            
            "finance": DomainModel(
                domain="finance",
                entities=[
                    {"name": "Account", "sensitivity": "financial", "attributes": ["id", "balance", "type", "owner_id"]},
                    {"name": "Transaction", "sensitivity": "financial", "attributes": ["id", "account_id", "amount", "type"]},
                    {"name": "Customer", "sensitivity": "PII", "attributes": ["id", "name", "ssn", "address"]},
                ],
                business_rules=[
                    "All transactions must be immutable and auditable",
                    "Account balances must be consistent (ACID)",
                    "Fraud detection must run on all transactions",
                    "Multi-factor authentication required for high-value transactions",
                ],
                compliance_requirements=[
                    "PCI DSS",
                    "SOX",
                    "GDPR",
                    "GLBA",
                    "KYC/AML",
                ],
                data_sensitivity_levels={
                    "financial": "high",
                    "PII": "high",
                    "transactional": "medium",
                },
                common_patterns=[],
                regulatory_frameworks=["PCI_DSS", "SOX", "GDPR", "GLBA"]
            ),
            
            "ecommerce": DomainModel(
                domain="ecommerce",
                entities=[
                    {"name": "Product", "sensitivity": "general", "attributes": ["id", "name", "price", "inventory"]},
                    {"name": "Order", "sensitivity": "financial", "attributes": ["id", "customer_id", "items", "total"]},
                    {"name": "Customer", "sensitivity": "PII", "attributes": ["id", "email", "address", "payment_info"]},
                    {"name": "Cart", "sensitivity": "low", "attributes": ["id", "customer_id", "items"]},
                ],
                business_rules=[
                    "Inventory must be checked before order confirmation",
                    "Prices must be consistent across checkout flow",
                    "Payment processing must be PCI compliant",
                    "Order confirmations must be sent within 1 minute",
                ],
                compliance_requirements=[
                    "PCI DSS",
                    "GDPR",
                    "Consumer protection laws",
                ],
                data_sensitivity_levels={
                    "financial": "high",
                    "PII": "medium",
                    "general": "low",
                },
                common_patterns=[],
                regulatory_frameworks=["PCI_DSS", "GDPR"]
            ),
        }
    
    def get_domain(self, domain_name: str) -> Optional[DomainModel]:
        """Get domain model by name."""
        return self.domains.get(domain_name.lower())
    
    async def analyze_domain_requirements(
        self,
        requirements: str,
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze requirements with domain expertise."""
        
        # Auto-detect domain if not specified
        if not domain:
            domain = await self._detect_domain(requirements)
        
        domain_model = self.get_domain(domain)
        
        if not domain_model:
            return {"domain": "generic", "compliance": []}
        
        return {
            "domain": domain,
            "entities": domain_model.entities,
            "business_rules": domain_model.business_rules,
            "compliance_requirements": domain_model.compliance_requirements,
            "data_sensitivity": domain_model.data_sensitivity_levels,
            "patterns": domain_model.common_patterns,
            "regulatory_frameworks": domain_model.regulatory_frameworks
        }
    
    async def _detect_domain(self, requirements: str) -> str:
        """Auto-detect domain from requirements."""
        requirements_lower = requirements.lower()
        
        healthcare_keywords = ['patient', 'medical', 'health', 'doctor', 'prescription', 'diagnosis', 'hipaa']
        finance_keywords = ['bank', 'transaction', 'payment', 'account', 'investment', 'trading', 'pci']
        ecommerce_keywords = ['product', 'cart', 'checkout', 'order', 'inventory', 'shipping']
        
        scores = {
            'healthcare': sum(1 for kw in healthcare_keywords if kw in requirements_lower),
            'finance': sum(1 for kw in finance_keywords if kw in requirements_lower),
            'ecommerce': sum(1 for kw in ecommerce_keywords if kw in requirements_lower),
        }
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'generic'


class AmbiguityResolver:
    """
    Handles ambiguous requirements through clarification and reasoning.
    Uses advanced prompting techniques to handle uncertainty.
    """
    
    def __init__(self, llm_interface):
        self.llm = llm_interface
        self.clarification_history = []
    
    async def resolve_ambiguity(
        self,
        request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolve ambiguous requirements through reasoning.
        
        Returns either:
        - Clarification questions if too ambiguous
        - Reasoned decision with assumptions if manageable
        """
        
        # Step 1: Analyze ambiguity level
        ambiguity_analysis = await self._analyze_ambiguity(request)
        
        if ambiguity_analysis['level'] == 'high':
            # Too ambiguous - need clarification
            return await self._generate_clarification_questions(request, ambiguity_analysis)
        
        elif ambiguity_analysis['level'] == 'medium':
            # Make reasonable assumptions
            return await self._make_reasoned_assumptions(request, ambiguity_analysis)
        
        else:
            # Low ambiguity - proceed with confidence
            return {
                'status': 'proceed',
                'reasoning': ambiguity_analysis.get('reasoning'),
                'assumptions': [],
                'confidence': 0.9
            }
    
    async def _analyze_ambiguity(self, request: str) -> Dict[str, Any]:
        """Analyze the level of ambiguity in the request."""
        
        system_prompt = """You are analyzing requirements for ambiguity.
        
        Analyze the request and determine:
        1. Ambiguity level (low/medium/high)
        2. Specific unclear aspects
        3. Missing information
        4. Multiple possible interpretations
        5. Technical uncertainty
        
        Return JSON with:
        - level: "low", "medium", or "high"
        - unclear_aspects: list of specific ambiguities
        - missing_info: what's not specified
        - possible_interpretations: different ways to interpret
        - reasoning: explanation of your assessment"""
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=f"Request: {request}",
            temperature=0.3
        )
        
        try:
            return json.loads(response.content)
        except:
            return {'level': 'medium', 'unclear_aspects': [], 'reasoning': 'default'}
    
    async def _generate_clarification_questions(
        self,
        request: str,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate specific clarification questions."""
        
        system_prompt = """Generate specific clarification questions to resolve ambiguities.
        
        Rules:
        - Ask one question per ambiguity
        - Provide multiple-choice options when possible
        - Prioritize by importance
        - Suggest reasonable defaults"""
        
        prompt = f"Request: {request}\nAmbiguities: {json.dumps(analysis.get('unclear_aspects', []))}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.3
        )
        
        try:
            questions = json.loads(response.content)
        except:
            questions = {'questions': ['Could you provide more details about your requirements?']}
        
        return {
            'status': 'clarification_needed',
            'questions': questions.get('questions', []),
            'reasoning': analysis.get('reasoning')
        }
    
    async def _make_reasoned_assumptions(
        self,
        request: str,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make reasonable assumptions for medium ambiguity."""
        
        system_prompt = """Make reasonable assumptions to proceed with implementation.
        
        For each ambiguity:
        1. State the assumption clearly
        2. Explain the reasoning
        3. Note that this can be changed later
        4. Choose the most common/best practice option
        
        Be conservative - prefer standard approaches over exotic ones."""
        
        prompt = f"Request: {request}\nAmbiguities: {json.dumps(analysis.get('unclear_aspects', []))}"
        
        response = await self.llm.generate(
            system=system_prompt,
            prompt=prompt,
            temperature=0.3
        )
        
        try:
            assumptions = json.loads(response.content)
        except:
            assumptions = {'assumptions': ['Using standard industry practices']}
        
        return {
            'status': 'proceed_with_assumptions',
            'assumptions': assumptions.get('assumptions', []),
            'reasoning': analysis.get('reasoning'),
            'confidence': 0.7,
            'note': 'Assumptions can be adjusted based on feedback'
        }


# Integration with main agent
class AdvancedGoatCodeAgent:
    """
    Enhanced GOATCODE agent with architecture, security, and domain expertise.
    """
    
    def __init__(self, llm_interface, config=None):
        self.llm = llm_interface
        self.config = config or {}
        
        # Initialize specialized engines
        self.architecture = ArchitectureEngine(llm_interface)
        self.security = SecurityAuditEngine(llm_interface)
        self.domain = DomainExpertSystem()
        self.ambiguity = AmbiguityResolver(llm_interface)
    
    async def execute_advanced(
        self,
        prompt: str,
        project_path: str,
        domain: Optional[str] = None,
        capabilities: List[AgentCapability] = None
    ) -> Dict[str, Any]:
        """
        Execute with advanced capabilities.
        
        Args:
            prompt: User request
            project_path: Project directory
            domain: Specific domain (healthcare, finance, etc.)
            capabilities: List of capabilities to use
        """
        capabilities = capabilities or [
            AgentCapability.ARCHITECTURE_DESIGN,
            AgentCapability.SECURITY_AUDIT,
            AgentCapability.DOMAIN_EXPERTISE
        ]
        
        results = {}
        
        # 1. Handle ambiguity
        ambiguity_result = await self.ambiguity.resolve_ambiguity(prompt, {})
        if ambiguity_result['status'] == 'clarification_needed':
            return {
                'status': 'clarification_needed',
                'questions': ambiguity_result['questions']
            }
        
        results['assumptions'] = ambiguity_result.get('assumptions', [])
        
        # 2. Domain analysis
        if AgentCapability.DOMAIN_EXPERTISE in capabilities:
            domain_analysis = await self.domain.analyze_domain_requirements(prompt, domain)
            results['domain_analysis'] = domain_analysis
        
        # 3. Architecture design (for complex requests)
        if AgentCapability.ARCHITECTURE_DESIGN in capabilities:
            # Check if request involves architecture
            if any(kw in prompt.lower() for kw in ['architecture', 'system design', 'microservices', 'database design']):
                architecture = await self.architecture.design_system_architecture(
                    requirements={'prompt': prompt},
                    constraints={'project_path': project_path}
                )
                results['architecture'] = architecture
        
        # 4. Security audit (if code exists)
        if AgentCapability.SECURITY_AUDIT in capabilities:
            import os
            if os.path.exists(project_path):
                # Find relevant files
                files = []
                for root, dirs, filenames in os.walk(project_path):
                    for f in filenames:
                        if f.endswith(('.py', '.js', '.ts', '.java', '.go')):
                            files.append(os.path.join(root, f))
                
                if files[:20]:  # Limit to first 20 files
                    security_report = await self.security.perform_security_audit(
                        project_path, files[:20]
                    )
                    results['security_audit'] = security_report
        
        return results


# Export
__all__ = [
    'ArchitectureEngine',
    'SecurityAuditEngine', 
    'DomainExpertSystem',
    'AmbiguityResolver',
    'AdvancedGoatCodeAgent',
    'AgentCapability',
    'ArchitecturePattern',
    'SecurityVulnerability',
    'DomainModel',
    'SystemComponent',
    'DesignDecision'
]
