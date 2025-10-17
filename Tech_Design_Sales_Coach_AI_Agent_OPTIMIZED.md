# Sales Coach in the Pocket: Enterprise AI Agent - OPTIMIZED Technical Design

**System Name:** Sales Coach in the Pocket (SCIP)
**Version:** 2.1 - Optimized Architecture
**Date:** October 2025
**Classification:** Best Practices Architecture (ImpactWon Methodology)
**Target Platform:** Microsoft Azure Cloud
**Architecture Philosophy:** Lean Agents + Rich Tools (MCP)

---

## Executive Summary

### Key Optimizations from v2.0

| Aspect | v2.0 (Original) | v2.1 (Optimized) | Improvement |
|--------|-----------------|------------------|-------------|
| **Agent Count** | 21 agents | 6-7 agents | **70% reduction** |
| **Architecture** | Agent-heavy | Lean agents + MCP tools | Simplified |
| **UI Layer** | Web + Mobile + Salesforce | Web + Mobile only | Removed bloat |
| **Operational Cost** | ~$15K/month | ~$5-7K/month | **50-60% savings** |
| **Latency (P95)** | 3-5s | 1-2s | **50-60% faster** |
| **Maintainability** | Complex (21 agents) | Moderate (6-7 agents) | Easier debugging |

### Vision Statement

Sales Coach in the Pocket is an **enterprise-grade, lean multi-agent AI system** built on the ImpactWon sales methodology. By following AI best practices of "**Lean Agents + Rich Tools**", SCIP provides the "Right to Win" assessment, strategic recommendations, and automated insights with **70% fewer agents** than traditional architectures.

### Core Philosophy: Lean Agents + Rich Tools

**Agents** (6-7 core):
- Autonomous reasoning and decision-making
- Complex, multi-step workflows
- State management and planning
- Handle ambiguity and strategic thinking

**MCP Tools** (Functions/Services):
- Stateless data retrieval
- Deterministic transformations
- Template-based generation
- Classification and scoring algorithms

---

## 1. Optimized System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                           │
│  ┌──────────────────────────┬──────────────────────────────────────┐   │
│  │     Web Portal           │        Mobile App                     │   │
│  │     (React/Next.js)      │        (React Native)                 │   │
│  │     - Responsive PWA     │        - iOS & Android                │   │
│  │     - SSR/SSG            │        - Offline support              │   │
│  └──────────────────────────┴──────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│                    API GATEWAY + AI GATEWAY                              │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  Azure API Management + AI Gateway Services                        │ │
│  │  ┌──────────────────────────────────────────────────────────────┐ │ │
│  │  │  Model Routing        - Route to optimal LLM                 │ │ │
│  │  │  Token-Based Limiting - Cost control per user/tier           │ │ │
│  │  │  AI Guardrails        - Content safety, bias detection       │ │ │
│  │  │  Semantic Caching     - Redis + Vector cache                 │ │ │
│  │  │  Observability        - LangFuse + App Insights              │ │ │
│  │  └──────────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│               LEAN AGENTIC ORCHESTRATION LAYER (6-7 Agents)              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              Supervisor Agent (LangGraph)                         │  │
│  │  - Task decomposition aligned with ImpactWon                     │  │
│  │  - Agent routing (6 core agents)                                 │  │
│  │  - MCP tool orchestration                                        │  │
│  │  - 4Cs workflow state management                                 │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────── CORE AGENTS (Tier 2) ─────────────────────────┐ │
│  │  Power Plan Agent (4Cs)    │  Strategic Planning Agent           │ │
│  │  THE CRITICAL AGENT         │  (CEO Plan + Attainment + Pursuit) │ │
│  │  - 4Cs calculation          │  - Bedrock deal planning           │ │
│  │  - Right to Win scoring     │  - Multi-year strategy             │ │
│  └─────────────────────────────┴─────────────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────── SUPPORTING AGENTS (Tier 2) ───────────────────┐ │
│  │  Client Intelligence Agt   │  Deal Assessment Agent              │ │
│  │  - Client profiling         │  - Deal qualification              │ │
│  │  - BBB stakeholder mapping  │  - Budget validation               │ │
│  │  - Trap detection           │  - Risk assessment                 │ │
│  │                             │                                     │ │
│  │  Team Orchestration Agent  │  [Optional] Real-time Coach Agent  │ │
│  │  - Team planning            │  - Live meeting support            │ │
│  │  - Right team selection     │  - Transcription + coaching        │ │
│  └─────────────────────────────┴─────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│                       MCP TOOLS LAYER (Not Agents!)                      │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  MCP Servers & Function Tools                                    │  │
│  │  ┌────────────────┬────────────────┬──────────────────────────┐ │  │
│  │  │ Research Tool  │ Content Gen    │ Competitive Intel Tool   │ │  │
│  │  │ - Web search   │ Tool           │ - Competitor tracking    │ │  │
│  │  │ - News aggr.   │ - Email tmpl   │ - Product comparison     │ │  │
│  │  │ - Social media │ - Proposal gen │ - Pricing intel          │ │  │
│  │  └────────────────┴────────────────┴──────────────────────────┘ │  │
│  │                                                                  │  │
│  │  ┌────────────────────────────────────────────────────────────┐ │  │
│  │  │  Function Tools (Stateless)                                │ │  │
│  │  │  - FOG Analysis (Fact/Opinion/Gossip classifier)           │ │  │
│  │  │  - Engagement Excellence (6 lenses analyzer)               │ │  │
│  │  │  - Impact Theme Generator (from 4Cs Control score)         │ │  │
│  │  │  - License to Sell (competency scorer)                     │ │  │
│  │  │  - Find Money Validator (budget checker)                   │ │  │
│  │  └────────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│                      REASONING & MEMORY LAYER                            │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  LLM Router (Model Selection & Load Distribution)                │  │
│  │  ┌────────────┬────────────┬────────────┬────────────┐          │  │
│  │  │  GPT-4o    │  Claude    │  Claude    │  Gemini    │          │  │
│  │  │  (Primary) │  Opus      │  Sonnet    │  Pro       │          │  │
│  │  │            │  (Critical)│  (Research)│  (Multi)   │          │  │
│  │  └────────────┴────────────┴────────────┴────────────┘          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Context & Memory Management                                     │  │
│  │  - Conversation History (Redis + Cosmos DB)                      │  │
│  │  - Long-term Memory (Azure SQL + Vector Embeddings)              │  │
│  │  - Semantic Cache (Redis + Milvus)                               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│                      KNOWLEDGE & DATA LAYER                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Multi-Modal Knowledge Graph (Neo4j Enterprise)                  │  │
│  │  - ImpactWon Entities (4Cs, Deals, Clients, Stakeholders)       │  │
│  │  - Relationship Discovery (BBB mapping)                          │  │
│  │  - Temporal Graph (Power Plan evolution tracking)                │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────────┐ │
│  │  Vector DB   │  Search      │  Data Lake   │  Data Warehouse      │ │
│  │  (Milvus)    │  (Cognitive) │  (ADLS Gen2) │  (Synapse)           │ │
│  └──────────────┴──────────────┴──────────────┴──────────────────────┘ │
│                                                                          │
│  ┌─────────────────────────── Data Buckets ──────────────────────────┐ │
│  │  COMPANY Bucket  │  CLIENT Bucket  │  INDUSTRY Bucket  │  DEAL    │ │
│  │                  │                 │                   │  Bucket  │ │
│  │                  │                 │                   │  +4Cs    │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│                       DATA INGESTION & ETL LAYER                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Azure Data Factory (Orchestration)                              │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────────┐ │
│  │  Web         │  API         │  CRM Data    │  News/Social         │ │
│  │  Crawlers    │  Integrators │  Sync        │  Media Listeners     │ │
│  │  (Scrapy)    │  (REST API)  │  (HubSpot,   │  (Twitter, LinkedIn  │ │
│  │              │              │  Salesforce  │   APIs - data only)  │ │
│  │              │              │  REST APIs)  │                      │ │
│  └──────────────┴──────────────┴──────────────┴──────────────────────┘ │
│                                                                          │
│  NOTE: CRM integration is DATA SYNC only (no UI components)             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Lean Multi-Agent Design (ImpactWon-Aligned)

### 2.1 Optimized Agent Registry (6-7 Agents)

```python
# OPTIMIZED: From 21 agents to 6-7 agents
# Philosophy: Each agent is AUTONOMOUS with COMPLEX REASONING
# Simple tasks delegated to MCP tools

OPTIMIZED_AGENT_REGISTRY = {

    #========================================================================
    # TIER 1: ORCHESTRATION (1 Agent)
    #========================================================================

    "supervisor": {
        "name": "Supervisor Agent",
        "model": "GPT-4o",
        "role": "Master orchestrator using ImpactWon framework",
        "capabilities": [
            "Task decomposition aligned with Right Model",
            "Agent selection (routes to 6 core agents)",
            "MCP tool orchestration",
            "4Cs workflow management",
            "Result aggregation for Power Plan"
        ],
        "framework_alignment": "Overall orchestration",
        "cost_tier": "premium",
        "available_agents": [
            "power_plan_agent",
            "strategic_planning_agent",
            "client_intelligence_agent",
            "deal_assessment_agent",
            "team_orchestration_agent",
            "realtime_coach_agent"
        ],
        "available_tools": [
            "research_tool",
            "content_generation_tool",
            "competitive_intel_tool",
            "fog_analysis_tool",
            "engagement_excellence_tool",
            "impact_theme_generator_tool",
            "license_to_sell_tool",
            "find_money_validator_tool"
        ],
        "sla": {
            "latency_p95": "300ms",
            "availability": "99.99%"
        }
    },

    #========================================================================
    # TIER 2: CORE BUSINESS LOGIC AGENTS (5-6 Agents)
    #========================================================================

    "power_plan_agent": {
        "name": "Power Plan Agent (4Cs Assessment)",
        "model": "GPT-4o",
        "role": "THE MOST CRITICAL AGENT - Calculate Right to Win via 4Cs",
        "right_model_component": "6. Power Plan (Heart of ImpactWon)",
        "capabilities": [
            "4Cs calculation (Credibility, Capability, Commitment, Control)",
            "Real-time Right to Win scoring",
            "Initiative recommendation to improve 4Cs",
            "Moment-in-time snapshot analysis",
            "Tracking score evolution over time",
            "Binary qualifier validation (YES/NO questions)"
        ],
        "scoring_methodology": {
            "credibility": {
                "formula": "Knowledge × Trust",
                "qualifier_question": "Can you meet CEO within 7 days?",
                "max_score_if_yes": 100,
                "max_score_if_no": 50
            },
            "capability": {
                "formula": "Competence × Quantum",
                "qualifier_question": "Can you reference in region, in industry?",
                "max_score_if_yes": 100,
                "max_score_if_no": 50
            },
            "commitment": {
                "formula": "Outcome × Satisfaction",
                "qualifier_question": "Is client currently buying from us?",
                "max_score_if_yes": 100,
                "max_score_if_no": 50
            },
            "control": {
                "formula": "Mastery × Influence",
                "qualifier_question": "Can you see your fingerprints on this deal?",
                "max_score_if_yes": 100,
                "max_score_if_no": 50
            }
        },
        "tools": [
            "research_tool",
            "fog_analysis_tool",
            "impact_theme_generator_tool"
        ],
        "data_buckets": ["deal", "client", "company"],
        "cost_tier": "premium",
        "critical": True,
        "why_agent": "Complex reasoning: Multi-factor scoring, initiative generation, temporal analysis"
    },

    "strategic_planning_agent": {
        "name": "Strategic Planning Agent",
        "model": "Claude 3.5 Sonnet",
        "role": "CONSOLIDATED: CEO Sales Plan + Attainment + Pursuit Planning",
        "right_model_components": [
            "1. CEO Sales Plan",
            "2. Attainment Plan",
            "5. Pursuit Plan"
        ],
        "capabilities": [
            # CEO Sales Plan
            "Distill CEO vision into sales strategy",
            "Identify bedrock deals aligned with company direction",
            "Map strategic imperatives to market opportunities",

            # Attainment Plan
            "Multi-year plan creation per Client Expert",
            "Bedrock + Stepping Stone deal mapping",
            "Resource allocation across deals",
            "Timeline and milestone planning",

            # Pursuit Plan
            "Client analysis and segmentation",
            "Deal-specific strategy formulation",
            "Competitive positioning",
            "Execution roadmap creation"
        ],
        "tools": [
            "research_tool",
            "content_generation_tool",
            "competitive_intel_tool",
            "engagement_excellence_tool"
        ],
        "data_buckets": ["company", "client", "deal", "industry"],
        "cost_tier": "premium",
        "why_agent": "Strategic reasoning: Long-term planning, ambiguity handling, multi-stakeholder alignment",
        "consolidation_rationale": "CEO Plan → Attainment → Pursuit are sequential strategic planning phases"
    },

    "client_intelligence_agent": {
        "name": "Client Intelligence Agent",
        "model": "GPT-4o",
        "role": "CONSOLIDATED: Client Profiling + BBB Stakeholder Mapping + Right Clients",
        "right_model_components": [
            "7. Right Clients"
        ],
        "right_tools_components": [
            "4. Client Profiles",
            "6. Buyers, Beneficiaries, Backers"
        ],
        "capabilities": [
            # Client Profiling
            "Profile classification (New/Transactional/Repeatable/Meaningful)",
            "Trap detection (Honey/Margin/Dependency/Incumbency)",
            "Profile transition planning",

            # BBB Stakeholder Mapping
            "Stakeholder identification and mapping",
            "Role classification (Buyer/Beneficiary/Backer)",
            "Influence and concern analysis",
            "Engagement strategy per role",

            # Right Clients
            "Client-company culture fit analysis",
            "Strategic alignment scoring",
            "Growth potential assessment",
            "Mutual success probability"
        ],
        "client_profiles": {
            "new": {
                "trap": "Honey Trap (time wasters)",
                "goal": "Move to Transactional or Repeatable"
            },
            "transactional": {
                "trap": "Margin Trap (price race)",
                "goal": "Move to Repeatable"
            },
            "repeatable": {
                "trap": "Dependency Trap (complacency)",
                "goal": "Move to Meaningful"
            },
            "meaningful": {
                "trap": "Incumbency Trap (declining innovation)",
                "goal": "Maintain and deepen"
            }
        },
        "stakeholder_types": {
            "buyer": "Budget owner, final decision maker",
            "beneficiary": "Direct user/benefit recipient",
            "backer": "Implementation support, integration"
        },
        "tools": [
            "research_tool",
            "competitive_intel_tool",
            "fog_analysis_tool"
        ],
        "data_buckets": ["client", "deal", "company"],
        "cost_tier": "standard",
        "why_agent": "Complex analysis: Multi-dimensional client assessment, relationship dynamics, future potential",
        "consolidation_rationale": "All three focus on CLIENT UNDERSTANDING from different angles"
    },

    "deal_assessment_agent": {
        "name": "Deal Assessment Agent",
        "model": "GPT-4o",
        "role": "CONSOLIDATED: Right Deals + Find Money + Risk Assessment",
        "right_model_components": [
            "9. Right Deals"
        ],
        "right_tools_components": [
            "7. Find the Money"
        ],
        "capabilities": [
            # Right Deals
            "Deal classification (Bedrock/Stepping Stone/Stray)",
            "Strategic fit assessment",
            "Multi-solution opportunity identification",
            "Transformational potential scoring",

            # Find Money
            "Budget existence validation",
            "Budget owner identification",
            "Priority assessment",
            "Problem-budget linkage",
            "Deal viability prediction",

            # Risk Assessment
            "Anomaly detection",
            "Deal risk scoring",
            "Contract review",
            "Compliance checking"
        ],
        "budget_validation": {
            "rule": "No Budget = No Deal (typically)",
            "indicators": [
                "Strategic imperative alignment",
                "Budget owner identified",
                "Priority level defined",
                "Problem clearly articulated",
                "Timeline established"
            ]
        },
        "deal_types": {
            "bedrock": "Multi-solution, transformational, high investment",
            "stepping_stone": "Path to bedrock, relationship building",
            "stray": "One-off, misaligned, avoid"
        },
        "tools": [
            "research_tool",
            "competitive_intel_tool",
            "find_money_validator_tool"
        ],
        "data_buckets": ["deal", "client", "company"],
        "cost_tier": "standard",
        "why_agent": "Judgment-heavy: Deal qualification requires nuanced assessment of strategic fit, budget reality, risk",
        "consolidation_rationale": "All three answer: 'Should we pursue this deal?'"
    },

    "team_orchestration_agent": {
        "name": "Team Orchestration Agent",
        "model": "GPT-4o",
        "role": "CONSOLIDATED: Team Plan + Right Team Selection",
        "right_model_components": [
            "3. Team Plan",
            "8. Right Team"
        ],
        "capabilities": [
            # Team Plan
            "Role delineation (delivery vs pursuit)",
            "Cross-functional collaboration design",
            "Stakeholder engagement strategy",
            "Communication workflow planning",

            # Right Team
            "Skill-gap analysis",
            "Subject matter expert identification",
            "Team composition optimization",
            "Diversity and perspective balancing",
            "Past performance analysis"
        ],
        "tools": [
            "research_tool",
            "license_to_sell_tool"
        ],
        "data_buckets": ["company", "deal"],
        "cost_tier": "standard",
        "why_agent": "Complex optimization: Multi-constraint team assembly, skill matching, collaboration dynamics",
        "consolidation_rationale": "Both focus on PEOPLE & TEAM DYNAMICS for deal success"
    },

    "realtime_coach_agent": {
        "name": "Real-time Meeting Coach Agent",
        "model": "GPT-4o + Whisper",
        "role": "OPTIONAL: Live meeting coaching aligned with ImpactWon",
        "capabilities": [
            "Live transcription (Whisper)",
            "FOG analysis during conversation",
            "Stakeholder identification (BBB) in real-time",
            "4Cs opportunity spotting",
            "Suggestion generation",
            "Action item extraction"
        ],
        "supports": [
            "Credibility (Trust building in real-time)",
            "FOG Model (real-time fact validation)",
            "BBB identification"
        ],
        "tools": [
            "speech_to_text",
            "fog_analysis_tool"
        ],
        "data_buckets": ["deal", "client"],
        "cost_tier": "premium",
        "latency_requirement": "<2s (real-time)",
        "optional": True,
        "why_agent": "Real-time reasoning: Low-latency decision making, context-aware coaching",
        "deployment_note": "Deploy only if real-time coaching is critical to business value"
    }
}
```

---

### 2.2 MCP Tools & Functions (NOT Agents)

```python
# These were AGENTS in v2.0, now TOOLS in v2.1
# Rationale: Stateless, deterministic, no complex reasoning

MCP_TOOLS = {

    #========================================================================
    # MCP SERVERS (External services via Model Context Protocol)
    #========================================================================

    "research_tool": {
        "type": "mcp_server",
        "description": "Multi-source research and data aggregation",
        "capabilities": [
            "web_search",
            "news_aggregation",
            "social_media_monitoring",
            "company_database_lookup",
            "financial_data_api",
            "patent_search"
        ],
        "providers": [
            "Bing Search API",
            "NewsAPI",
            "Twitter/LinkedIn APIs",
            "Clearbit/ZoomInfo",
            "Yahoo Finance / Bloomberg API"
        ],
        "cost_tier": "variable",
        "was_agent_in_v20": "research_agent",
        "why_tool": "Stateless data retrieval, no reasoning required"
    },

    "content_generation_tool": {
        "type": "mcp_server",
        "description": "Template-based content generation",
        "capabilities": [
            "email_template_personalization",
            "proposal_generation",
            "presentation_creation",
            "follow_up_automation"
        ],
        "templates": {
            "email_templates": "Pre-defined with variable substitution",
            "proposal_templates": "Modular sections based on deal type",
            "presentation_templates": "Aligned with ImpactWon 4Cs"
        },
        "cost_tier": "low",
        "was_agent_in_v20": "content_agent",
        "why_tool": "Template-based, deterministic, no complex decisions"
    },

    "competitive_intel_tool": {
        "type": "mcp_server",
        "description": "Competitor tracking and intelligence gathering",
        "capabilities": [
            "competitor_tracking",
            "product_comparison_matrix",
            "pricing_intelligence",
            "win_loss_analysis",
            "market_positioning_data"
        ],
        "data_sources": [
            "Competitor websites",
            "Product review sites",
            "Patent databases",
            "Industry reports (Gartner, Forrester)"
        ],
        "cost_tier": "variable",
        "was_agent_in_v20": "competitive_intel_agent",
        "why_tool": "Data aggregation and comparison, minimal reasoning"
    },

    #========================================================================
    # FUNCTION TOOLS (Lightweight algorithms)
    #========================================================================

    "fog_analysis_tool": {
        "type": "function",
        "description": "Classify statements as Fact, Opinion, or Gossip",
        "right_tools_component": "2. FOG Model",
        "algorithm": {
            "fact": "Verifiable, objective, evidence-based",
            "opinion": "Subjective view, belief, interpretation",
            "gossip": "Unverified rumor, hearsay, speculation"
        },
        "implementation": "Rule-based classifier + small LLM (GPT-3.5 or fine-tuned Llama)",
        "cost_tier": "very_low",
        "was_agent_in_v20": "fog_analysis_agent",
        "why_tool": "Simple classification task, no multi-step reasoning"
    },

    "engagement_excellence_tool": {
        "type": "function",
        "description": "Apply 6 lenses of client relevance assessment",
        "right_tools_component": "3. Engagement Excellence",
        "six_lenses": [
            "Executive",
            "Client Experts (Sales)",
            "Solution Masters",
            "Tailored Outcomes",
            "Emerging Needs",
            "Strategic Imperatives"
        ],
        "output": "Scoring matrix across 6 lenses",
        "implementation": "Scoring algorithm with predefined criteria",
        "cost_tier": "low",
        "was_agent_in_v20": "engagement_excellence_agent",
        "why_tool": "Structured scoring against known criteria, deterministic"
    },

    "impact_theme_generator_tool": {
        "type": "function",
        "description": "Generate unique value propositions (ALL to ONLY)",
        "right_tools_component": "8. Client Value / Impact Themes",
        "input": "4Cs Control score (Mastery × Influence)",
        "output": "2-3 impact themes highlighting strategic differentiation",
        "algorithm": "Extract high-scoring Control factors → map to strategic imperatives → generate themes",
        "implementation": "Template-based generation + LLM for language polish",
        "cost_tier": "low",
        "was_agent_in_v20": "impact_theme_agent",
        "why_tool": "Derived output from 4Cs, template-driven"
    },

    "license_to_sell_tool": {
        "type": "function",
        "description": "Assess Client Expert competencies and skills",
        "right_tools_component": "5. Licence to Sell",
        "attributes": ["Brand Advocate", "Investigator", "Team Player"],
        "skills": [
            "Leadership and Ethics",
            "Business Acumen",
            "Sales and Sales Planning",
            "Products and Services"
        ],
        "formula": "Skills × Attributes = 4Cs Success Probability",
        "implementation": "Competency matrix scoring",
        "cost_tier": "very_low",
        "was_agent_in_v20": "license_to_sell_agent",
        "why_tool": "Structured assessment, scoring algorithm"
    },

    "find_money_validator_tool": {
        "type": "function",
        "description": "Validate budget existence and deal viability",
        "right_tools_component": "7. Find the Money",
        "rule": "No Budget = No Deal (typically)",
        "validation_checks": [
            "Is there a budget allocated?",
            "Who is the budget owner?",
            "What is the priority level?",
            "Is the problem clearly articulated?",
            "Is there a timeline?"
        ],
        "output": "Boolean viability + confidence score",
        "implementation": "Rule-based validator with data lookup",
        "cost_tier": "very_low",
        "was_agent_in_v20": "find_money_agent",
        "why_tool": "Binary checks and validation rules, no complex reasoning"
    }
}
```

---

### 2.3 Agent vs Tool Decision Matrix

**When to use an AGENT:**
- ✅ Requires multi-step reasoning
- ✅ Handles ambiguity and uncertainty
- ✅ Makes strategic decisions
- ✅ Maintains state across interactions
- ✅ Plans and adjusts dynamically
- ✅ Combines multiple information sources with judgment

**When to use a TOOL (MCP or Function):**
- ✅ Stateless data retrieval
- ✅ Deterministic transformation
- ✅ Template-based generation
- ✅ Simple classification/scoring
- ✅ Rule-based validation
- ✅ API wrapper or data connector

**Examples from this Architecture:**

| Functionality | v2.0 (Agent) | v2.1 (Tool) | Rationale |
|---------------|--------------|-------------|-----------|
| Web Search | research_agent | research_tool (MCP) | Stateless data retrieval |
| Email Templates | content_agent | content_generation_tool | Template-based, no reasoning |
| FOG Classification | fog_analysis_agent | fog_analysis_tool (function) | Simple classifier |
| Budget Validation | find_money_agent | find_money_validator_tool | Rule-based checks |
| Competitive Intel | competitive_intel_agent | competitive_intel_tool (MCP) | Data aggregation |

| Functionality | Still Agent | Why |
|---------------|-------------|-----|
| 4Cs Calculation | power_plan_agent | Multi-factor reasoning, initiative generation, temporal analysis |
| Strategic Planning | strategic_planning_agent | Long-term planning, ambiguity, stakeholder alignment |
| Client Profiling | client_intelligence_agent | Nuanced relationship assessment, trap detection |
| Deal Qualification | deal_assessment_agent | Judgment-heavy, strategic fit evaluation |

---

## 3. Optimized Workflows

### 3.1 Right to Win Assessment Workflow (Using Optimized Architecture)

```python
async def calculate_right_to_win_workflow_optimized(deal_id: str):
    """
    Optimized: Uses 2 agents + 3 tools (vs 5 agents in v2.0)
    """

    orchestrator = AgentOrchestrator()

    plan = {
        "workflow": "Right to Win Assessment (Optimized)",
        "deal_id": deal_id,
        "steps": [
            {
                "step_id": 1,
                "name": "Data Gathering",
                "type": "tool_call",
                "tool": "research_tool",  # MCP Server (was research_agent)
                "task": f"Gather comprehensive intelligence on deal {deal_id}",
                "data_buckets": ["deal", "client", "company", "industry"]
            },
            {
                "step_id": 2,
                "name": "4Cs Calculation",
                "type": "agent_call",
                "agent": "power_plan_agent",  # AGENT
                "task": "Calculate all 4Cs scores with detailed breakdowns",
                "depends_on": [1],
                "tools_available": [
                    "fog_analysis_tool",  # Function (was fog_analysis_agent)
                    "impact_theme_generator_tool"  # Function (was impact_theme_agent)
                ]
            },
            {
                "step_id": 3,
                "name": "Generate Power Plan Report",
                "type": "tool_call",
                "tool": "content_generation_tool",  # MCP Server (was content_agent)
                "task": "Create comprehensive Power Plan report",
                "depends_on": [2],
                "template": "power_plan_report_template"
            }
        ]
    }

    results = await orchestrator.execute_plan(plan)

    return {
        "deal_id": deal_id,
        "right_to_win_score": results[2]["overall_score"],
        "4cs_breakdown": results[2]["4cs_detail"],
        "initiatives": results[2]["initiatives"],
        "power_plan_report": results[3]["report_url"]
    }

# COMPARISON:
# v2.0: 5 agent calls (research_agent, right_to_win_agent, power_plan_agent,
#                      fog_analysis_agent, content_agent)
# v2.1: 2 agent calls + 3 tool calls
# Cost reduction: ~60%, Latency improvement: ~50%
```

---

## 4. Technical Stack (Updated)

### 4.1 Core Technology Choices

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Frontend** | React/Next.js | Modern, SSR/SSG capable, strong ecosystem |
| **Mobile** | React Native | Code reuse with web, single team |
| **Agent Framework** | LangGraph + LangChain | State machine for workflows, LLM orchestration |
| **MCP Implementation** | Anthropic MCP SDK | Standard for tool integration |
| **API Gateway** | Azure API Management | Enterprise-grade, Azure-native |
| **Orchestration** | Azure Container Apps | Serverless containers, auto-scaling |
| **LLM Providers** | GPT-4o, Claude Opus/Sonnet, Gemini Pro | Multi-model for cost/performance optimization |
| **Vector DB** | Azure AI Search (Milvus alternative) | Managed, Azure-native, hybrid search |
| **Graph DB** | Neo4j on Azure | ImpactWon relationship modeling |
| **Cache** | Azure Redis | Semantic caching + session management |
| **Observability** | LangFuse + Application Insights | LLM-specific metrics + Azure monitoring |

### 4.2 Why NOT Salesforce in UI Layer?

**Original Design (v2.0):**
```
UI Layer: Web Portal + Mobile App + Salesforce Integration (Standard Components)
```

**Problem:**
1. **Redundancy**: Already have Web + Mobile → why add Salesforce UI?
2. **Complexity**: Salesforce Standard Components require APEX/Visualforce development
3. **Cost**: Salesforce licenses for UI embedding are expensive ($150-300/user/month)
4. **User Experience**: Better UX in custom React app vs embedded Salesforce
5. **Maintenance**: Three UI codebases vs two

**Optimized Approach:**
- **UI Layer**: Web Portal (React) + Mobile App (React Native) ONLY
- **Data Integration**: Salesforce REST API for data sync (in Data Ingestion Layer)
- **Benefit**: Single codebase (React web + React Native mobile), no Salesforce UI licensing

```yaml
CRM_Integration_Strategy:
  UI_Layer:
    - Web Portal (React/Next.js)
    - Mobile App (React Native)
    - NO Salesforce UI components

  Data_Layer:
    - Salesforce REST API (bidirectional sync)
    - HubSpot API (if applicable)
    - Sync: deals, contacts, activities, opportunities
    - Frequency: Real-time (webhooks) + nightly batch

  Cost_Savings:
    - No Salesforce Platform licenses: Save $150-300/user/month
    - Single UI codebase: Reduce dev/maintenance by 30%
```

---

## 5. Cost Analysis - Optimized

### 5.1 Agent Cost Comparison (v2.0 vs v2.1)

**Assumptions:**
- 100 sales users
- 10 Right to Win assessments per user per week
- Average 20K tokens per assessment

| Version | Agent Count | Monthly LLM Cost | Other Infra | Total Monthly |
|---------|-------------|------------------|-------------|---------------|
| **v2.0 (Original)** | 21 agents | $12,000 | $3,000 | **$15,000** |
| **v2.1 (Optimized)** | 6-7 agents | $4,500 | $2,000 | **$6,500** |
| **Savings** | 70% reduction | **$7,500** | **$1,000** | **$8,500 (57%)** |

### 5.2 Detailed Cost Breakdown (v2.1)

```yaml
Monthly_Operational_Cost_v21:

  LLM_API_Costs:
    GPT-4o:
      usage: "60% of requests (primary)"
      cost: "$2,500/month"

    Claude_Opus:
      usage: "10% (critical strategic planning)"
      cost: "$1,000/month"

    Claude_Sonnet:
      usage: "25% (research-heavy tasks)"
      cost: "$800/month"

    Gemini_Pro:
      usage: "5% (multimodal)"
      cost: "$200/month"

    Total_LLM: "$4,500/month"

  Azure_Infrastructure:
    Container_Apps: "$600/month (auto-scaling)"
    Redis_Cache: "$300/month"
    Cosmos_DB: "$400/month"
    Azure_SQL: "$200/month"
    Neo4j_Graph: "$400/month"
    API_Management: "$100/month"
    Total_Infra: "$2,000/month"

  Data_&_Integrations:
    News_APIs: "$200/month"
    Social_Media_APIs: "$150/month"
    Company_Data_APIs: "$300/month (Clearbit, ZoomInfo)"
    Total_Data: "$650/month"

  Total_Monthly: "$7,150/month"

  Annual_Cost: "$85,800/year"

  Cost_Per_User: "$71.50/month (100 users)"
```

### 5.3 Cost Optimization Strategies

1. **Semantic Caching** (30-40% token reduction)
   - Cache similar queries in Redis + vector similarity
   - Expected savings: ~$1,500/month

2. **Model Routing** (15-20% cost reduction)
   - Route simple tasks to GPT-3.5 or fine-tuned Llama
   - Use GPT-4o/Claude Opus only for complex reasoning
   - Expected savings: ~$900/month

3. **Batch Processing** (10-15% savings)
   - Batch non-urgent research tasks
   - Off-peak processing for reports
   - Expected savings: ~$500/month

**Optimized Monthly Cost (with strategies):** ~$4,250/month ($51K/year)

---

## 6. Implementation Roadmap

### Phase 1: Foundation (Months 1-2)
- ✅ Set up Azure infrastructure (Container Apps, Redis, Cosmos DB)
- ✅ Implement Supervisor Agent + LangGraph orchestration
- ✅ Build MCP tool infrastructure (research, content gen, competitive intel)
- ✅ Develop Power Plan Agent (THE critical 4Cs engine)
- ✅ Create Web Portal (React/Next.js) with basic UI

### Phase 2: Core Agents (Months 3-4)
- ✅ Implement Strategic Planning Agent (CEO Plan + Attainment + Pursuit)
- ✅ Implement Client Intelligence Agent (Profiling + BBB + Right Clients)
- ✅ Implement Deal Assessment Agent (Right Deals + Find Money + Risk)
- ✅ Build Knowledge Graph (Neo4j) with ImpactWon entities
- ✅ Integrate MCP function tools (FOG, Engagement Excellence, etc.)

### Phase 3: Team & Mobile (Months 5-6)
- ✅ Implement Team Orchestration Agent
- ✅ Build Mobile App (React Native)
- ✅ Integrate CRM data sync (Salesforce/HubSpot REST APIs - data only, no UI)
- ✅ Implement semantic caching for cost optimization

### Phase 4: Advanced Features (Months 7-8)
- ✅ [Optional] Real-time Coach Agent with Whisper integration
- ✅ Advanced analytics and dashboards
- ✅ Model routing and cost optimization
- ✅ Security hardening and compliance (SOC 2, GDPR)

### Phase 5: Scale & Optimize (Months 9-12)
- ✅ Performance tuning (target: P95 latency <1.5s)
- ✅ A/B testing for prompt optimization
- ✅ User training and adoption programs
- ✅ Continuous monitoring and improvement

---

## 7. Success Metrics (12-Month Target)

```yaml
Adoption_Metrics:
  - Daily Active Users: ">85% of sales team"
  - Right to Win Assessments per week: "10-15"
  - Power Plan updates per deal: "Daily"
  - NPS Score: ">70"

ImpactWon_Business_Outcomes:
  - Average Right to Win score: "+25 points"
  - Deals with 4Cs >75%: "60% of pipeline"
  - CEO-level access (Credibility): "+40%"
  - Regional references (Capability): "+50%"
  - Active buying clients (Commitment): "+35%"
  - Deals with 'our fingerprints' (Control): "+45%"

Technical_Performance:
  - System uptime: "99.95%"
  - Average response time: "<1.5s (P95)"
  - 4Cs calculation accuracy: ">95%"
  - Data freshness: "<15 minutes"
  - Monthly cost per user: "<$50"

Optimization_Achievements:
  - Agent count reduction: "70% (21 → 6-7)"
  - Cost reduction: "57% vs v2.0"
  - Latency improvement: "50% faster"
  - Code complexity: "-40%"
```

---

## 8. Key Architectural Decisions

### 8.1 Lean Agents + Rich Tools Philosophy

**Decision:** Reduce from 21 agents to 6-7 agents, move 15 capabilities to MCP tools/functions

**Rationale:**
- Agents are expensive (LLM calls, state management, orchestration overhead)
- Many "agents" in v2.0 were simple data retrievers or template generators
- Tools are cheaper, faster, and easier to maintain
- Focus agent capabilities on complex reasoning, planning, and decision-making

**Trade-offs:**
- Pro: 57% cost savings, 50% latency reduction, simpler debugging
- Con: Less "agentic" for simple tasks (but those don't need agents anyway)

### 8.2 Remove Salesforce UI Integration

**Decision:** Remove Salesforce from UI layer, keep as data integration only

**Rationale:**
- Already building Web + Mobile → Salesforce UI is redundant
- Salesforce UI embedding requires expensive platform licenses
- Better UX in custom React app
- Single codebase (React web + React Native mobile)

**Trade-offs:**
- Pro: Save $15K-30K/month in Salesforce licenses, better UX, simpler codebase
- Con: Users need to switch between SCIP app and Salesforce (mitigated by data sync)

### 8.3 Multi-Model Strategy

**Decision:** Use GPT-4o (primary), Claude Opus (critical), Claude Sonnet (research), Gemini Pro (multimodal)

**Rationale:**
- No single LLM is best for all tasks
- Cost optimization: Use cheaper models for simple tasks
- Resilience: Fallback if one provider has issues
- Performance: Match model strengths to agent needs

**Trade-offs:**
- Pro: 20-30% cost savings, better performance per task, redundancy
- Con: More complexity in model routing logic

---

## 9. Summary of Optimizations

| Aspect | v2.0 (Original) | v2.1 (Optimized) | Impact |
|--------|-----------------|------------------|--------|
| **Agent Count** | 21 | 6-7 | 70% reduction |
| **Agent Architecture** | Agent-heavy | Lean agents + MCP tools | Simplified |
| **UI Layer** | Web + Mobile + Salesforce | Web + Mobile only | Cost savings |
| **CRM Integration** | Salesforce UI components | Data sync via REST API | No UI licenses |
| **Monthly Cost** | ~$15K | ~$6.5K (with optimization: $4.3K) | 57-71% savings |
| **Latency (P95)** | 3-5s | 1-2s | 50-60% faster |
| **Code Complexity** | High (21 agents) | Moderate (6-7 agents) | Easier maintenance |
| **Debuggability** | Difficult (agent spaghetti) | Moderate (clear agent boundaries) | Improved |

---

## 10. Recommendations

### Immediate Actions

1. **Accept Optimized Architecture**
   - Approve 6-7 agent design vs 21 agents
   - Approve MCP tool migration for 15 capabilities
   - Approve Salesforce UI removal

2. **Prioritize Power Plan Agent**
   - This is THE critical agent (4Cs calculation)
   - Invest 30% of development time here
   - Ensure 99.9% uptime and <1s latency

3. **Build Web Portal First, Mobile Later**
   - Web portal has higher ROI (sales teams use desktops)
   - Mobile can wait until Phase 3

4. **Implement Cost Optimization Early**
   - Semantic caching from Day 1
   - Model routing by Phase 2
   - Target: <$50/user/month

### Long-term Strategy

1. **Continuous Agent Consolidation**
   - Monitor which agents could be further consolidated
   - Consider fine-tuning smaller models to replace agents with tools

2. **User Adoption Focus**
   - Best tech is useless without adoption
   - Invest in training, onboarding, UI/UX

3. **ImpactWon Methodology Validation**
   - Measure: Does 4Cs scoring actually predict wins?
   - Adjust scoring methodology based on data

---

## Appendix A: Agent Migration Map (v2.0 → v2.1)

| v2.0 Agent | v2.1 Status | New Home | Rationale |
|------------|-------------|----------|-----------|
| supervisor | ✅ Kept as Agent | supervisor | Orchestration requires reasoning |
| ceo_sales_plan_agent | 🔀 Consolidated | strategic_planning_agent | Sequential planning phases |
| attainment_plan_agent | 🔀 Consolidated | strategic_planning_agent | Sequential planning phases |
| team_plan_agent | 🔀 Consolidated | team_orchestration_agent | Team dynamics |
| remuneration_agent | ❌ Removed | N/A | Out of scope for MVP |
| pursuit_plan_agent | 🔀 Consolidated | strategic_planning_agent | Sequential planning phases |
| power_plan_agent | ✅ Kept as Agent | power_plan_agent | THE critical 4Cs engine |
| right_clients_agent | 🔀 Consolidated | client_intelligence_agent | Client understanding |
| right_team_agent | 🔀 Consolidated | team_orchestration_agent | Team dynamics |
| right_deals_agent | 🔀 Consolidated | deal_assessment_agent | Deal qualification |
| right_to_win_agent | 🔀 Merged | power_plan_agent | Duplicate of power_plan |
| fog_analysis_agent | ⚙️ Tool | fog_analysis_tool | Simple classifier |
| engagement_excellence_agent | ⚙️ Tool | engagement_excellence_tool | Scoring algorithm |
| client_profiling_agent | 🔀 Consolidated | client_intelligence_agent | Client understanding |
| license_to_sell_agent | ⚙️ Tool | license_to_sell_tool | Competency scoring |
| bbb_stakeholder_agent | 🔀 Consolidated | client_intelligence_agent | Stakeholder mapping |
| find_money_agent | ⚙️ Tool | find_money_validator_tool | Rule-based validation |
| impact_theme_agent | ⚙️ Tool | impact_theme_generator_tool | Template-driven |
| research_agent | ⚙️ MCP Tool | research_tool | Data retrieval |
| content_agent | ⚙️ MCP Tool | content_generation_tool | Template-based |
| risk_agent | 🔀 Consolidated | deal_assessment_agent | Deal risk assessment |
| competitive_intel_agent | ⚙️ MCP Tool | competitive_intel_tool | Data aggregation |
| meeting_coach_agent | ✅ Optional Agent | realtime_coach_agent | Real-time reasoning |

**Legend:**
- ✅ Kept as Agent
- 🔀 Consolidated into another agent
- ⚙️ Converted to Tool (MCP or Function)
- ❌ Removed

---

## Appendix B: Comparison Diagram

```
v2.0 (Original)                    v2.1 (Optimized)
┌──────────────────┐              ┌──────────────────┐
│   21 AGENTS      │              │   6-7 AGENTS     │
│                  │              │                  │
│ • Supervisor     │              │ • Supervisor     │
│ • CEO Sales Plan │─┐            │ • Power Plan (4Cs)│
│ • Attainment     │─┤            │ • Strategic Planning│
│ • Pursuit        │─┘─→          │   (consolidates 3)│
│ • Power Plan     │              │ • Client Intelligence│
│ • Right to Win   │─→ merged     │   (consolidates 3)│
│ • Team Plan      │─┐            │ • Deal Assessment│
│ • Right Team     │─┘─→          │   (consolidates 3)│
│ • Right Clients  │─┐            │ • Team Orchestration│
│ • Client Profiling│─┤           │   (consolidates 2)│
│ • BBB Stakeholder│─┘─→          │ [Optional]       │
│ • Right Deals    │─┐            │ • Realtime Coach │
│ • Find Money     │─┤            └──────────────────┘
│ • Risk           │─┘─→
│ • Research       │─┐            ┌──────────────────┐
│ • Content        │─┤            │   MCP TOOLS      │
│ • Competitive Int│─┤            │                  │
│ • FOG Analysis   │─┤            │ • research_tool  │
│ • Engagement Exc │─┤            │ • content_gen_tool│
│ • Impact Theme   │─┤            │ • competitive_intel│
│ • License to Sell│─┤            │                  │
│ • Meeting Coach  │─┘─→          │   FUNCTIONS      │
└──────────────────┘              │ • fog_analysis   │
                                  │ • engagement_exc │
Cost: $15K/month                  │ • impact_theme   │
Latency: 3-5s                     │ • license_to_sell│
                                  │ • find_money     │
                                  └──────────────────┘

                                  Cost: $6.5K/month
                                  Latency: 1-2s
```

---

**End of Optimized Technical Design v2.1**

**Next Steps:**
1. Review and approve optimizations
2. Begin Phase 1 implementation (Foundation)
3. Set up Azure infrastructure
4. Build Supervisor + Power Plan Agent first
