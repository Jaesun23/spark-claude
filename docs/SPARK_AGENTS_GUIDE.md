# 🎯 SPARK v3.5 Agents Implementation Guide

> **Complete guide for optimal agent information provision and context management**
> 
> *Last updated: August 10, 2025*
> *Version: SPARK v3.5 - Advanced Multi-Agent System*

This guide details exactly what information each SPARK agent needs to deliver optimal results. Every detail is crucial for Hook automation and seamless agent operation.

---

## 🔍 **analyzer-spark** - Multi-Dimensional System Analysis

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "analysis_target": {
    "scope": "file_path | directory_path | entire_system",
    "focus_areas": ["quality", "security", "performance", "architecture", "dependencies"],
    "depth": "quick | standard | deep",
    "exclusions": ["test_files", "node_modules", "vendor", "build_output"]
  },
  "project_context": {
    "framework": "detected_or_specified_framework",
    "language": "primary_programming_language",
    "project_type": "web_app | api | library | microservice | monolith",
    "team_size": "number_of_developers",
    "environment": "development | staging | production"
  },
  "complexity_hints": {
    "file_count": "actual_number",
    "integration_points": "number_of_external_services",
    "known_issues": ["performance_bottlenecks", "security_concerns", "technical_debt"]
  }
}
```

#### ⚙️ **Configuration Parameters**
- **Wave Mode Trigger**: Complexity ≥0.7 (auto-calculated or manually set)
- **Evidence Collection Depth**: 
  - Quick: 5-10 files, 30 patterns
  - Standard: 20-50 files, 100 patterns  
  - Deep: All files, 500+ patterns
- **Analysis Dimensions**: Specify which to prioritize
  - Architecture Analysis: Layer violations, coupling metrics
  - Performance Analysis: O(n²) algorithms, N+1 queries, resource usage
  - Security Analysis: OWASP top 10, auth flows, data exposure
  - Quality Analysis: Code smells, duplication, complexity metrics

#### 🔧 **Automation Information**
- **Recent Changes**: Git commits from last 7/30 days
- **Known Problem Areas**: Files/modules with frequent bugs
- **Performance Baselines**: Current response times, resource usage
- **Business Critical Paths**: User journeys that must never break
- **Compliance Requirements**: GDPR, PCI, HIPAA, SOX requirements

#### 📊 **Expected Deliverables Specification**
```yaml
report_format:
  executive_summary: "3-5 critical findings with business impact"
  complexity_score: "0.0-1.0 with justification"
  priority_matrix: "P0 (Critical) to P3 (Low) with effort estimates"
  heatmap: "Visual complexity representation"
  metrics_dashboard: "Performance/Security/Quality scores out of 100"
  improvement_roadmap: "Week 1, Month 1, Quarter phased approach"
```

---

## 🎨 **designer-spark** - Comprehensive System Design

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "design_target": {
    "type": "architecture | api | component | database | ui_system",
    "scope": "new_system | enhancement | migration | integration",
    "stakeholders": ["end_users", "developers", "administrators", "business"],
    "timeline": "prototype | mvp | full_production | enterprise_scale"
  },
  "requirements": {
    "functional": ["user_authentication", "data_processing", "reporting"],
    "non_functional": {
      "performance": "response_times | throughput | scalability",
      "security": "authentication | authorization | encryption | compliance",
      "usability": "accessibility_level | user_experience_goals",
      "reliability": "uptime_requirements | disaster_recovery"
    }
  },
  "constraints": {
    "technical": ["existing_systems", "technology_stack", "infrastructure"],
    "business": ["budget", "timeline", "team_skills", "maintenance_capacity"],
    "regulatory": ["compliance_requirements", "data_governance", "audit_needs"]
  }
}
```

#### ⚙️ **Configuration Parameters**
- **Complexity Calculation**: 
  - UI complexity (0.2 weight): Simple forms vs Complex dashboards
  - Architecture complexity (0.3 weight): Monolith vs Microservices
  - Performance requirements (0.2 weight): <100ms vs <1s response
  - Security requirements (0.2 weight): Basic auth vs Zero trust
  - User scale (0.1 weight): <100 vs >1M users
- **Wave Mode Trigger**: Complexity ≥0.7
- **Persona Activation**: Auto-select based on design type
  - Frontend: UI/UX system design
  - Backend: API and data architecture
  - Security: Threat modeling required
  - Architect: System-wide design decisions

#### 🔧 **Integration Requirements**
```yaml
existing_systems:
  - name: "system_name"
    version: "version_number"
    api_endpoints: ["list_of_endpoints"]
    data_formats: ["json", "xml", "csv"]
    authentication: "oauth2 | jwt | basic | none"
    
technology_preferences:
  backend: ["preferred_languages", "frameworks", "databases"]
  frontend: ["preferred_frameworks", "ui_libraries", "build_tools"]
  infrastructure: ["cloud_provider", "container_platform", "deployment_method"]
```

#### 📊 **Expected Deliverables Specification**
```yaml
design_outputs:
  executive_summary: "High-level design overview and key decisions"
  c4_diagrams: "Context, Container, Component, Code level diagrams"
  api_specifications: "Complete OpenAPI/GraphQL schemas with examples"
  data_models: "ERD with relationships, constraints, and indexes"
  ui_guidelines: "Component library, design tokens, style guide"
  adrs: "Architecture Decision Records with alternatives considered"
  implementation_roadmap: "Phased delivery with milestones and dependencies"
  migration_strategy: "Step-by-step upgrade from current state"
```

---

## ⚡ **implementer-spark** - Systematic Feature Implementation

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "implementation_target": {
    "feature_description": "detailed_requirements_and_acceptance_criteria",
    "file_locations": ["existing_files_to_modify", "new_files_to_create"],
    "integration_points": ["apis_to_call", "databases_to_modify", "services_to_connect"],
    "ui_requirements": "components_needed | screens_to_build | user_flows"
  },
  "quality_standards": {
    "test_coverage": {"unit": 95, "integration": 85, "e2e": "critical_paths"},
    "performance": {"api_response": "<200ms", "ui_load": "<3s", "database_query": "<100ms"},
    "security": ["input_validation", "output_sanitization", "auth_requirements"],
    "code_standards": ["naming_conventions", "documentation_level", "error_handling"]
  },
  "technical_context": {
    "existing_patterns": "architecture_patterns_already_used",
    "code_style": "linting_rules | formatting_standards | type_requirements",
    "dependencies": "allowed_libraries | version_constraints | license_restrictions"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **Complexity Auto-Calculation**:
  - API endpoints: +0.2 per endpoint
  - Database operations: +0.15 per table/collection
  - Authentication/Authorization: +0.25
  - UI components: +0.1 per component
  - External integrations: +0.2 per service
  - Real-time features: +0.3
- **Wave Mode Trigger**: Complexity ≥0.7
- **Persona Auto-Activation**:
  - Backend: API, database, server logic detected
  - Frontend: UI, components, user interaction detected
  - Security: Auth, encryption, validation required
  - Architect: System design, scalability concerns

#### 🔧 **Environment Information**
```yaml
development_setup:
  local_environment: "setup_commands_and_requirements"
  test_databases: "connection_strings_and_seed_data"
  api_keys: "development_keys_and_service_accounts"
  feature_flags: "toggles_needed_for_development"
  
deployment_context:
  environments: ["dev", "staging", "prod"]
  deployment_method: "ci_cd_pipeline | manual | automated"
  rollback_strategy: "blue_green | canary | immediate"
  monitoring: "metrics_to_track | alerts_to_configure"
```

#### 📊 **Expected Deliverables Specification**
```yaml
implementation_outputs:
  source_code: "Fully functional, tested code meeting all requirements"
  test_suite: "Unit tests (95%+), Integration tests (85%+), E2E critical paths"
  api_documentation: "OpenAPI specs, endpoint examples, error codes"
  database_migrations: "Schema changes, data migrations, rollback scripts"
  deployment_scripts: "CI/CD updates, environment configurations"
  performance_metrics: "Benchmark results, load test outcomes"
  security_validation: "Vulnerability scan results, penetration test summary"
  user_documentation: "Feature guides, troubleshooting, FAQs"
```

---

## ✅ **tester-spark** - Comprehensive Testing Excellence

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "testing_scope": {
    "implementation_context": "what_was_built_or_changed",
    "critical_paths": ["user_registration", "payment_processing", "data_export"],
    "risk_areas": ["authentication", "data_integrity", "performance_bottlenecks"],
    "test_types_needed": ["unit", "integration", "e2e", "performance", "security", "regression"]
  },
  "coverage_targets": {
    "unit": 95,
    "integration": 85,
    "overall": 90,
    "critical_path_e2e": 100,
    "regression": "all_existing_features"
  },
  "test_environment": {
    "frameworks": "existing_test_frameworks_in_project",
    "databases": "test_database_setup_and_seed_data",
    "external_services": "mocking_strategy_for_third_party_apis",
    "browsers": ["chrome", "firefox", "safari", "mobile_chrome"]
  }
}
```

#### ⚙️ **Configuration Parameters**
- **Test Pyramid Distribution**: Unit (70%) > Integration (20%) > E2E (10%)
- **Persona Activation**:
  - Primary QA: Always active for quality focus
  - Frontend: UI component and user interaction testing
  - Backend: API, service, and data layer testing
  - Security: Vulnerability testing, auth flow validation
  - Performance: Load testing, stress testing, scalability
- **MCP Server Usage**:
  - Playwright: E2E browser automation, cross-browser testing
  - Sequential: Systematic test planning and analysis
  - Context7: Testing patterns and best practices

#### 🔧 **Testing Specifications**
```yaml
test_categories:
  unit_tests:
    - individual_functions: "isolated_testing_with_mocks"
    - components: "react_component_testing_with_enzyme_or_testing_library"
    - services: "business_logic_testing_with_dependency_injection"
    - utilities: "helper_function_testing_with_edge_cases"
    
  integration_tests:
    - api_contracts: "endpoint_testing_with_real_database"
    - database_operations: "crud_testing_with_transactions"
    - service_communication: "microservice_interaction_testing"
    - external_integrations: "third_party_api_integration_testing"
    
  e2e_tests:
    - user_workflows: "complete_user_journey_testing"
    - cross_browser: "compatibility_testing_across_browsers"
    - mobile_responsive: "testing_on_different_device_sizes"
    - performance: "page_load_times_and_user_interaction_speed"
```

#### 📊 **Expected Deliverables Specification**
```yaml
testing_outputs:
  test_strategy_document: "Test pyramid, coverage targets, risk areas"
  test_implementation: "Complete test suites for all categories"
  test_execution_results: "Pass/fail status, coverage reports, performance metrics"
  ci_cd_integration: "Automated test execution, quality gates, failure notifications"
  performance_benchmarks: "Load test results, scalability limits, optimization recommendations"
  security_validation: "Vulnerability scan results, penetration test outcomes"
  regression_suite: "Automated tests preventing future feature breakage"
  test_documentation: "Test case descriptions, maintenance guides, troubleshooting"
```

---

## 📚 **documenter-spark** - Professional Documentation Creation

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "documentation_scope": {
    "target_audience": ["developers", "end_users", "administrators", "stakeholders"],
    "document_types": ["api_reference", "user_guides", "developer_tutorials", "architecture_docs"],
    "technical_depth": "beginner | intermediate | advanced | expert",
    "use_cases": ["onboarding", "troubleshooting", "integration", "maintenance"]
  },
  "content_source": {
    "code_locations": ["source_files_to_document", "api_endpoints", "configuration_files"],
    "existing_docs": ["current_documentation_to_update", "style_guides_to_follow"],
    "subject_matter_experts": "team_members_for_technical_review",
    "business_context": "feature_purpose_and_business_value"
  },
  "deliverable_format": {
    "output_format": "markdown | wiki | confluence | gitbook | docusaurus",
    "language": "en | es | fr | de | ja | zh | ko",
    "branding": "company_style_guide_and_formatting_requirements",
    "interactive_elements": ["code_examples", "tutorials", "faqs", "troubleshooting"]
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Documentation Process**:
  - Phase 1: Audience Analysis - Identify users and their needs
  - Phase 2: Structure Design - Information architecture and navigation
  - Phase 3: Content Creation - Write core documentation
  - Phase 4: Examples Addition - Code samples, use cases, scenarios
  - Phase 5: Review & Improvement - Validation and refinement
- **Persona Activation**:
  - Scribe: Professional writing and localization
  - Mentor: Educational approach and clarity
  - Frontend: UI/UX documentation expertise
  - Architect: System-level documentation

#### 🔧 **Content Requirements**
```yaml
documentation_elements:
  api_documentation:
    - endpoint_descriptions: "purpose, parameters, responses, errors"
    - authentication_guides: "how_to_obtain_and_use_api_keys"
    - code_examples: "curl, javascript, python, postman_collections"
    - rate_limiting: "request_limits_and_best_practices"
    - sdks_libraries: "available_client_libraries_and_wrappers"
    
  user_documentation:
    - getting_started: "account_setup, first_steps, quick_wins"
    - feature_guides: "step_by_step_instructions_with_screenshots"
    - troubleshooting: "common_issues_and_solutions"
    - faqs: "frequently_asked_questions_and_answers"
    - best_practices: "recommended_usage_patterns"
    
  developer_documentation:
    - architecture_overview: "system_design_and_component_relationships"
    - setup_guides: "local_development_environment_configuration"
    - contribution_guidelines: "code_style, pr_process, testing_requirements"
    - deployment_runbooks: "step_by_step_deployment_procedures"
    - maintenance_procedures: "routine_tasks_and_troubleshooting"
```

#### 📊 **Expected Deliverables Specification**
```yaml
documentation_outputs:
  structured_content: "Complete documentation sets organized by audience"
  code_examples: "Working examples with inline comments"
  visual_aids: "Mermaid diagrams, flowcharts, architecture diagrams"
  interactive_elements: "Tutorials, quizzes, hands_on_exercises"
  search_optimization: "Properly indexed content with metadata"
  maintenance_plan: "Update procedures, review schedules, ownership"
  quality_validation: "Accuracy checks, user feedback integration, analytics"
  multilingual_support: "Translation management if required"
```

---

## 🚨 **troubleshooter-spark** - Systematic Problem Resolution

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "problem_description": {
    "symptoms": "detailed_error_messages_and_observed_behavior",
    "affected_systems": ["frontend", "backend", "database", "infrastructure"],
    "impact_scope": "users_affected | services_down | data_integrity_concerns",
    "timeline": "when_started | frequency | patterns_observed",
    "recent_changes": "deployments | configuration_changes | dependency_updates"
  },
  "environment_details": {
    "production_environment": "server_specs | deployment_architecture | load_patterns",
    "monitoring_data": "metrics | logs | alerts | dashboard_links",
    "reproduction_steps": "how_to_replicate_the_issue",
    "attempted_solutions": "what_has_been_tried_already"
  },
  "business_impact": {
    "severity": "critical | high | medium | low",
    "affected_users": "number_and_types_of_users",
    "business_functions": "impacted_operations_and_workflows",
    "sla_violations": "uptime | response_time | availability_commitments"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Troubleshooting**: Symptom Analysis → Hypothesis Formation → Evidence Collection → Root Cause Verification → Solution Design
- **Complexity Assessment**:
  - Affected systems (>3 = +0.3)
  - Intermittent vs consistent (+0.2 for intermittent)
  - Production impact severity (+0.1 to +0.3)
  - Unknown root cause (+0.2)
  - Cross-service dependencies (+0.2)
- **Wave Mode**: Complexity ≥0.7 for comprehensive analysis
- **Persona Integration**: Analyzer + Performance + DevOps + Security as needed

#### 🔧 **Investigation Resources**
```yaml
diagnostic_information:
  log_locations: ["application_logs", "system_logs", "error_tracking_services"]
  metrics_sources: ["monitoring_dashboards", "performance_counters", "business_metrics"]
  test_environments: ["staging_reproduction", "load_testing_capabilities"]
  access_credentials: ["log_aggregation_systems", "monitoring_tools", "production_systems"]
  
investigation_tools:
  performance_profiling: ["apm_tools", "database_query_analyzers", "network_monitoring"]
  log_analysis: ["log_aggregation", "pattern_matching", "correlation_tools"]
  system_diagnostics: ["server_monitoring", "resource_utilization", "health_checks"]
  application_debugging: ["debuggers", "profilers", "trace_analyzers"]
```

#### 📊 **Expected Deliverables Specification**
```yaml
troubleshooting_outputs:
  executive_summary: "Problem, impact, root cause, recommended action"
  investigation_timeline: "Step_by_step_analysis_process_with_findings"
  root_cause_analysis: "Confirmed_cause_with_supporting_evidence"
  solution_options: "Immediate, short_term, long_term_fixes_with_risks"
  implementation_plan: "Detailed_steps_with_rollback_procedures"
  prevention_measures: "Monitoring, alerts, safeguards_to_prevent_recurrence"
  runbook_updates: "Documentation_updates_for_future_incidents"
  lessons_learned: "Process_improvements_and_knowledge_sharing"
```

---

## 🔧 **improver-spark** - Systematic Code Enhancement

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "improvement_target": {
    "scope": "specific_files | module | entire_system",
    "improvement_types": ["performance", "security", "code_quality", "architecture"],
    "constraints": ["backward_compatibility", "minimal_downtime", "no_breaking_changes"],
    "success_criteria": "measurable_goals_and_acceptance_criteria"
  },
  "current_state_analysis": {
    "known_issues": "technical_debt | performance_bottlenecks | security_vulnerabilities",
    "metrics_baseline": "current_performance | quality_scores | test_coverage",
    "user_complaints": "reported_issues | feedback | support_tickets",
    "business_impact": "cost_of_current_problems | opportunity_cost"
  },
  "improvement_goals": {
    "performance_targets": "response_times | throughput | resource_usage",
    "quality_metrics": "complexity_reduction | duplication_elimination | test_coverage",
    "security_objectives": "vulnerability_fixes | compliance_requirements",
    "maintainability": "code_readability | documentation | modularity"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Improvement**: Deep Analysis → Planning → Implementation → Integration → Validation
- **Wave Strategy** (complexity ≥0.7):
  - Wave 1: Critical fixes (security, crashes)
  - Wave 2: Performance optimizations  
  - Wave 3: Code quality improvements
  - Wave 4: Architecture enhancements
  - Wave 5: Documentation and testing
- **Persona Coordination**: Refactorer + Performance + Security + Architect
- **Quality Targets**:
  - Complexity: <10 per function
  - Duplication: <3%
  - Test coverage: >95% unit, >85% integration
  - Performance: 30-50% improvement
  - Security: 0 high/critical vulnerabilities

#### 🔧 **Improvement Context**
```yaml
technical_context:
  refactoring_opportunities: "design_patterns_to_apply | solid_principles_violations"
  performance_bottlenecks: "slow_queries | inefficient_algorithms | resource_leaks"
  security_vulnerabilities: "owasp_violations | authentication_issues | data_exposure"
  architecture_concerns: "coupling_issues | modularity_problems | scalability_limits"
  
success_metrics:
  before_measurements: "baseline_performance_and_quality_metrics"
  target_improvements: "specific_percentage_improvements_expected"
  acceptance_criteria: "clear_pass_fail_criteria_for_each_improvement"
  rollback_triggers: "conditions_that_would_require_reverting_changes"
```

#### 📊 **Expected Deliverables Specification**
```yaml
improvement_outputs:
  improved_codebase: "All_files_updated_with_enhancements"
  performance_report: "Before/after_benchmarks_with_detailed_analysis"
  security_validation: "Vulnerability_scan_results_and_fixes_applied"
  quality_metrics: "Code_complexity,_coverage,_maintainability_scores"
  refactoring_documentation: "Patterns_applied,_rationale,_impact_analysis"
  migration_guide: "Step_by_step_upgrade_instructions"
  rollback_procedures: "Emergency_recovery_plans_and_scripts"
  continuous_improvement_plan: "Ongoing_maintenance_and_optimization_strategy"
```

---

## 🧹 **cleaner-spark** - Technical Debt Elimination

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "cleanup_scope": {
    "target_areas": ["dead_code", "unused_dependencies", "build_artifacts", "legacy_patterns"],
    "preservation_requirements": "critical_functionality_to_maintain",
    "cleanup_depth": "surface_level | comprehensive | deep_archaeological",
    "risk_tolerance": "conservative | moderate | aggressive"
  },
  "project_constraints": {
    "downtime_limits": "maximum_acceptable_service_interruption",
    "testing_requirements": "test_coverage_to_maintain_during_cleanup",
    "rollback_plan": "strategy_for_reverting_changes_if_issues_arise",
    "team_availability": "resources_for_validation_and_testing"
  },
  "cleanup_priorities": {
    "immediate_wins": "low_risk_high_impact_improvements",
    "security_focused": "vulnerable_dependencies_and_insecure_patterns",
    "performance_focused": "bottlenecks_and_resource_waste",
    "maintainability": "code_complexity_and_technical_debt_reduction"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Cleanup**: Technical Debt Scan → Priority Matrix → Cleanup Execution → Validation → Documentation
- **Target Metrics**:
  - Code reduction: 30-50%
  - Build time improvement: 20%+
  - Bundle size reduction: 30-50%
  - Memory usage reduction: 15-30%
  - Security vulnerabilities: 0
- **Cleanup Categories**:
  - Dead Code: Unused functions, variables, imports, comments
  - Dependencies: Outdated packages, unused dependencies, vulnerabilities
  - Code Quality: High complexity, duplication, poor naming
  - Build artifacts: Temp files, cache, generated files, logs

#### 🔧 **Safety Measures**
```yaml
validation_requirements:
  functionality_preservation: "100%_test_pass_rate_requirement"
  performance_monitoring: "no_degradation_in_critical_metrics"
  security_verification: "no_new_vulnerabilities_introduced"
  backward_compatibility: "api_compatibility_if_required"
  
incremental_approach:
  small_batches: "process_in_testable_increments"
  continuous_testing: "run_full_test_suite_after_each_change"
  progress_tracking: "measure_and_report_cleanup_impact"
  stakeholder_communication: "regular_updates_on_cleanup_progress"
```

#### 📊 **Expected Deliverables Specification**
```yaml
cleanup_outputs:
  cleaned_codebase: "Optimized_code_with_technical_debt_eliminated"
  cleanup_report: "Before/after_metrics_with_detailed_impact_analysis"
  removed_items_log: "Complete_list_of_deleted_files,_functions,_dependencies"
  performance_validation: "Build_time,_bundle_size,_runtime_improvements"
  security_clearance: "Updated_vulnerability_scan_showing_zero_issues"
  maintenance_guidelines: "Best_practices_to_prevent_future_technical_debt"
  recovery_procedures: "Rollback_instructions_if_issues_discovered_later"
  team_documentation: "Knowledge_transfer_about_cleanup_changes"
```

---

## 🏗️ **builder-spark** - Build System Optimization

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "project_analysis": {
    "project_type": "react | vue | angular | node | python | java | go | multi_language",
    "build_tools": ["webpack", "vite", "rollup", "parcel", "gradle", "maven", "cargo"],
    "deployment_targets": ["development", "staging", "production", "multiple_environments"],
    "performance_requirements": "build_time_goals | bundle_size_targets | startup_time"
  },
  "current_build_state": {
    "build_time_baseline": "current_development_and_production_build_times",
    "bundle_analysis": "current_bundle_sizes_and_composition",
    "pain_points": "slow_builds | large_bundles | complex_configuration | ci_failures",
    "resource_constraints": "ci_runner_specs | developer_machine_capabilities"
  },
  "optimization_goals": {
    "build_speed": "target_30_50_percent_reduction_in_build_time",
    "bundle_optimization": "target_bundle_sizes_and_performance_budgets", 
    "developer_experience": "hmr_speed | debugging_capabilities | error_reporting",
    "ci_cd_efficiency": "pipeline_speed | cache_effectiveness | parallel_execution"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Build Pattern**: Discovery → Foundation → Enhancement → Integration → Validation
- **Complexity Assessment**: scope (0.3) + file_count (0.3) + framework_complexity (0.4)
- **Performance Targets**:
  - Development builds: <5 seconds for HMR
  - Production builds: 30-50% reduction from baseline
  - Bundle sizes: Initial <500KB, Total <2MB
  - CI builds: <3 minutes with optimized caching
- **Quality Gates**: 8-step validation (syntax, types, linting, security, tests, performance, docs, integration)

#### 🔧 **Build Environment Details**
```yaml
environment_configuration:
  development_setup: "local_environment_requirements_and_configurations"
  ci_cd_environment: "runner_specifications_and_caching_strategies"
  deployment_pipeline: "build_artifact_handling_and_distribution"
  monitoring_integration: "build_performance_tracking_and_alerting"
  
optimization_strategies:
  code_splitting: "route_based | component_based | vendor_separation"
  tree_shaking: "dead_code_elimination_and_unused_import_removal"
  caching: "filesystem | memory | distributed | browser_caching"
  parallel_processing: "worker_threads | multicore_utilization"
  incremental_builds: "changed_file_detection_and_partial_rebuilds"
```

#### 📊 **Expected Deliverables Specification**
```yaml
build_optimization_outputs:
  optimized_configurations: "Production_ready_build_configs_for_all_environments"
  performance_benchmarks: "Before/after_build_time_and_bundle_size_comparisons"
  ci_cd_pipeline: "Automated_build_and_deployment_setup_with_caching"
  caching_strategy: "Multi_level_caching_implementation_and_documentation"
  optimization_report: "Detailed_analysis_of_applied_techniques_and_results"
  maintenance_playbook: "Guidelines_for_maintaining_and_updating_build_system"
  developer_guide: "Setup_instructions_and_troubleshooting_procedures"
  performance_monitoring: "Build_metrics_dashboard_and_alerting_setup"
```

---

## 📊 **estimater-spark** - Evidence-Based Project Estimation

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "estimation_request": {
    "project_type": "new_development | migration | refactoring | enhancement",
    "scope_description": "detailed_feature_requirements_and_acceptance_criteria",
    "deliverables": ["backend_api", "frontend_ui", "database_schema", "documentation"],
    "constraints": "timeline | budget | team_size | technology_restrictions"
  },
  "technical_complexity": {
    "technology_stack": "languages | frameworks | databases | infrastructure",
    "integration_requirements": "third_party_apis | existing_systems | data_migrations",
    "performance_requirements": "response_times | concurrent_users | data_volumes",
    "security_requirements": "authentication | authorization | compliance | encryption"
  },
  "team_context": {
    "team_size": "number_of_developers_and_skill_levels",
    "experience_level": "familiarity_with_technology_stack_and_domain",
    "availability": "full_time | part_time | percentage_allocation",
    "historical_velocity": "previous_project_completion_times_if_available"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Estimation**: Scope Analysis → Complexity Assessment → Historical Reference → Risk Evaluation → Scenario Presentation
- **Complexity Factors**: Technical complexity + Business complexity + Integration complexity + Risk factors
- **3-Point Estimation**:
  - Optimistic (P10): Best case scenario
  - Realistic (P50): Most likely outcome
  - Pessimistic (P90): Worst case with obstacles
- **Evidence Sources**: Historical data, industry benchmarks, team velocity, similar projects

#### 🔧 **Historical Context**
```yaml
reference_projects:
  similar_completed_projects: "scope | duration | team_size | technology_stack"
  industry_benchmarks: "standard_velocities_for_similar_project_types"
  team_velocity_data: "historical_completion_rates_and_productivity_metrics"
  technology_learning_curves: "ramp_up_time_for_new_technologies_or_team_members"
  
risk_assessment:
  technical_risks: "unproven_technologies | complex_integrations | performance_challenges"
  business_risks: "changing_requirements | stakeholder_availability | approval_delays"
  resource_risks: "team_turnover | skill_gaps | competing_priorities"
  external_risks: "dependency_delays | third_party_changes | regulatory_changes"
```

#### 📊 **Expected Deliverables Specification**
```yaml
estimation_outputs:
  executive_summary: "Project_overview,_complexity_assessment,_confidence_level"
  three_point_estimates: "Optimistic,_realistic,_pessimistic_scenarios_with_ranges"
  work_breakdown_structure: "Hierarchical_task_decomposition_with_time_estimates"
  risk_assessment: "Identified_risks_with_probability,_impact,_and_buffer_calculations"
  resource_allocation_plan: "Team_composition_and_role_assignments_over_time"
  milestone_timeline: "Key_deliverables_and_checkpoints_with_dependencies"
  confidence_analysis: "Accuracy_assessment_and_factors_affecting_reliability"
  contingency_planning: "Buffer_allocation_and_risk_mitigation_strategies"
```

---

## 📁 **loader-spark** - Comprehensive Project Onboarding

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "project_location": {
    "root_directory": "absolute_path_to_project_root",
    "access_permissions": "read_write_permissions_and_any_restricted_areas",
    "project_size": "estimated_file_count_and_codebase_size",
    "repository_info": "git_repository_url_and_branch_information"
  },
  "loading_purpose": {
    "use_case": "new_developer_onboarding | project_analysis | environment_setup | team_handoff",
    "focus_areas": ["architecture", "development_workflow", "deployment_process", "testing_strategy"],
    "depth_level": "quick_overview | comprehensive_analysis | deep_dive_documentation",
    "target_audience": "junior_developer | senior_developer | technical_lead | non_technical"
  },
  "project_context": {
    "project_stage": "proof_of_concept | active_development | maintenance | legacy",
    "team_structure": "team_size | roles | communication_channels",
    "business_domain": "industry | use_case | target_users"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Loading**: Structure Scan → Environment Analysis → Context Construction → Workspace Setup → Guide Generation
- **Auto-Detection Capabilities**:
  - Project Type: Frontend/Backend/Monorepo/Microservices/Mobile/AI-ML
  - Framework Detection: React, Vue, Angular, Express, FastAPI, Django, etc.
  - Build Tools: webpack, vite, gradle, maven, cargo, npm, yarn, pnpm
  - Testing Frameworks: jest, pytest, junit, mocha, cypress
- **Persona Activation**: Analyzer + Frontend/Backend/Architect based on detected type

#### 🔧 **Environment Analysis**
```yaml
development_environment:
  dependency_management: "package_managers | lock_files | version_constraints"
  development_servers: "local_server_configuration | hot_reloading | proxy_settings"
  database_setup: "connection_strings | migration_scripts | seed_data"
  external_services: "api_keys | service_configurations | mock_setups"
  
toolchain_configuration:
  ide_settings: "recommended_extensions | debug_configurations | workspace_settings"
  git_workflow: "branching_strategy | commit_conventions | pr_templates"
  ci_cd_pipeline: "automated_testing | deployment_process | quality_gates"
  monitoring_tools: "logging | error_tracking | performance_monitoring"
```

#### 📊 **Expected Deliverables Specification**
```yaml
loading_outputs:
  project_overview: "Architecture,_technology_stack,_complexity_assessment"
  quick_start_guide: "Setup_commands,_development_workflow,_common_tasks"
  architecture_diagrams: "System_overview,_component_relationships,_data_flow"
  development_setup: "Environment_configuration,_dependencies,_toolchain"
  critical_files_index: "Entry_points,_configuration_files,_key_modules"
  workflow_documentation: "Development_process,_testing_strategy,_deployment"
  troubleshooting_guide: "Common_issues,_solutions,_debugging_techniques"
  onboarding_checklist: "Step_by_step_tasks_for_new_team_members"
```

---

## 🎯 **spawner-spark** - Multi-Task Orchestration

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "orchestration_scope": {
    "operation_complexity": "simple(0.0-0.3) | moderate(0.3-0.7) | complex(0.7-1.0) | enterprise(>0.9)",
    "target_systems": ["frontend", "backend", "database", "infrastructure", "monitoring"],
    "execution_strategy": "sequential | parallel | hybrid | wave_based",
    "coordination_level": "single_domain | multi_domain | cross_team | enterprise_wide"
  },
  "task_requirements": {
    "main_operation": "detailed_description_of_primary_objective",
    "sub_operations": ["decomposed_tasks_or_components_involved"],
    "dependencies": "critical_prerequisite_relationships_and_constraints",
    "success_criteria": "measurable_completion_requirements"
  },
  "resource_constraints": {
    "time_budget": "available_execution_time_window",
    "token_budget": "computational_resource_limitations",
    "concurrency_limits": "maximum_parallel_operations_allowed",
    "rollback_requirements": "safety_mechanisms_and_recovery_procedures"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **6-Phase Orchestration**: Task Decomposition → Dependency Analysis → Execution Planning → Resource Allocation → Monitoring → Integration Validation
- **Execution Strategies**: Sequential/Parallel/Hybrid/Wave-based based on dependency analysis
- **Multi-Persona Coordination**: Architect, Frontend, Backend, Security, DevOps, QA, Performance
- **Complexity Auto-Detection**: ≥0.8 automatically activates advanced orchestration mode

#### 🔧 **Operation Categories**
```yaml
full_stack_deployment:
  components: "frontend_build | backend_services | database_migration | cdn_setup"
  coordination: "build_pipeline | deployment_sequence | health_checks | rollback_strategy"
  
ci_cd_pipeline_construction:
  elements: "source_control | build_automation | test_integration | security_scanning"
  orchestration: "pipeline_stages | parallel_execution | quality_gates | deployment_automation"
  
microservice_coordination:
  architecture: "service_discovery | api_gateway | inter_service_communication | load_balancing"
  monitoring: "distributed_tracing | circuit_breakers | health_endpoints | metrics_collection"
  
large_scale_refactoring:
  analysis: "code_impact_assessment | migration_strategy | test_coverage_enhancement"
  execution: "incremental_changes | backward_compatibility | gradual_rollout"
  
enterprise_integration:
  systems: "interconnection_mapping | data_synchronization | authentication_integration"
  compliance: "audit_logging | security_validation | disaster_recovery_planning"
```

#### 📊 **Expected Deliverables Specification**
```yaml
orchestration_outputs:
  orchestration_report: "Executive_summary,_task_breakdown,_dependency_graph,_timeline"
  execution_results: "Task_outcomes,_performance_metrics,_error_logs,_recovery_actions"
  integration_validation: "Health_checks,_end_to_end_tests,_performance_benchmarks"
  optimization_recommendations: "Bottleneck_identification,_parallelization_opportunities"
  resource_utilization: "Token_usage,_execution_time,_concurrency_metrics"
  rollback_documentation: "Recovery_procedures,_checkpoint_status,_contingency_plans"
```

---

## 🚨 **troubleshooter-spark** - Root Cause Analysis

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "problem_definition": {
    "symptom_description": "detailed_description_of_observable_issues",
    "problem_category": "performance | error_conditions | system_problems | infrastructure",
    "impact_assessment": "affected_users | services | business_operations",
    "urgency_level": "critical | high | medium | low"
  },
  "incident_timeline": {
    "first_occurrence": "when_problem_first_detected_with_timestamps",
    "frequency_pattern": "continuous | intermittent | scheduled | random",
    "recent_changes": "deployments | configurations | dependencies | infrastructure",
    "correlation_events": "related_system_changes_or_external_factors"
  },
  "system_context": {
    "affected_components": ["specific_services_or_modules_experiencing_issues"],
    "environment_details": "production | staging | development | specific_configuration",
    "architecture_complexity": "monolith | microservices | distributed | serverless",
    "monitoring_data": "available_logs | metrics | traces | alerts"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Analysis**: Symptom Analysis → Hypothesis Formation → Evidence Collection → Root Cause Verification → Solution Design
- **Complexity Calculation**: 
  - Affected systems >3 (+0.3)
  - Intermittent issues (+0.2)
  - Production impact (+0.1 to +0.3)
  - Unknown root cause (+0.2)
  - Cross-service dependencies (+0.2)
- **Wave Mode**: Auto-activates when complexity ≥0.7
- **Persona Coordination**: Analyzer + Performance/DevOps/Security based on issue type

#### 🔧 **Problem Categories**
```yaml
performance_issues:
  symptoms: "response_time_degradation | throughput_bottlenecks | resource_exhaustion"
  analysis: "query_optimization | network_latency | memory_profiling | cpu_utilization"
  
error_conditions:
  symptoms: "application_exceptions | integration_failures | timeout_issues"
  analysis: "stack_trace_analysis | dependency_mapping | retry_logic_examination"
  
system_problems:
  symptoms: "service_downtime | memory_leaks | connection_pool_exhaustion"
  analysis: "resource_monitoring | garbage_collection | database_performance"
  
infrastructure_challenges:
  symptoms: "container_orchestration | load_balancer_issues | certificate_problems"
  analysis: "deployment_pipeline | dns_resolution | ssl_configuration"
```

#### 📊 **Expected Deliverables Specification**
```yaml
troubleshooting_outputs:
  executive_summary: "Problem_statement,_business_impact,_confirmed_root_cause"
  detailed_analysis: "Symptom_timeline,_investigation_process,_causal_chain"
  solution_options: "Immediate_fixes,_short_term_solutions,_long_term_improvements"
  action_items: "Commands_and_scripts,_follow_up_tasks,_monitoring_setup"
  prevention_plan: "Monitoring_alerts,_safeguards,_process_improvements"
  documentation: "Runbooks,_post_mortem,_lessons_learned"
```

---

## 📋 **tasker-spark** - Enterprise Project Management

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "project_scope": {
    "project_location": "absolute_path_to_project_directory",
    "operation_type": "analyze | plan | execute | monitor",
    "complexity_assessment": "simple_project | multi_team_initiative | enterprise_transformation",
    "time_horizon": "sprint | quarter | multi_quarter | long_term"
  },
  "management_strategy": {
    "methodology": "systematic | agile | enterprise | hybrid",
    "wave_mode_trigger": "boolean_for_complex_projects_requiring_5_wave_execution",
    "tracking_depth": "quick | standard | comprehensive",
    "stakeholder_level": "development_team | management | executive | board"
  },
  "project_context": {
    "current_state": "project_initiation | active_development | maintenance | modernization",
    "team_structure": "single_team | cross_functional | multi_team | distributed",
    "business_criticality": "experimental | important | mission_critical | regulatory_required"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Task Management**: Project Analysis → Hierarchical Decomposition → Dependency Mapping → 5-Wave Execution → Monitoring Dashboard
- **Task Hierarchy**: Epic → Story → Task with clear ownership and timelines
- **Quality Gate Integration**: Jason's 8-step validation at each major milestone
- **Wave Mode**: Auto-activates for complexity ≥0.7 or enterprise-scale indicators

#### 🔧 **Task Management Capabilities**
```yaml
hierarchical_decomposition:
  structure: "Epic_to_Story_to_Task_breakdown_with_clear_ownership"
  tracking: "status_indicators_(✅_⏳_📝_🚧)_with_TodoWrite_integration"
  dependencies: "prerequisite_relationships_and_critical_path_analysis"
  
5_wave_execution_planning:
  wave_1_discovery: "requirements_analysis | architecture_review | risk_assessment"
  wave_2_core: "foundation_implementation | core_functionality_development"
  wave_3_integration: "system_integration | api_development | data_flow"
  wave_4_quality: "testing | security_review | performance_optimization"
  wave_5_deployment: "production_deployment | monitoring | documentation"
  
resource_optimization:
  allocation: "team_composition | skill_matching | workload_balancing"
  timeline: "milestone_planning | buffer_management | risk_mitigation"
  tracking: "real_time_progress | kpi_metrics | automated_reporting"
```

#### 📊 **Expected Deliverables Specification**
```yaml
project_management_outputs:
  hierarchical_task_structure: "Complete_WBS_with_Epic_Story_Task_breakdown"
  dependency_graph: "Mermaid_diagrams_with_critical_path_and_parallel_opportunities"
  5_wave_execution_plan: "Detailed_timeline_with_resource_allocation_and_milestones"
  real_time_dashboard: "Progress_tracking_with_visual_indicators_and_metrics"
  quality_gate_checklist: "Jason_8_step_validation_integrated_at_each_phase"
  risk_assessment_matrix: "Identified_risks_with_probability_impact_mitigation"
  performance_kpis: "Success_metrics_completion_criteria_progress_indicators"
  project_completion_report: "Final_deliverables_lessons_learned_recommendations"
```

---
#### 📋 **Essential Context (Always Provide)**
```json
{
  "orchestration_scope": {
    "operation_type": "full_stack_deployment | ci_cd_setup | large_scale_refactoring | system_migration",
    "subsystems": ["frontend", "backend", "database", "infrastructure", "monitoring"],
    "complexity_indicators": "number_of_services | integration_points | deployment_environments",
    "coordination_requirements": "sequential_dependencies | parallel_opportunities | resource_constraints"
  },
  "task_decomposition": {
    "primary_objectives": "high_level_goals_and_success_criteria",
    "component_breakdown": "individual_systems_and_their_responsibilities",
    "integration_points": "how_components_communicate_and_share_data",
    "quality_gates": "validation_requirements_at_each_stage"
  },
  "resource_allocation": {
    "available_resources": "development_team | infrastructure | time_constraints | budget",
    "persona_requirements": "specialized_expertise_needed_for_each_task",
    "tool_dependencies": "required_mcp_servers | external_services | access_credentials",
    "execution_timeline": "overall_deadline | milestone_checkpoints | critical_path"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **6-Phase Orchestration**: Task Decomposition → Dependency Analysis → Execution Planning → Resource Allocation → Monitoring & Coordination → Integration Validation
- **Complexity Thresholds**:
  - Simple (0.0-0.3): Single domain, <5 tasks, linear execution
  - Complex (0.7-1.0): Multi-domain, >15 tasks, heavy parallelization
  - Enterprise (>0.9): System-wide, >50 tasks, distributed execution
- **Execution Strategies**: Sequential, Parallel, Hybrid, Wave-based
- **Multi-Persona Coordination**: Architect, Frontend, Backend, Security, DevOps, QA, Performance

#### 🔧 **Coordination Requirements**
```yaml
task_orchestration:
  dependency_mapping: "task_prerequisites | blocking_relationships | critical_path_analysis"
  parallel_execution: "independent_tasks | resource_sharing | synchronization_points"
  rollback_strategy: "checkpoint_creation | failure_recovery | state_restoration"
  progress_monitoring: "real_time_tracking | milestone_validation | bottleneck_detection"
  
integration_validation:
  system_health_checks: "end_to_end_functionality | performance_benchmarks"
  data_consistency: "state_synchronization | transaction_integrity | backup_verification"
  security_validation: "access_control | encryption | audit_trail"
  business_continuity: "service_availability | user_impact | rollback_capability"
```

#### 📊 **Expected Deliverables Specification**
```yaml
orchestration_outputs:
  orchestration_plan: "Complete_task_breakdown_with_dependencies_and_timeline"
  execution_results: "Individual_task_outcomes_with_success_failure_metrics"
  integration_report: "System_health_validation_and_end_to_end_testing_results"
  performance_analysis: "Resource_utilization_and_optimization_recommendations"
  risk_mitigation: "Issues_encountered_and_contingency_actions_taken"
  lessons_learned: "Process_improvements_and_best_practices_identified"
  runbook_creation: "Operational_procedures_for_ongoing_maintenance"
  stakeholder_communication: "Executive_summary_and_business_impact_assessment"
```

---

## 📋 **tasker-spark** - Enterprise Project Management

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "project_scope": {
    "initiative_type": "new_product_development | system_modernization | platform_migration | enterprise_integration",
    "business_objectives": "revenue_goals | efficiency_improvements | cost_reduction | user_experience_enhancement",
    "stakeholder_landscape": "executive_sponsors | product_owners | development_teams | end_users",
    "success_metrics": "kpis | okrs | business_value_measurements"
  },
  "project_characteristics": {
    "complexity_assessment": "multi_team | multi_technology | regulatory_compliance | high_availability",
    "duration_expectations": "weeks | months | quarters | multi_year_initiative",
    "resource_availability": "team_size | skill_mix | budget_constraints | vendor_dependencies",
    "risk_factors": "technical_unknowns | regulatory_changes | market_pressures | resource_constraints"
  },
  "execution_context": {
    "methodology_preference": "agile | waterfall | hybrid | continuous_delivery",
    "reporting_requirements": "stakeholder_updates | governance_reviews | compliance_reporting",
    "integration_needs": "existing_systems | data_migration | business_process_changes",
    "quality_standards": "performance_requirements | security_standards | compliance_frameworks"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Task Management**: Project Analysis & Discovery → Hierarchical Task Decomposition → Dependency Mapping & Critical Path → 5-Wave Execution Planning → Monitoring & Dashboard Setup
- **Complexity Triggers**: Wave mode auto-activation when complexity ≥0.7 or enterprise indicators
- **5-Wave Execution Strategy**:
  - Wave 1: Discovery (requirements, architecture, risk assessment)
  - Wave 2: Core (foundation implementation, core functionality)
  - Wave 3: Integration (system integration, API development, data flow)
  - Wave 4: Quality (testing, security review, performance optimization)  
  - Wave 5: Deployment (production deployment, monitoring, documentation)

#### 🔧 **Project Management Framework**
```yaml
task_hierarchy:
  epic_level: "major_business_capabilities_or_system_components"
  story_level: "user_facing_features_or_technical_capabilities"
  task_level: "specific_implementation_units_with_clear_completion_criteria"
  
tracking_mechanisms:
  progress_indicators: "completed ✅ | in_progress ⏳ | planned 📝 | blocked 🚧"
  quality_gates: "jasons_8_step_validation_at_major_milestones"
  risk_monitoring: "continuous_assessment_with_escalation_procedures"
  resource_tracking: "capacity_planning_and_utilization_monitoring"
```

#### 📊 **Expected Deliverables Specification**
```yaml
project_management_outputs:
  hierarchical_task_structure: "Complete_WBS_with_Epic_Story_Task_breakdown"
  dependency_visualization: "Mermaid_diagrams_with_critical_path_highlighting"
  execution_roadmap: "5_Wave_timeline_with_milestones_and_quality_gates"
  progress_dashboard: "Real_time_tracking_with_visual_indicators_and_KPIs"
  risk_management_plan: "Risk_register_with_mitigation_strategies_and_ownership"
  resource_allocation_matrix: "Team_assignments_and_capacity_planning_across_waves"
  stakeholder_communication_plan: "Reporting_schedule_and_escalation_procedures"
  project_completion_report: "Final_deliverables_and_lessons_learned_documentation"
```

---

## ⚙️ **gitter-spark** - Git Workflow Architecture

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "team_structure": {
    "team_size": "1_5_small | 5_20_medium | 20plus_large",
    "skill_levels": "junior | mixed | senior | expert",
    "distributed_team": "co_located | distributed | hybrid | remote_first",
    "collaboration_patterns": "pair_programming | code_review_heavy | async_development"
  },
  "project_characteristics": {
    "project_type": "startup | enterprise | open_source | regulated_industry",
    "release_frequency": "continuous | weekly | monthly | quarterly",
    "stability_requirements": "experimental | production_critical | high_availability",
    "compliance_needs": "audit_trails | regulatory_approval | security_clearance"
  },
  "current_git_state": {
    "existing_strategy": "current_branching_model | commit_conventions | review_process",
    "pain_points": "merge_conflicts | deployment_delays | code_review_bottlenecks",
    "repository_structure": "monorepo | multi_repo | hybrid_approach",
    "integration_requirements": "ci_cd_systems | issue_tracking | deployment_automation"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Git Workflow**: Strategy Selection → Branch Configuration → Rules Establishment → Automation Setup → Team Guidance
- **Strategy Auto-Selection**:
  - Small teams (1-5): GitHub Flow (simple, fast iterations)
  - Medium teams (5-20): GitFlow (structured releases)
  - Large teams (20+): GitLab Flow (environment branches)
- **Automation Integration**: Pre-commit hooks, commit-msg validation, CI/CD integration, automated versioning
- **Quality Standards**: Enforced conventions, comprehensive documentation, scalable design

#### 🔧 **Workflow Configuration**
```yaml
branching_strategy:
  github_flow: "main + feature_branches | simple_workflow | continuous_deployment"
  gitflow: "main_develop_feature_release_hotfix | structured_releases | scheduled_deployments"
  gitlab_flow: "main_pre_production_production | environment_branches | staged_deployment"
  
automation_requirements:
  commit_conventions: "conventional_commits | semantic_versioning | automated_changelog"
  code_quality: "pre_commit_linting | automated_testing | security_scanning"
  deployment_integration: "ci_cd_triggers | automated_releases | rollback_capabilities"
  team_enforcement: "branch_protection | required_reviews | status_checks"
```

#### 📊 **Expected Deliverables Specification**
```yaml
git_workflow_outputs:
  configuration_files: "gitignore | gitattributes | gitmessage | hook_scripts"
  automation_setup: "pre_commit_hooks | ci_cd_integration | release_automation"
  documentation_package: "workflow_guide | quick_reference | troubleshooting_guide"
  team_onboarding: "setup_instructions | best_practices | common_scenarios"
  branch_protection: "repository_settings | access_controls | review_requirements"
  integration_configs: "issue_tracking | deployment_pipelines | notification_setup"
  migration_plan: "transition_strategy | timeline | risk_mitigation"
  maintenance_procedures: "workflow_updates | team_training | continuous_improvement"
```

---

## 🎓 **explainer-spark** - Educational Content Creation

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "learning_objective": {
    "topic_scope": "programming_concept | framework_feature | design_pattern | algorithm | system_architecture",
    "complexity_level": "beginner | intermediate | advanced | expert",
    "learning_context": "onboarding | skill_development | problem_solving | certification_prep",
    "time_constraints": "quick_overview | comprehensive_tutorial | deep_dive_course"
  },
  "audience_profile": {
    "experience_level": "complete_beginner | some_programming | experienced_developer | domain_expert",
    "background_knowledge": "prerequisite_concepts | familiar_technologies | learning_style_preferences",
    "practical_goals": "immediate_application | theoretical_understanding | teaching_others | building_foundation",
    "preferred_format": "text_heavy | visual_diagrams | hands_on_examples | interactive_exercises"
  },
  "content_requirements": {
    "depth_preference": "overview_only | practical_focus | theoretical_foundation | comprehensive_coverage",
    "example_complexity": "simple_demonstrations | real_world_applications | complex_scenarios | edge_cases",
    "interaction_level": "passive_reading | guided_exercises | independent_practice | project_based",
    "assessment_needs": "understanding_check | practical_validation | certification_requirements"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **3-Phase Educational Pattern**: Concept Collection → Structure Organization → Customization
- **Complexity Assessment**: 0.1-0.3 for educational requests (focusing on clarity over complexity)
- **Pedagogical Techniques**: Progressive disclosure, active learning, multiple perspectives
- **Content Adaptation**: Beginner-friendly analogies vs expert-level nuances
- **Interactive Elements**: Thought-provoking questions, practice exercises, real-world connections

#### 🔧 **Educational Content Structure**
```yaml
content_organization:
  overview_section: "importance | key_concepts | learning_outcomes"
  prerequisite_knowledge: "required_background | recommended_preparation | skill_assumptions"
  core_explanation: "fundamental_principles | step_by_step_breakdown | conceptual_framework"
  practical_examples: "working_code | use_case_scenarios | problem_solving_applications"
  advanced_topics: "edge_cases | optimization_techniques | related_concepts"
  practice_opportunities: "exercises | challenges | project_suggestions"
  
visual_aids:
  diagrams: "concept_maps | flowcharts | architecture_diagrams | process_visualization"
  code_examples: "minimal_examples | progressive_complexity | annotated_explanations"
  comparisons: "alternative_approaches | pros_cons_analysis | decision_frameworks"
  troubleshooting: "common_mistakes | debugging_techniques | best_practices"
```

#### 📊 **Expected Deliverables Specification**
```yaml
educational_outputs:
  structured_explanation: "Clear_progression_from_basics_to_advanced_concepts"
  practical_examples: "Working_code_demonstrations_with_detailed_annotations"
  visual_learning_aids: "Diagrams,_flowcharts,_and_conceptual_illustrations"
  interactive_elements: "Questions,_exercises,_and_hands_on_activities"
  assessment_materials: "Knowledge_checks,_practice_problems,_project_ideas"
  further_learning: "Advanced_topics,_related_concepts,_recommended_resources"
  troubleshooting_guide: "Common_pitfalls,_debugging_tips,_best_practices"
  reference_materials: "Quick_reference_cards,_cheat_sheets,_documentation_links"
```

---

## 📖 **indexer-spark** - Command Catalog Navigation

### Core Information Requirements

#### 📋 **Essential Context (Always Provide)**
```json
{
  "exploration_purpose": {
    "user_goal": "learn_superclaude | find_right_command | optimize_workflow | understand_capabilities",
    "experience_level": "complete_beginner | some_familiarity | experienced_user | power_user",
    "specific_need": "command_recommendation | workflow_optimization | capability_discovery | troubleshooting",
    "time_availability": "quick_reference | comprehensive_overview | detailed_exploration | learning_session"
  },
  "context_requirements": {
    "project_type": "web_development | api_development | data_analysis | system_administration",
    "workflow_stage": "planning | development | testing | deployment | maintenance",
    "complexity_level": "simple_tasks | moderate_projects | complex_systems | enterprise_scale",
    "team_dynamics": "solo_developer | small_team | large_organization | multi_team_coordination"
  },
  "command_interests": {
    "domain_focus": "development | analysis | quality | meta_commands | all_domains",
    "specific_commands": "known_commands_of_interest | commands_to_avoid | preferred_approaches",
    "integration_needs": "command_chaining | parallel_execution | workflow_automation | hook_integration",
    "learning_priorities": "immediate_application | foundational_knowledge | advanced_techniques | best_practices"
  }
}
```

#### ⚙️ **Configuration Parameters**
- **5-Phase Index Execution**: Discovery → Analysis → Categorization → Recommendation → Documentation
- **Command Domains**: Development (/build, /implement, /design), Analysis (/analyze, /troubleshoot, /explain), Quality (/improve, /cleanup, /test), Meta (/index, /load, /spawn, /task, /git, /document, /estimate)
- **Complexity Levels**: Simple (0.0-0.4), Moderate (0.4-0.7), Complex (0.7-1.0)
- **Usage Patterns**: Auto-activation triggers, flag combinations, optimal workflows

#### 🔧 **Navigation Framework**
```yaml
command_categorization:
  by_domain: "development_focused | analysis_focused | quality_focused | meta_management"
  by_complexity: "beginner_friendly | intermediate_complexity | advanced_orchestration"
  by_execution_time: "quick_operations | standard_tasks | long_running_processes"
  by_integration: "standalone_commands | chain_friendly | orchestration_compatible"
  
workflow_patterns:
  sequential_workflows: "command_a_then_b_then_c | dependency_based_execution"
  parallel_workflows: "simultaneous_execution | resource_sharing | coordination_points"
  conditional_workflows: "decision_based_routing | adaptive_execution | error_handling"
  iterative_workflows: "feedback_loops | progressive_refinement | continuous_improvement"
```

#### 📊 **Expected Deliverables Specification**
```yaml
indexing_outputs:
  command_catalog: "Complete_reference_with_descriptions_and_use_cases"
  interactive_explorer: "Conversational_command_discovery_and_recommendation"
  workflow_guides: "Optimal_command_sequences_for_common_scenarios"
  decision_trees: "Command_selection_logic_based_on_project_characteristics"
  quick_reference: "Cheat_sheets_and_command_summaries_for_rapid_access"
  learning_pathways: "Progressive_skill_development_through_command_mastery"
  integration_patterns: "Hook_automation_and_workflow_optimization_strategies"
  troubleshooting_matrix: "Command_selection_for_specific_problems_and_situations"
```

---

## 🔄 Common Information for All Agents

### Universal Context Requirements (Hook Automation)

#### 📋 **Project Environment**
```json
{
  "working_directory": "current_project_root_path",
  "git_repository": "repository_url_and_current_branch",
  "project_metadata": {
    "name": "project_name",
    "version": "current_version",
    "description": "project_purpose_and_scope",
    "team": "team_members_and_roles"
  },
  "technology_stack": {
    "languages": ["primary_and_secondary_languages"],
    "frameworks": ["main_frameworks_and_libraries"],
    "databases": ["database_systems_and_versions"],
    "infrastructure": ["deployment_platforms_and_services"]
  }
}
```

#### ⚙️ **Quality Standards (Jason's 8-Step Gates)**
```yaml
quality_gates:
  1_syntax_validation: "0_compilation_errors_required"
  2_type_checking: "mypy_strict_mode_0_errors"
  3_linting: "ruff_strict_mode_0_violations"
  4_security_analysis: "OWASP_compliance_0_critical_vulnerabilities"
  5_test_coverage: "Unit_95%_Integration_85%_Overall_90%"
  6_performance_check: "response_times_memory_usage_within_targets"
  7_documentation_validation: "docstrings_api_docs_user_guides_complete"
  8_integration_testing: "end_to_end_workflows_functional"
```

#### 🔧 **Execution Context**
```yaml
execution_environment:
  complexity_assessment: "auto_calculated_0.0_1.0_score"
  wave_mode_trigger: "complexity_gte_0.7_auto_activation"
  persona_activation: "domain_based_automatic_selection"
  mcp_server_coordination: "intelligent_server_utilization"
  progress_tracking: "todowrite_integration_required"
  error_handling: "graceful_degradation_rollback_procedures"
```

### Automation Patterns (Hook Integration)

#### 📋 **UserPromptSubmit Hook**
- **Persona Router**: Analyze task and activate appropriate personas
- **Context Enrichment**: Add project metadata, recent changes, known issues
- **Complexity Assessment**: Calculate and determine execution mode
- **Resource Allocation**: Assign MCP servers and tools based on requirements

#### 🔧 **SubagentStop Hook**
- **Quality Gates**: Validate against Jason's 8-step requirements
- **Progress Tracking**: Update TodoWrite with completion status
- **Result Validation**: Ensure deliverables meet specifications
- **Context Relay**: Pass results to next phase or agent if needed

#### 📊 **Continuous Monitoring**
- **Performance Metrics**: Track execution time, resource usage, success rates
- **Quality Metrics**: Monitor compliance with standards and requirements
- **User Satisfaction**: Track successful task completion and user feedback
- **Improvement Opportunities**: Identify optimization potential

---

## 🎯 Agent Selection Decision Matrix

| Task Type | Primary Agent | Secondary Agents | Complexity Threshold | Typical Duration |
|-----------|---------------|------------------|---------------------|------------------|
| **System Analysis** | analyzer-spark | troubleshooter-spark | 0.5+ | 30-120 min |
| **Architecture Design** | designer-spark | analyzer-spark | 0.6+ | 60-240 min |
| **Feature Implementation** | implementer-spark | tester-spark | 0.4+ | 120-480 min |
| **Quality Assurance** | tester-spark | improver-spark | 0.3+ | 60-180 min |
| **Documentation** | documenter-spark | explainer-spark | 0.2+ | 30-120 min |
| **Problem Resolution** | troubleshooter-spark | analyzer-spark | 0.7+ | 15-90 min |
| **Code Enhancement** | improver-spark | cleaner-spark | 0.5+ | 60-240 min |
| **Technical Debt** | cleaner-spark | improver-spark | 0.4+ | 120-360 min |
| **Build Optimization** | builder-spark | improver-spark | 0.6+ | 60-180 min |
| **Project Estimation** | estimater-spark | tasker-spark | 0.3+ | 30-90 min |
| **Project Onboarding** | loader-spark | documenter-spark | 0.4+ | 45-120 min |
| **Multi-Task Coordination** | spawner-spark | tasker-spark | 0.8+ | 180-600 min |
| **Project Management** | tasker-spark | spawner-spark | 0.7+ | 240-960 min |
| **Git Workflow** | gitter-spark | loader-spark | 0.3+ | 30-90 min |
| **Educational Content** | explainer-spark | documenter-spark | 0.2+ | 45-120 min |
| **Command Discovery** | indexer-spark | explainer-spark | 0.1+ | 15-45 min |

---

*This guide ensures every SPARK agent receives optimal context for maximum effectiveness. Each agent is designed to work independently while contributing to the overall SPARK ecosystem through intelligent automation and quality-driven execution.*