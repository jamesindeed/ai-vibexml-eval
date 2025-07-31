"""
Test Cases for LLML Evaluation

This module contains carefully designed test cases where structured formatting
should provide measurable advantages over raw text concatenation.

Each test case is designed to highlight specific aspects where hierarchical
data organization improves AI comprehension and response quality.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class StructuredTestCase:
    """
    A test case designed to evaluate structured vs unstructured data formatting.

    Attributes:
        name: Unique identifier for the test case
        description: Human-readable description of the scenario
        data: The structured data to be formatted
        task: The specific task the AI should perform
        category: Type of test case (structured_advantage, neutral, creative, factual, computational, adversarial)
        why_structure_helps: Explanation of why structured formatting should help (or why it shouldn't)
        expected_advantages: List of specific improvements expected from structured format (or potential disadvantages)
    """

    name: str
    description: str
    data: Dict[str, Any]
    task: str
    category: str
    why_structure_helps: str
    expected_advantages: List[str]


class TestCaseDataset:
    """
    Curated dataset of test cases for LLML evaluation.

    These test cases are specifically designed to highlight scenarios where
    structured data formatting provides measurable advantages in AI comprehension.
    """

    @classmethod
    def get_all_cases(cls) -> List[StructuredTestCase]:
        """Get all test cases in the dataset."""
        return [
            # Structured advantage cases (15)
            cls.nested_conditional_logic(),
            cls.workflow_dependencies(),
            cls.hierarchical_analysis(),
            cls.configuration_parsing(),
            cls.multi_context_decisions(),
            cls.financial_risk_assessment(),
            cls.medical_treatment_protocol(),
            cls.security_access_control(),
            cls.supply_chain_optimization(),
            cls.scientific_experiment_design(),
            cls.legal_compliance_analysis(),
            cls.infrastructure_capacity_planning(),
            cls.educational_curriculum_mapping(),
            cls.investment_portfolio_analysis(),
            cls.regulatory_policy_interpretation(),
            # Neutral cases (3)
            cls.basic_factual_question(),
            cls.weather_report(),
            # Computational cases (1)
            cls.simple_calculation(),
            # Creative cases (2)
            cls.creative_story_writing(),
            cls.poem_composition(),
            # Adversarial cases (2)
            cls.conversational_advice(),
            cls.stream_of_consciousness(),
        ]

    @classmethod
    def get_cases_by_category(cls, category: str) -> List[StructuredTestCase]:
        """Get test cases filtered by category."""
        all_cases = cls.get_all_cases()
        return [case for case in all_cases if case.category == category]

    @classmethod
    def get_available_categories(cls) -> List[str]:
        """Get list of all available test case categories."""
        return [
            "structured_advantage",
            "neutral",
            "computational",
            "creative",
            "adversarial",
        ]

    @classmethod
    def nested_conditional_logic(cls) -> StructuredTestCase:
        """Test case with complex nested conditional logic and dependencies."""
        return StructuredTestCase(
            name="nested_conditional_logic",
            description="Complex deployment decision tree with nested conditions and approval matrices",
            data={
                "deployment_request": {
                    "application": "payment-service",
                    "version": "v2.1.0",
                    "environment": "production",
                    "rollback_version": "v2.0.3",
                },
                "conditions": {
                    "safety_checks": {
                        "database_migration": {
                            "required": True,
                            "backwards_compatible": False,
                            "estimated_downtime": "15 minutes",
                        },
                        "traffic_requirements": {
                            "peak_hours": "9am-5pm EST",
                            "max_error_rate": "0.1%",
                            "canary_percentage": 5,
                        },
                    },
                    "approval_matrix": {
                        "database_changes": ["dba-team", "tech-lead"],
                        "production_deploy": ["engineering-manager"],
                        "emergency_rollback": ["on-call-engineer"],
                    },
                },
                "current_status": {
                    "time": "2:30 PM EST",
                    "error_rate": "0.05%",
                    "database_locked": False,
                    "approvals_received": ["dba-team", "tech-lead"],
                },
            },
            task="Analyze the deployment request and determine the exact sequence of actions needed, including who needs to approve each step and what conditions must be met.",
            category="structured_advantage",
            why_structure_helps="Nested conditions, approval dependencies, and multi-level decision logic are clearer when hierarchically organized",
            expected_advantages=[
                "Correctly identify all required approvals",
                "Sequence actions based on dependencies",
                "Reference specific safety thresholds",
                "Handle nested conditional logic accurately",
            ],
        )

    @classmethod
    def workflow_dependencies(cls) -> StructuredTestCase:
        """Test case with complex workflow dependencies and conditional execution."""
        return StructuredTestCase(
            name="workflow_dependencies",
            description="CI/CD pipeline with conditional steps and complex dependency chains",
            data={
                "pipeline": "frontend-build",
                "trigger": {
                    "type": "pull_request",
                    "branch": "feature/checkout-redesign",
                    "files_changed": [
                        "src/checkout/",
                        "tests/checkout/",
                        "api/payment.ts",
                    ],
                },
                "stages": {
                    "validate": {
                        "depends_on": [],
                        "parallel": True,
                        "steps": [
                            {"name": "lint", "timeout": 5, "required": True},
                            {"name": "type-check", "timeout": 3, "required": True},
                            {"name": "security-scan", "timeout": 10, "required": False},
                        ],
                    },
                    "test": {
                        "depends_on": ["validate"],
                        "parallel": False,
                        "conditional": "if files_changed includes src/ or tests/",
                        "steps": [
                            {"name": "unit-tests", "timeout": 15, "required": True},
                            {
                                "name": "integration-tests",
                                "timeout": 20,
                                "required": True,
                                "condition": "if api/ files changed",
                            },
                            {
                                "name": "e2e-tests",
                                "timeout": 30,
                                "required": False,
                                "condition": "if checkout/ files changed",
                            },
                        ],
                    },
                    "build": {
                        "depends_on": ["test"],
                        "parallel": False,
                        "steps": [
                            {"name": "compile", "timeout": 10, "required": True},
                            {"name": "bundle", "timeout": 5, "required": True},
                            {"name": "optimize", "timeout": 8, "required": False},
                        ],
                    },
                },
                "environment": {
                    "node_version": "18.x",
                    "cache_enabled": True,
                    "max_parallel_jobs": 3,
                },
            },
            task="Generate the exact execution plan for this pipeline, including which steps run in parallel, conditional execution logic, and total estimated timeline.",
            category="structured_advantage",
            why_structure_helps="Complex dependencies and conditional logic require understanding hierarchical relationships that are clearer in structured format",
            expected_advantages=[
                "Correctly identify parallel vs sequential execution",
                "Apply conditional logic based on file changes",
                "Calculate realistic timeline with dependencies",
                "Reference specific timeout values and conditions",
            ],
        )

    @classmethod
    def hierarchical_analysis(cls) -> StructuredTestCase:
        """Test case requiring analysis of hierarchical organizational data."""
        return StructuredTestCase(
            name="hierarchical_analysis",
            description="Complex organizational analysis requiring understanding of reporting structures and resource allocation",
            data={
                "organization": {
                    "department": "Engineering",
                    "budget": {"annual": 2400000, "remaining_q4": 320000},
                    "teams": [
                        {
                            "name": "Backend Platform",
                            "manager": {
                                "name": "Sarah Chen",
                                "level": "Senior Manager",
                            },
                            "budget_allocation": 0.4,
                            "members": [
                                {
                                    "name": "Alex",
                                    "level": "Staff",
                                    "salary": 180000,
                                    "skills": ["golang", "kubernetes"],
                                },
                                {
                                    "name": "Jordan",
                                    "level": "Senior",
                                    "salary": 150000,
                                    "skills": ["python", "databases"],
                                },
                                {
                                    "name": "Casey",
                                    "level": "Mid",
                                    "salary": 120000,
                                    "skills": ["java", "microservices"],
                                },
                            ],
                            "projects": [
                                {
                                    "name": "API Gateway",
                                    "priority": "P0",
                                    "budget": 400000,
                                    "completion": 0.8,
                                },
                                {
                                    "name": "Data Pipeline",
                                    "priority": "P1",
                                    "budget": 200000,
                                    "completion": 0.3,
                                },
                            ],
                        },
                        {
                            "name": "Frontend Experience",
                            "manager": {"name": "Mike Rodriguez", "level": "Manager"},
                            "budget_allocation": 0.35,
                            "members": [
                                {
                                    "name": "Taylor",
                                    "level": "Staff",
                                    "salary": 175000,
                                    "skills": ["react", "typescript"],
                                },
                                {
                                    "name": "Riley",
                                    "level": "Senior",
                                    "salary": 145000,
                                    "skills": ["vue", "design-systems"],
                                },
                                {
                                    "name": "Morgan",
                                    "level": "Junior",
                                    "salary": 95000,
                                    "skills": ["javascript", "css"],
                                },
                            ],
                            "projects": [
                                {
                                    "name": "Mobile App",
                                    "priority": "P0",
                                    "budget": 350000,
                                    "completion": 0.6,
                                },
                                {
                                    "name": "Design System",
                                    "priority": "P2",
                                    "budget": 150000,
                                    "completion": 0.9,
                                },
                            ],
                        },
                    ],
                },
                "analysis_request": {
                    "focus": "budget_optimization",
                    "constraints": [
                        "maintain_p0_projects",
                        "no_layoffs",
                        "skill_gaps_ok",
                    ],
                    "deadline": "end_of_quarter",
                },
            },
            task="Analyze the organizational structure and provide specific recommendations for budget optimization, including project prioritization, potential restructuring, and skill gap analysis.",
            why_structure_helps="Hierarchical relationships between teams, budgets, projects, and skills require clear structural understanding for accurate analysis",
            category="structured_advantage",
            expected_advantages=[
                "Correctly calculate budget allocations and remaining funds",
                "Identify skill distribution patterns across teams",
                "Prioritize projects based on completion and priority levels",
                "Provide recommendations with numerical justification",
            ],
        )

    @classmethod
    def configuration_parsing(cls) -> StructuredTestCase:
        """Test case with complex configuration requiring precise parsing."""
        return StructuredTestCase(
            name="configuration_parsing",
            description="Kubernetes deployment configuration with multiple interdependent settings and reported issues",
            data={
                "deployment": {
                    "metadata": {"name": "web-app", "namespace": "production"},
                    "spec": {
                        "replicas": 3,
                        "strategy": {
                            "type": "RollingUpdate",
                            "rollingUpdate": {
                                "maxUnavailable": "25%",
                                "maxSurge": "25%",
                            },
                        },
                        "template": {
                            "spec": {
                                "containers": [
                                    {
                                        "name": "app",
                                        "image": "myapp:v2.1.0",
                                        "ports": [{"containerPort": 8080}],
                                        "env": [
                                            {
                                                "name": "DATABASE_URL",
                                                "valueFrom": {
                                                    "secretKeyRef": {
                                                        "name": "db-secret",
                                                        "key": "url",
                                                    }
                                                },
                                            },
                                            {
                                                "name": "REDIS_URL",
                                                "value": "redis://redis-service:6379",
                                            },
                                            {"name": "LOG_LEVEL", "value": "info"},
                                        ],
                                        "resources": {
                                            "requests": {
                                                "cpu": "100m",
                                                "memory": "256Mi",
                                            },
                                            "limits": {
                                                "cpu": "500m",
                                                "memory": "512Mi",
                                            },
                                        },
                                        "livenessProbe": {
                                            "httpGet": {
                                                "path": "/health",
                                                "port": 8080,
                                            },
                                            "initialDelaySeconds": 30,
                                            "periodSeconds": 10,
                                        },
                                    }
                                ]
                            }
                        },
                    },
                },
                "issues_reported": [
                    "Pods failing to start during deployment",
                    "Memory usage spiking during rolling updates",
                    "Health checks timing out intermittently",
                ],
            },
            task="Analyze this Kubernetes configuration and identify specific issues that could cause the reported problems. Provide exact configuration changes needed to resolve them.",
            why_structure_helps="Complex nested configuration requires understanding relationships between resources, probes, and deployment strategies",
            category="structured_advantage",
            expected_advantages=[
                "Identify specific configuration conflicts and paths",
                "Reference exact parameter values in nested structures",
                "Understand relationships between resource limits and health checks",
                "Provide precise configuration fixes with proper nesting",
            ],
        )

    @classmethod
    def multi_context_decisions(cls) -> StructuredTestCase:
        """Test case requiring decisions based on multiple interconnected contexts."""
        return StructuredTestCase(
            name="multi_context_decisions",
            description="Incident response requiring coordination across multiple systems, teams, and procedures",
            data={
                "incident": {
                    "id": "INC-2024-0142",
                    "severity": "P1",
                    "description": "Payment processing failures in US region",
                    "started_at": "2024-01-15T14:30:00Z",
                    "affected_services": [
                        "payment-api",
                        "user-notifications",
                        "order-fulfillment",
                    ],
                },
                "system_status": {
                    "payment_api": {
                        "region": "us-east-1",
                        "error_rate": "15%",
                        "response_time_p99": "2.5s",
                        "healthy_instances": 3,
                        "total_instances": 5,
                    },
                    "database": {
                        "primary": {
                            "status": "healthy",
                            "connections": 85,
                            "max_connections": 100,
                        },
                        "replica": {"status": "degraded", "replication_lag": "45s"},
                    },
                    "external_dependencies": {
                        "stripe_api": {"status": "operational", "latency": "normal"},
                        "fraud_service": {"status": "degraded", "error_rate": "8%"},
                    },
                },
                "team_availability": {
                    "on_call": {
                        "primary": {
                            "name": "Alex Kim",
                            "tz": "PST",
                            "responds_in": "5min",
                        },
                        "secondary": {
                            "name": "Jordan Liu",
                            "tz": "EST",
                            "responds_in": "15min",
                        },
                    },
                    "specialists": {
                        "database": {"available": True, "eta": "10min"},
                        "payments": {"available": False, "next_available": "2hrs"},
                        "infrastructure": {"available": True, "eta": "immediate"},
                    },
                },
                "runbooks": {
                    "payment_failures": {
                        "steps": [
                            "check_external_apis",
                            "verify_database_health",
                            "restart_degraded_instances",
                        ],
                        "escalation": "if error_rate > 10% for 15min, page payments team",
                    },
                    "database_issues": {
                        "steps": [
                            "check_replication_lag",
                            "verify_connection_pool",
                            "consider_failover",
                        ],
                        "escalation": "if lag > 60s, engage database team immediately",
                    },
                },
            },
            task="Create a complete incident response plan including immediate actions, team coordination, and escalation decisions based on current system status and team availability.",
            why_structure_helps="Multiple interconnected contexts (systems, teams, procedures) require understanding complex relationships and dependencies across different domains",
            category="structured_advantage",
            expected_advantages=[
                "Prioritize actions based on multiple factors (severity, availability, status)",
                "Reference specific thresholds and escalation criteria",
                "Coordinate effectively across different team specialties",
                "Adapt runbook procedures to current contextual state",
            ],
        )

    @classmethod
    def financial_risk_assessment(cls) -> StructuredTestCase:
        """Test case requiring complex financial risk analysis across multiple asset classes."""
        return StructuredTestCase(
            name="financial_risk_assessment",
            description="Multi-dimensional portfolio risk assessment with correlation analysis and regulatory constraints",
            data={
                "portfolio": {
                    "total_value": 50000000,
                    "target_risk": "moderate",
                    "asset_classes": {
                        "equities": {
                            "allocation": 0.6,
                            "positions": [
                                {
                                    "symbol": "TECH_GROWTH",
                                    "value": 15000000,
                                    "beta": 1.3,
                                    "volatility": 0.25,
                                    "sector": "technology",
                                    "correlation_matrix": {
                                        "FINANCIAL": 0.4,
                                        "ENERGY": -0.1,
                                    },
                                },
                                {
                                    "symbol": "FINANCIAL",
                                    "value": 10000000,
                                    "beta": 1.1,
                                    "volatility": 0.18,
                                    "sector": "financial",
                                    "correlation_matrix": {
                                        "TECH_GROWTH": 0.4,
                                        "ENERGY": 0.2,
                                    },
                                },
                                {
                                    "symbol": "ENERGY",
                                    "value": 5000000,
                                    "beta": 0.8,
                                    "volatility": 0.35,
                                    "sector": "energy",
                                    "correlation_matrix": {
                                        "TECH_GROWTH": -0.1,
                                        "FINANCIAL": 0.2,
                                    },
                                },
                            ],
                        },
                        "bonds": {
                            "allocation": 0.3,
                            "duration": 5.2,
                            "credit_rating": "AA",
                            "yield": 0.045,
                        },
                        "alternatives": {
                            "allocation": 0.1,
                            "liquidity_horizon": "90_days",
                            "risk_rating": "high",
                        },
                    },
                },
                "constraints": {
                    "regulatory": {
                        "single_position_limit": 0.05,
                        "sector_concentration_limit": 0.25,
                        "liquidity_requirement": 0.15,
                    },
                    "risk_limits": {
                        "max_portfolio_beta": 1.2,
                        "var_95_limit": 0.02,
                        "max_drawdown": 0.15,
                    },
                },
                "market_conditions": {
                    "volatility_regime": "elevated",
                    "interest_rate_environment": "rising",
                    "economic_indicators": {
                        "gdp_growth": 0.023,
                        "inflation": 0.031,
                        "unemployment": 0.042,
                    },
                },
            },
            task="Analyze the portfolio's risk profile, identify concentration risks, assess regulatory compliance, and recommend specific rebalancing actions given current market conditions.",
            why_structure_helps="Complex interdependencies between asset correlations, regulatory constraints, and risk metrics require hierarchical organization to track relationships",
            category="structured_advantage",
            expected_advantages=[
                "Calculate portfolio-level risk metrics using correlation data",
                "Identify specific regulatory violations with precise limits",
                "Cross-reference market conditions with asset characteristics",
                "Provide quantitative rebalancing recommendations",
            ],
        )

    @classmethod
    def medical_treatment_protocol(cls) -> StructuredTestCase:
        """Test case requiring analysis of complex medical protocols with contraindications and interactions."""
        return StructuredTestCase(
            name="medical_treatment_protocol",
            description="Multi-condition patient with complex medication interactions and treatment protocol decisions",
            data={
                "patient": {
                    "demographics": {
                        "age": 67,
                        "weight": 78.5,
                        "height": 175,
                        "gender": "female",
                    },
                    "medical_history": {
                        "primary_conditions": [
                            {
                                "condition": "type_2_diabetes",
                                "diagnosed": "2018-03-15",
                                "severity": "moderate",
                                "hba1c": 7.8,
                                "complications": ["neuropathy", "retinopathy"],
                            },
                            {
                                "condition": "hypertension",
                                "diagnosed": "2015-07-22",
                                "severity": "stage_2",
                                "systolic": 165,
                                "diastolic": 95,
                            },
                            {
                                "condition": "chronic_kidney_disease",
                                "diagnosed": "2020-11-10",
                                "stage": 3,
                                "gfr": 45,
                                "creatinine": 1.8,
                            },
                        ],
                        "allergies": ["sulfa_drugs", "penicillin"],
                        "current_medications": [
                            {
                                "name": "metformin",
                                "dose": "1000mg",
                                "frequency": "twice_daily",
                                "interactions": ["contrast_dye", "alcohol"],
                            },
                            {
                                "name": "lisinopril",
                                "dose": "20mg",
                                "frequency": "daily",
                                "contraindications": ["pregnancy", "hyperkalemia"],
                            },
                        ],
                    },
                },
                "treatment_protocols": {
                    "diabetes_management": {
                        "target_hba1c": 7.0,
                        "medication_options": {
                            "first_line": [
                                {
                                    "name": "insulin_glargine",
                                    "dosing": "weight_based",
                                    "kidney_adjustment": "required_if_gfr_below_30",
                                    "monitoring": ["glucose", "hba1c", "hypoglycemia"],
                                }
                            ],
                            "add_on_therapy": [
                                {
                                    "name": "empagliflozin",
                                    "contraindications": [
                                        "gfr_below_30",
                                        "ketoacidosis_risk",
                                    ],
                                    "benefits": ["cardiovascular", "renal_protection"],
                                    "side_effects": ["uti", "dehydration"],
                                }
                            ],
                        },
                    },
                    "hypertension_management": {
                        "target_bp": "130/80",
                        "medication_adjustments": {
                            "ace_inhibitor": {
                                "current": "lisinopril_20mg",
                                "max_dose": "40mg",
                                "kidney_monitoring": "required",
                            },
                            "combination_therapy": {
                                "options": [
                                    "calcium_channel_blocker",
                                    "thiazide_diuretic",
                                ],
                                "kidney_considerations": "avoid_thiazide_if_gfr_below_30",
                            },
                        },
                    },
                },
                "lab_values": {
                    "recent": {
                        "date": "2024-01-15",
                        "potassium": 4.8,
                        "sodium": 142,
                        "bun": 35,
                        "creatinine": 1.8,
                        "gfr": 45,
                    }
                },
            },
            task="Develop a comprehensive treatment plan that optimizes diabetes and hypertension management while considering kidney function, drug interactions, and patient safety constraints.",
            why_structure_helps="Complex medical decision-making requires tracking multiple interconnected factors: conditions, contraindications, dosing adjustments, and monitoring parameters",
            category="structured_advantage",
            expected_advantages=[
                "Identify specific contraindications based on patient conditions",
                "Apply kidney function adjustments to medication dosing",
                "Cross-reference drug interactions and allergies",
                "Develop monitoring plan based on medication choices",
            ],
        )

    @classmethod
    def security_access_control(cls) -> StructuredTestCase:
        """Test case requiring analysis of complex role-based access control with inheritance and temporal constraints."""
        return StructuredTestCase(
            name="security_access_control",
            description="Enterprise security audit requiring analysis of role hierarchies, permission inheritance, and temporal access patterns",
            data={
                "organization": {
                    "security_model": "rbac_with_attributes",
                    "compliance_requirements": ["sox", "pci_dss", "gdpr"],
                    "roles": {
                        "executive": {
                            "level": 1,
                            "inherits_from": [],
                            "permissions": [
                                {
                                    "resource": "financial_reports",
                                    "actions": ["read", "export"],
                                    "conditions": {
                                        "time_restriction": "business_hours",
                                        "location": "corporate_network",
                                        "mfa_required": True,
                                    },
                                },
                                {
                                    "resource": "employee_data",
                                    "actions": ["read"],
                                    "conditions": {
                                        "approval_required": "hr_director",
                                        "audit_logged": True,
                                    },
                                },
                            ],
                        },
                        "finance_manager": {
                            "level": 2,
                            "inherits_from": ["employee"],
                            "permissions": [
                                {
                                    "resource": "financial_reports",
                                    "actions": ["read", "modify", "approve"],
                                    "conditions": {
                                        "department_scope": "finance",
                                        "approval_chain": ["cfo"],
                                        "data_classification": "confidential",
                                    },
                                },
                                {
                                    "resource": "budget_data",
                                    "actions": ["read", "modify"],
                                    "conditions": {
                                        "fiscal_year": "current_and_next",
                                        "segregation_duties": "no_self_approval",
                                    },
                                },
                            ],
                        },
                        "employee": {
                            "level": 3,
                            "inherits_from": [],
                            "permissions": [
                                {
                                    "resource": "timesheet",
                                    "actions": ["read", "modify"],
                                    "conditions": {
                                        "scope": "self_only",
                                        "time_restriction": "submission_period",
                                    },
                                }
                            ],
                        },
                    },
                    "users": [
                        {
                            "id": "alice_johnson",
                            "roles": ["finance_manager"],
                            "attributes": {
                                "department": "finance",
                                "clearance_level": "confidential",
                                "employment_type": "full_time",
                                "manager": "bob_wilson",
                            },
                            "access_history": {
                                "last_login": "2024-01-20T09:15:00Z",
                                "failed_attempts": 0,
                                "unusual_activity": False,
                            },
                        },
                        {
                            "id": "charlie_davis",
                            "roles": ["employee", "temp_auditor"],
                            "attributes": {
                                "department": "finance",
                                "clearance_level": "restricted",
                                "employment_type": "contractor",
                                "contract_end": "2024-06-30",
                            },
                            "access_history": {
                                "last_login": "2024-01-19T14:30:00Z",
                                "failed_attempts": 2,
                                "unusual_activity": True,
                            },
                        },
                    ],
                },
                "access_request": {
                    "user": "charlie_davis",
                    "resource": "financial_reports",
                    "action": "export",
                    "justification": "quarterly_audit_requirement",
                    "requested_time": "2024-01-21T10:00:00Z",
                    "request_context": {
                        "location": "remote_vpn",
                        "device": "personal_laptop",
                        "audit_firm": "external_auditors_llc",
                    },
                },
                "security_policies": {
                    "data_loss_prevention": {
                        "export_restrictions": {
                            "financial_data": "executive_approval_required",
                            "customer_data": "gdpr_compliance_check",
                        }
                    },
                    "temporal_restrictions": {
                        "contractor_access": "business_hours_only",
                        "executive_actions": "mfa_required_after_hours",
                    },
                },
            },
            task="Evaluate the access request, determine if it should be approved based on role permissions, policy constraints, and risk factors. Provide specific approval/denial reasoning and required additional controls.",
            why_structure_helps="Complex permission inheritance, conditional access rules, and temporal constraints require hierarchical organization to properly evaluate access decisions",
            category="structured_advantage",
            expected_advantages=[
                "Trace permission inheritance through role hierarchy",
                "Apply conditional access rules based on user attributes",
                "Evaluate temporal and location-based constraints",
                "Identify policy violations and required approvals",
            ],
        )

    @classmethod
    def supply_chain_optimization(cls) -> StructuredTestCase:
        """Test case requiring optimization of complex supply chain with multiple constraints and dependencies."""
        return StructuredTestCase(
            name="supply_chain_optimization",
            description="Multi-tier supply chain optimization with capacity constraints, demand forecasting, and disruption scenarios",
            data={
                "supply_network": {
                    "suppliers": {
                        "tier_1": [
                            {
                                "id": "supplier_a",
                                "location": "china",
                                "capacity": 10000,
                                "lead_time": 21,
                                "reliability": 0.95,
                                "cost_per_unit": 12.50,
                                "minimum_order": 500,
                                "quality_rating": 4.2,
                                "certifications": ["iso9001", "iso14001"],
                                "risk_factors": {
                                    "geopolitical": "medium",
                                    "weather": "high",
                                    "financial_stability": "high",
                                },
                            }
                        ]
                    },
                    "manufacturing": {
                        "facilities": [
                            {
                                "location": "usa_midwest",
                                "capacity": 15000,
                                "efficiency": 0.87,
                                "labor_cost": 25.00,
                                "automation_level": 0.6,
                                "environmental_impact": "medium",
                            }
                        ]
                    },
                },
                "demand_forecast": {
                    "regions": {
                        "midwest": {
                            "q1_demand": 8000,
                            "q2_demand": 12000,
                            "seasonal_factor": 1.2,
                            "growth_rate": 0.05,
                        }
                    }
                },
            },
            task="Optimize the supply chain configuration to minimize total cost while meeting demand forecasts and resilience requirements.",
            why_structure_helps="Multi-level supply chain optimization requires understanding complex interdependencies between suppliers, manufacturing, and demand across multiple constraints",
            category="structured_advantage",
            expected_advantages=[
                "Calculate end-to-end cost optimization across tiers",
                "Apply multiple constraint satisfaction simultaneously",
                "Analyze disruption impact through dependency chains",
                "Balance trade-offs between cost, risk, and sustainability",
            ],
        )

    @classmethod
    def scientific_experiment_design(cls) -> StructuredTestCase:
        """Test case requiring design of complex scientific experiments with multiple variables and controls."""
        return StructuredTestCase(
            name="scientific_experiment_design",
            description="Multi-factorial experimental design with nested variables, statistical power requirements, and ethical constraints",
            data={
                "research_objective": {
                    "hypothesis": "Novel drug compound X reduces inflammatory markers more effectively than standard treatment",
                    "primary_endpoints": [
                        {
                            "measure": "il6_reduction",
                            "target_effect_size": 0.5,
                            "measurement_timepoints": [
                                "baseline",
                                "week_2",
                                "week_4",
                                "week_8",
                            ],
                            "clinical_significance": 0.3,
                        }
                    ],
                },
                "experimental_design": {
                    "study_type": "randomized_controlled_trial",
                    "blinding": "double_blind",
                    "treatment_arms": [
                        {
                            "name": "experimental",
                            "intervention": "compound_x",
                            "dosage": "150mg_daily",
                            "duration": "8_weeks",
                            "sample_size_target": 120,
                        }
                    ],
                },
            },
            task="Design the optimal clinical trial protocol that maximizes statistical power while meeting regulatory requirements and ensuring patient safety.",
            why_structure_helps="Complex experimental design requires coordinating multiple interdependent factors: statistical power, regulatory compliance, operational constraints, and safety considerations",
            category="structured_advantage",
            expected_advantages=[
                "Calculate sample sizes across stratification factors",
                "Apply inclusion/exclusion criteria systematically",
                "Balance statistical requirements with operational constraints",
                "Identify regulatory compliance requirements and timelines",
            ],
        )

    @classmethod
    def legal_compliance_analysis(cls) -> StructuredTestCase:
        """Test case requiring analysis of complex regulatory compliance across multiple jurisdictions."""
        return StructuredTestCase(
            name="legal_compliance_analysis",
            description="Multi-jurisdictional compliance assessment for cross-border data processing with conflicting regulatory requirements",
            data={
                "business_operation": {
                    "company": "global_fintech_inc",
                    "business_model": "cross_border_payments",
                    "data_processing": {
                        "personal_data_types": [
                            {
                                "category": "identity_data",
                                "fields": ["name", "address", "id_number"],
                                "sensitivity": "high",
                                "retention_period": "7_years",
                            }
                        ]
                    },
                },
                "jurisdictions": {
                    "european_union": {
                        "applicable_regulations": [
                            {
                                "name": "gdpr",
                                "requirements": {
                                    "lawful_basis": [
                                        "consent",
                                        "legitimate_interest",
                                        "contract",
                                    ],
                                    "data_subject_rights": [
                                        "access",
                                        "rectification",
                                        "erasure",
                                        "portability",
                                    ],
                                },
                            }
                        ]
                    }
                },
            },
            task="Develop a comprehensive compliance strategy that addresses all jurisdictional requirements while balancing business needs.",
            why_structure_helps="Multi-jurisdictional compliance requires understanding complex interactions between different regulatory frameworks, data types, and business requirements",
            category="structured_advantage",
            expected_advantages=[
                "Map specific data types to applicable regulations",
                "Identify conflicts between jurisdictional requirements",
                "Prioritize compliance gaps by risk and penalty exposure",
                "Design unified compliance strategy across jurisdictions",
            ],
        )

    @classmethod
    def infrastructure_capacity_planning(cls) -> StructuredTestCase:
        """Test case requiring analysis of complex infrastructure scaling with performance and cost optimization."""
        return StructuredTestCase(
            name="infrastructure_capacity_planning",
            description="Multi-tier infrastructure capacity planning with performance requirements, cost constraints, and fault tolerance",
            data={
                "current_infrastructure": {
                    "web_tier": {
                        "instances": [
                            {
                                "type": "c5.2xlarge",
                                "count": 8,
                                "cpu_utilization": 0.65,
                                "memory_utilization": 0.58,
                                "cost_per_hour": 0.34,
                            }
                        ]
                    },
                    "database_tier": {
                        "primary": {
                            "type": "r5.4xlarge",
                            "engine": "postgresql_13",
                            "cpu_utilization": 0.45,
                            "memory_utilization": 0.68,
                            "connection_count": 450,
                            "max_connections": 800,
                        }
                    },
                },
                "performance_requirements": {
                    "response_time": {"p95_target": "200ms", "current_p95": "180ms"},
                    "throughput": {"current_rps": 5000, "projected_growth": 0.15},
                },
            },
            task="Design an optimal infrastructure scaling plan that meets projected growth while staying within budget constraints and maintaining performance SLAs.",
            why_structure_helps="Infrastructure capacity planning requires analyzing complex interdependencies between performance, cost, growth projections, and operational constraints across multiple tiers",
            category="structured_advantage",
            expected_advantages=[
                "Model capacity requirements across interdependent tiers",
                "Optimize instance types and sizing based on utilization patterns",
                "Calculate cost implications of scaling scenarios",
                "Design fault-tolerant architecture meeting SLA requirements",
            ],
        )

    @classmethod
    def educational_curriculum_mapping(cls) -> StructuredTestCase:
        """Test case requiring design of educational pathways with prerequisites and learning objectives."""
        return StructuredTestCase(
            name="educational_curriculum_mapping",
            description="Comprehensive curriculum design with prerequisite chains, competency mapping, and personalized learning paths",
            data={
                "program_structure": {
                    "degree": "master_of_data_science",
                    "duration": "24_months",
                    "total_credits": 48,
                    "learning_outcomes": [
                        {
                            "id": "statistical_analysis",
                            "description": "Apply statistical methods to analyze complex datasets",
                            "bloom_level": "application",
                        }
                    ],
                },
                "course_catalog": {
                    "foundation_courses": [
                        {
                            "code": "DS501",
                            "title": "Statistics for Data Science",
                            "credits": 3,
                            "prerequisites": ["undergraduate_statistics"],
                            "learning_objectives": [
                                {
                                    "objective": "hypothesis_testing",
                                    "bloom_level": "application",
                                    "contributing_outcomes": ["statistical_analysis"],
                                }
                            ],
                        }
                    ]
                },
            },
            task="Design personalized degree plans that optimize learning progression, respect prerequisites, meet scheduling constraints, and align with career goals.",
            why_structure_helps="Educational pathway planning requires tracking complex prerequisite chains, competency development, and scheduling constraints across multiple interconnected courses",
            category="structured_advantage",
            expected_advantages=[
                "Trace prerequisite chains to ensure proper course sequencing",
                "Map learning objectives to program outcomes systematically",
                "Optimize course scheduling based on availability and constraints",
                "Personalize pathways based on student background and goals",
            ],
        )

    @classmethod
    def investment_portfolio_analysis(cls) -> StructuredTestCase:
        """Test case requiring comprehensive portfolio analysis with risk metrics and optimization recommendations."""
        return StructuredTestCase(
            name="investment_portfolio_analysis",
            description="Multi-asset portfolio analysis with risk-return optimization, regulatory constraints, and market scenario modeling",
            data={
                "portfolio": {
                    "total_assets": 100000000,
                    "client_profile": {
                        "risk_tolerance": "moderate_aggressive",
                        "investment_horizon": "10_years",
                    },
                    "current_allocation": {
                        "equity": {
                            "allocation": 0.65,
                            "holdings": [
                                {
                                    "asset": "us_large_cap",
                                    "weight": 0.35,
                                    "expected_return": 0.08,
                                    "volatility": 0.15,
                                    "beta": 1.0,
                                }
                            ],
                        }
                    },
                },
                "correlation_matrix": {
                    "us_large_cap": {
                        "international_developed": 0.7,
                        "us_treasury_bonds": -0.2,
                    }
                },
            },
            task="Analyze the current portfolio's risk-return profile, identify optimization opportunities within constraints, and recommend specific allocation changes.",
            why_structure_helps="Portfolio optimization requires analyzing complex relationships between asset correlations, risk metrics, regulatory constraints, and scenario modeling across multiple asset classes",
            category="structured_advantage",
            expected_advantages=[
                "Calculate portfolio-level risk metrics using correlation matrices",
                "Apply multiple constraint types simultaneously in optimization",
                "Model performance across different market scenarios",
                "Balance risk-return trade-offs with regulatory requirements",
            ],
        )

    @classmethod
    def regulatory_policy_interpretation(cls) -> StructuredTestCase:
        """Test case requiring interpretation of complex regulatory frameworks with precedent analysis and compliance recommendations."""
        return StructuredTestCase(
            name="regulatory_policy_interpretation",
            description="Complex regulatory interpretation for environmental compliance with overlapping federal, state, and local requirements",
            data={
                "regulatory_framework": {
                    "federal_regulations": {
                        "clean_air_act": {
                            "relevant_sections": [
                                {
                                    "section": "112",
                                    "title": "hazardous_air_pollutants",
                                    "requirements": {
                                        "mact_standards": "maximum_achievable_control_technology",
                                        "monitoring": "continuous_emission_monitoring",
                                    },
                                }
                            ]
                        }
                    }
                },
                "facility_characteristics": {
                    "location": {
                        "state": "california",
                        "air_district": "south_coast_aqmd",
                    },
                    "operations": {
                        "facility_type": "chemical_manufacturing",
                        "processes": [
                            {
                                "process_name": "solvent_recovery",
                                "emissions": {
                                    "toluene": {
                                        "annual_emissions": 12.5,
                                        "units": "tons_per_year",
                                        "hap_status": True,
                                    }
                                },
                            }
                        ],
                    },
                },
            },
            task="Analyze the regulatory requirements for proposed facility modifications, determine permit requirements across all jurisdictions, and recommend a comprehensive permitting strategy.",
            why_structure_helps="Complex regulatory analysis requires understanding interactions between multiple regulatory frameworks, precedent analysis, and facility-specific compliance requirements",
            category="structured_advantage",
            expected_advantages=[
                "Map facility characteristics to applicable regulatory requirements",
                "Identify conflicts or overlaps between different jurisdictional requirements",
                "Apply precedent analysis to predict regulatory outcomes",
                "Develop comprehensive compliance strategy across all regulatory levels",
            ],
        )

    # ========== NEUTRAL TEST CASES ==========
    # Simple factual questions where structure provides no clear advantage

    @classmethod
    def basic_factual_question(cls) -> StructuredTestCase:
        """Simple factual question where structure doesn't help."""
        return StructuredTestCase(
            name="basic_factual_question",
            description="Simple factual question about historical events",
            data={
                "question": "When did World War II end?",
                "context": {
                    "subject": "history",
                    "difficulty": "basic",
                    "type": "factual",
                },
            },
            task="Answer the factual question accurately and concisely.",
            category="neutral",
            why_structure_helps="Structure provides no advantage for simple factual recall - both formats contain identical information",
            expected_advantages=[
                "No expected advantages - this tests baseline performance",
                "Structure should not improve accuracy for simple facts",
                "Both formats should perform equally well",
            ],
        )

    @classmethod
    def simple_calculation(cls) -> StructuredTestCase:
        """Basic math problem where structure is irrelevant."""
        return StructuredTestCase(
            name="simple_calculation",
            description="Straightforward mathematical calculation",
            data={
                "numbers": [15, 23, 8, 42],
                "operation": "addition",
                "context": "Calculate the sum",
            },
            task="Calculate the sum of the given numbers: 15 + 23 + 8 + 42",
            category="computational",
            why_structure_helps="Mathematical calculations don't benefit from structural formatting - the computation is the same regardless",
            expected_advantages=[
                "No structural advantage expected",
                "Both formats should yield identical results",
                "Computation accuracy should be format-independent",
            ],
        )

    @classmethod
    def weather_report(cls) -> StructuredTestCase:
        """Simple weather information interpretation."""
        return StructuredTestCase(
            name="weather_report",
            description="Basic weather data interpretation",
            data={
                "temperature": "72°F",
                "humidity": "65%",
                "wind": "8 mph NW",
                "conditions": "partly cloudy",
            },
            task="Describe today's weather conditions in a single sentence.",
            category="neutral",
            why_structure_helps="Simple weather data is equally accessible in both formats - no complex relationships to parse",
            expected_advantages=[
                "No structural advantage for simple data interpretation",
                "Both formats contain the same information clearly",
                "Response quality should be equivalent",
            ],
        )

    # ========== CREATIVE TEST CASES ==========
    # Tasks where structure might actually hinder natural flow

    @classmethod
    def creative_story_writing(cls) -> StructuredTestCase:
        """Creative writing task where structure might constrain creativity."""
        return StructuredTestCase(
            name="creative_story_writing",
            description="Creative writing with character and setting prompts",
            data={
                "character": {
                    "name": "Elena",
                    "age": 28,
                    "occupation": "marine biologist",
                },
                "setting": {
                    "location": "remote island research station",
                    "time": "during a storm",
                    "mood": "mysterious",
                },
                "genre": "thriller",
            },
            task="Write a compelling 200-word story opening featuring Elena at the research station during the storm.",
            category="creative",
            why_structure_helps="Structure may actually constrain creative flow by breaking narrative elements into rigid categories",
            expected_advantages=[
                "Raw text may flow more naturally for creative writing",
                "Structured format might feel restrictive for storytelling",
                "Creative tasks often benefit from organic information presentation",
            ],
        )

    @classmethod
    def poem_composition(cls) -> StructuredTestCase:
        """Poetry writing where structure might interfere with artistic flow."""
        return StructuredTestCase(
            name="poem_composition",
            description="Write a poem based on given themes and constraints",
            data={
                "theme": "autumn leaves",
                "style": "free verse",
                "mood": "contemplative",
                "length": "8-12 lines",
                "imagery": ["golden", "falling", "whisper"],
            },
            task="Compose a contemplative free verse poem about autumn leaves using the suggested imagery.",
            category="creative",
            why_structure_helps="Poetic composition benefits from natural language flow rather than structured data presentation",
            expected_advantages=[
                "Raw text may inspire more natural creative expression",
                "Structured format may feel mechanical for artistic tasks",
                "Poetry often emerges from organic word associations",
            ],
        )

    # ========== ADVERSARIAL TEST CASES ==========
    # Cases designed to favor unstructured approaches

    @classmethod
    def conversational_advice(cls) -> StructuredTestCase:
        """Personal advice scenario where natural conversation style matters."""
        return StructuredTestCase(
            name="conversational_advice",
            description="Provide empathetic advice for a personal situation",
            data={
                "situation": "I'm feeling overwhelmed balancing work and personal life",
                "context": {
                    "person": "working professional",
                    "age_range": "late 20s",
                    "specific_concerns": [
                        "long work hours",
                        "neglecting relationships",
                        "stress",
                    ],
                },
                "tone_desired": "supportive and understanding",
            },
            task="Provide compassionate, practical advice for managing work-life balance and stress.",
            category="adversarial",
            why_structure_helps="Conversational advice benefits from natural, flowing language rather than structured presentation - empathy requires organic expression",
            expected_advantages=[
                "Raw text may sound more natural and empathetic",
                "Structured format may feel clinical for personal advice",
                "Human connection often requires informal, flowing communication",
            ],
        )

    @classmethod
    def stream_of_consciousness(cls) -> StructuredTestCase:
        """Task requiring natural thought flow."""
        return StructuredTestCase(
            name="stream_of_consciousness",
            description="Express thoughts and feelings about a memory",
            data={
                "memory_trigger": "the smell of fresh bread",
                "associations": [
                    "childhood",
                    "grandmother's kitchen",
                    "warmth",
                    "comfort",
                ],
                "emotion": "nostalgia",
                "style": "stream of consciousness",
            },
            task="Write a stream-of-consciousness reflection triggered by the smell of fresh bread, incorporating childhood memories.",
            category="adversarial",
            why_structure_helps="Stream of consciousness requires natural thought flow that structured formatting artificially fragments",
            expected_advantages=[
                "Raw text allows for natural thought progression",
                "Structured format disrupts the organic flow of consciousness",
                "Authentic emotional expression benefits from unstructured presentation",
            ],
        )
