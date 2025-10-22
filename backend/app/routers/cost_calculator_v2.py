from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum
router = APIRouter()

# Pricing configuration is now embedded in this file

# ===========================
# AI AGENT DEFINITIONS
# ===========================

AI_AGENTS = {
    "sales-coach": {
        "name": "Sales Coach in the Pocket (SCIP) - OPTIMIZED v2.1",
        "description": "Lean 9-agent architecture following ImpactWon methodology for 4Cs assessment + Next-Best-Move generation. Optimized from 21 agents, 57% cost savings vs v2.0",
        "agents_count": 9,
        "agents": [
            "Supervisor Agent",
            "Power Plan Agent (4Cs) - CRITICAL",
            "Strategic Planning Agent (CEO+Attainment+Pursuit)",
            "Client Intelligence Agent (Profiling+BBB+Right Clients)",
            "Deal Assessment Agent (Right Deals+Find Money+Risk)",
            "Team Orchestration Agent (Team Plan+Right Team)",
            "Persona-Coach Agent (NBM) - CRITICAL",
            "Feedback Agent",
            "Real-time Coach Agent (OPTIONAL)"
        ],
        "mcp_tools": [
            "research_tool (MCP Server)",
            "content_generation_tool (MCP Server)",
            "competitive_intel_tool (MCP Server)",
            "fog_analysis_tool (Function)",
            "engagement_excellence_tool (Function)",
            "impact_theme_generator_tool (Function)",
            "license_to_sell_tool (Function)",
            "find_money_validator_tool (Function)"
        ],
        "data_buckets": 4,
        "data_sources": [
            "ZoomInfo (Premium)",
            "LinkedIn Sales Navigator (Premium)",
            "Clearbit (Premium)",
            "HubSpot/Salesforce CRM (Data Sync only, no UI)",
            "News APIs",
            "Social Media APIs"
        ],
        "complexity": "medium",  # Reduced from "high" due to optimization
        "base_infrastructure": {
            "aks_nodes": 8,  # Reduced from 12 (fewer agents)
            "gpu_nodes": 0,  # No local LLM hosting, using API-based models
            "sql_vcores": 12,  # Reduced from 16
            "cosmos_ru": 45000,  # Reduced from 60000
            "neo4j_nodes": 2,  # Reduced from 3 (smaller graph)
            "storage_hot_tb": 15,  # Reduced from 25
            "storage_cool_tb": 120  # Reduced from 200
        }
    },
    "qa-agent": {
        "name": "QA AI Agent",
        "description": "Automated QA test generation, execution, and healing with multi-agent architecture",
        "agents_count": 5,
        "agents": ["Perception", "Planner", "Generator", "Execution", "Healer"],
        "data_buckets": 2,
        "data_sources": ["Confluence", "GitHub", "Test Results DB"],
        "complexity": "medium",
        "base_infrastructure": {
            "aks_nodes": 8,
            "gpu_nodes": 2,
            "sql_vcores": 8,
            "cosmos_ru": 30000,
            "neo4j_nodes": 1,
            "storage_hot_tb": 10,
            "storage_cool_tb": 50
        }
    },
    "rfp-evaluator": {
        "name": "RFP Evaluator AI Agent",
        "description": "Automated RFP/RFI evaluation with document analysis, scoring, and recommendation engine",
        "agents_count": 6,
        "agents": ["Document Parser", "Requirements Extractor", "Vendor Analyzer", "Scorer", "Comparator", "Report Generator"],
        "data_buckets": 3,
        "data_sources": ["Document Storage", "Vendor DB", "Historical RFPs"],
        "complexity": "medium-high",
        "base_infrastructure": {
            "aks_nodes": 10,
            "gpu_nodes": 3,
            "sql_vcores": 12,
            "cosmos_ru": 40000,
            "neo4j_nodes": 2,
            "storage_hot_tb": 15,
            "storage_cool_tb": 100
        }
    },
    "customer-support": {
        "name": "Customer Support AI Agent",
        "description": "Intelligent customer support with ticket routing, response generation, and knowledge base",
        "agents_count": 5,
        "agents": ["Ticket Classifier", "Intent Analyzer", "Response Generator", "Knowledge Retriever", "Escalation Manager"],
        "data_buckets": 3,
        "data_sources": ["Zendesk/ServiceNow", "Knowledge Base", "Customer DB"],
        "complexity": "medium",
        "base_infrastructure": {
            "aks_nodes": 10,
            "gpu_nodes": 2,
            "sql_vcores": 12,
            "cosmos_ru": 35000,
            "neo4j_nodes": 1,
            "storage_hot_tb": 12,
            "storage_cool_tb": 80
        }
    },
    "content-moderator": {
        "name": "Content Moderation AI Agent",
        "description": "AI-powered content moderation with real-time toxicity detection and classification",
        "agents_count": 4,
        "agents": ["Content Classifier", "Toxicity Detector", "Image Analyzer", "Decision Engine"],
        "data_buckets": 2,
        "data_sources": ["User Content DB", "Moderation Rules"],
        "complexity": "low-medium",
        "base_infrastructure": {
            "aks_nodes": 6,
            "gpu_nodes": 2,
            "sql_vcores": 8,
            "cosmos_ru": 25000,
            "neo4j_nodes": 1,
            "storage_hot_tb": 8,
            "storage_cool_tb": 40
        }
    }
}

# ===========================
# AZURE AUSTRALIA EAST (SYDNEY) PRICING - 2025
# All prices in AUD
# ===========================

AZURE_PRICING_SYDNEY = {
    "compute": {
        # VM Pricing (per hour) - Standard D-series v5
        "Standard_D4s_v5": {"payg": 0.288, "reserved_1yr": 0.173},  # 4 vCPU, 16 GB
        "Standard_D8s_v5": {"payg": 0.576, "reserved_1yr": 0.346},  # 8 vCPU, 32 GB
        "Standard_D16s_v5": {"payg": 1.152, "reserved_1yr": 0.691},  # 16 vCPU, 64 GB
        # GPU VM Pricing (per hour) - NC-series v3
        "Standard_NC6s_v3": {"payg": 4.20, "reserved_1yr": 2.52},  # 6 vCPU, 112 GB, 1x V100
        "Standard_NC12s_v3": {"payg": 8.40, "reserved_1yr": 5.04},  # 12 vCPU, 224 GB, 2x V100
    },
    "kubernetes": {
        "aks_management": 0.15,  # per cluster hour
        "load_balancer": 30.00,  # per month
    },
    "storage": {
        "adls_gen2_hot": 0.025,  # per GB/month
        "adls_gen2_cool": 0.015,  # per GB/month
        "blob_storage_hot": 0.0234,  # per GB/month
        "blob_storage_cool": 0.0128,  # per GB/month
    },
    "database": {
        # Azure SQL Database - vCore model (per vCore per hour)
        "sql_gen5_vcore": 0.5865,  # General Purpose, Gen5
        # Cosmos DB (per 100 RU/s per hour)
        "cosmosdb_ru_100": 0.012,  # Standard throughput
        # Redis Cache (per hour)
        "redis_c6": 0.765,  # 6 GB cache
    },
    "networking": {
        "api_management_developer": 56.00,  # per month
        "api_management_standard": 785.00,  # per month
        "application_gateway_v2": 0.315,  # per hour
        "front_door_standard": 35.00,  # per month (base)
        "firewall": 1.575,  # per hour
    },
    "monitoring": {
        "log_analytics_gb": 3.50,  # per GB ingested
        "application_insights_gb": 3.25,  # per GB
    },
    "functions": {
        "premium_ep1": 0.252,  # per hour
    },
    "databricks": {
        "all_purpose_dbu": 0.75,  # per DBU hour
    }
}

# LLM Pricing (USD per 1M tokens) - January 2025 Pricing
# Sources: OpenAI API pricing, Anthropic API pricing, Google Gemini pricing
# Note: Claude is NOT available on Azure, using Anthropic API pricing
LLM_PRICING_USD = {
    "gpt-4o": {
        "input": 2.50,  # per 1M input tokens (Azure OpenAI)
        "output": 10.00,  # per 1M output tokens
        "cache_read": 1.25,  # 50% discount for prompt caching
        "provider": "Azure OpenAI",
        "context_window": 128000
    },
    "gpt-4-turbo": {
        "input": 10.00,
        "output": 30.00,
        "cache_read": 5.00,
        "provider": "Azure OpenAI",
        "context_window": 128000
    },
    "gpt-3.5-turbo": {
        "input": 0.50,  # Cheaper option for simple tasks
        "output": 1.50,
        "cache_read": 0.25,
        "provider": "Azure OpenAI",
        "context_window": 16000
    },
    "claude-3.5-sonnet": {  # Via Anthropic API (NOT on Azure)
        "input": 3.00,
        "output": 15.00,
        "cache_read": 0.30,  # 90% discount for prompt caching
        "provider": "Anthropic API",
        "context_window": 200000
    },
    "claude-3.5-opus": {  # Via Anthropic API (NOT on Azure)
        "input": 15.00,
        "output": 75.00,
        "cache_read": 1.50,  # 90% discount
        "provider": "Anthropic API",
        "context_window": 200000
    },
    "gemini-1.5-pro": {  # Google Gemini via API
        "input": 1.25,
        "output": 5.00,
        "cache_read": 0.625,  # 50% discount
        "provider": "Google AI API",
        "context_window": 2000000  # 2M context!
    },
    "llama-3.1-70b": {  # Self-hosted on Azure GPU (NOT recommended for SCIP)
        "input": 0.00,  # No API costs, just infrastructure
        "output": 0.00,
        "cache_read": 0.00,
        "infrastructure_monthly": 0,  # Included in GPU node cost (if used)
        "provider": "Self-hosted",
        "context_window": 128000,
        "note": "Not recommended for SCIP v2.1 - use API-based models"
    }
}

# Premium Data Source Pricing (USD per month) - January 2025
# Note: These are enterprise tier prices for 100 users
DATA_SOURCE_PRICING_USD = {
    "zoominfo": 15000,  # Enterprise tier (100 seats)
    "linkedin_sales_navigator": 9900,  # 100 seats @ $99/month/seat
    "clearbit": 12000,  # Enterprise tier with enrichment API
    "hubspot_enterprise": 0,  # Using data sync only (no additional UI cost)
    "salesforce_api": 0,  # Data sync via REST API (included in existing licenses)
    "news_apis": 200,  # NewsAPI + aggregators
    "social_media_apis": 150,  # Twitter/LinkedIn APIs
    "company_data_apis": 300,  # Crunchbase, PitchBook access
}

# Exchange Rate (AUD to USD)
AUD_TO_USD = 0.65

# ===========================
# MODELS
# ===========================

class CostCalculatorRequest(BaseModel):
    # AI Agent Selection
    agent_type: str = Field(default="sales-coach", description="Type of AI agent")

    # User Parameters
    num_users: int = Field(default=100, ge=1, le=10000)
    queries_per_user_per_month: int = Field(default=1000, ge=10, le=10000)  # Lowered from 100 to 10 for Sales Coach assessments
    avg_input_tokens: int = Field(default=10000, ge=1000, le=100000)
    avg_output_tokens: int = Field(default=1000, ge=100, le=10000)

    # Infrastructure Scaling Multiplier (1.0 = base, 2.0 = double)
    infrastructure_scale: float = Field(default=1.0, ge=0.5, le=5.0)

    # LLM Mix (percentages, should sum to 100)
    llm_mix: Dict[str, float] = Field(
        default={
            "gpt-4o": 60.0,
            "claude-3.5-sonnet": 30.0,
            "llama-3.1-70b": 10.0
        }
    )

    # Usage Patterns
    cache_hit_rate: float = Field(default=0.70, ge=0.0, le=0.99)
    use_prompt_caching: bool = Field(default=True)
    use_reserved_instances: bool = Field(default=True)

    # Memory System Selection (THIS ADDRESSES USER'S QUESTION)
    memory_type: str = Field(default="redis", description="Memory system: redis, cosmos_db, neo4j, in_memory")

    # MCP Tools Selection (THIS ADDRESSES USER'S QUESTION)
    selected_tools: List[str] = Field(
        default=[],
        description="List of selected MCP tool names (e.g., ['research_tool', 'fog_analysis_tool'])"
    )

    # Optional: Override infrastructure (if not provided, uses agent defaults)
    custom_infrastructure: Optional[Dict[str, int]] = None


class CostBreakdown(BaseModel):
    category: str
    subcategory: str
    monthly_cost: float
    annual_cost: float
    unit: str
    quantity: float
    notes: str


class AgentArchitecture(BaseModel):
    agent_type: str
    agent_name: str
    description: str
    agents_count: int
    agents_list: List[str]
    mcp_tools: Optional[List[str]] = []  # MCP tools and functions
    data_buckets: int
    data_sources: List[str]
    complexity: str
    infrastructure: Dict[str, float]


class CostCalculatorResponse(BaseModel):
    # Agent Information
    agent_architecture: AgentArchitecture

    # Summary
    total_monthly_cost: float
    total_annual_cost: float
    cost_per_user_monthly: float
    cost_per_user_annual: float
    cost_per_query: float

    # Fixed vs Variable
    fixed_monthly_cost: float
    variable_monthly_cost: float

    # Category Totals (in tabs)
    infrastructure_costs: float
    llm_costs: float
    data_source_costs: float
    monitoring_costs: float
    memory_system_costs: float  # NEW - addresses user's question
    mcp_tools_costs: float      # NEW - addresses user's question

    # Detailed Breakdown by Tab
    infrastructure_breakdown: List[CostBreakdown]
    llm_breakdown: List[CostBreakdown]
    data_source_breakdown: List[CostBreakdown]
    monitoring_breakdown: List[CostBreakdown]
    memory_system_breakdown: List[CostBreakdown]  # NEW
    mcp_tools_breakdown: List[CostBreakdown]      # NEW

    # Metrics
    queries_per_month: int
    input_tokens_per_month: int
    output_tokens_per_month: int
    estimated_data_size_gb: float

    # Cost Savings
    savings_from_caching: float
    savings_from_reserved_instances: float


# ===========================
# HELPER FUNCTIONS
# ===========================

def get_agent_infrastructure(agent_type: str, scale: float, custom: Optional[Dict] = None) -> Dict[str, float]:
    """Get infrastructure configuration for an agent, scaled appropriately"""
    if agent_type not in AI_AGENTS:
        raise HTTPException(status_code=400, detail=f"Unknown agent type: {agent_type}")

    base_infra = AI_AGENTS[agent_type]["base_infrastructure"]

    if custom:
        return {k: custom.get(k, v) for k, v in base_infra.items()}

    return {k: v * scale for k, v in base_infra.items()}


def calculate_infrastructure_costs(infra: Dict[str, float], use_reserved: bool) -> tuple[float, List[CostBreakdown]]:
    """Calculate all infrastructure costs"""
    breakdown = []
    total = 0.0

    # AKS Nodes
    vm_price = AZURE_PRICING_SYDNEY["compute"]["Standard_D8s_v5"]
    hourly_rate = vm_price["reserved_1yr"] if use_reserved else vm_price["payg"]
    monthly_cost = hourly_rate * 730 * infra["aks_nodes"]
    total += monthly_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="AKS Agent Nodes",
        monthly_cost=monthly_cost,
        annual_cost=monthly_cost * 12,
        unit="nodes",
        quantity=infra["aks_nodes"],
        notes=f"Standard_D8s_v5 × {int(infra['aks_nodes'])} ({'Reserved' if use_reserved else 'PAYG'})"
    ))

    # GPU Nodes
    if infra["gpu_nodes"] > 0:
        gpu_price = AZURE_PRICING_SYDNEY["compute"]["Standard_NC6s_v3"]
        hourly_rate = gpu_price["reserved_1yr"] if use_reserved else gpu_price["payg"]
        monthly_cost = hourly_rate * 730 * infra["gpu_nodes"]
        total += monthly_cost
        breakdown.append(CostBreakdown(
            category="Infrastructure",
            subcategory="GPU Nodes (Llama Hosting)",
            monthly_cost=monthly_cost,
            annual_cost=monthly_cost * 12,
            unit="nodes",
            quantity=infra["gpu_nodes"],
            notes=f"Standard_NC6s_v3 × {int(infra['gpu_nodes'])} with V100 GPUs"
        ))

    # AKS Management
    aks_mgmt = AZURE_PRICING_SYDNEY["kubernetes"]["aks_management"] * 730
    total += aks_mgmt
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="AKS Management",
        monthly_cost=aks_mgmt,
        annual_cost=aks_mgmt * 12,
        unit="cluster",
        quantity=1,
        notes="Kubernetes cluster management fee"
    ))

    # Storage - Hot Tier
    storage_hot = AZURE_PRICING_SYDNEY["storage"]["adls_gen2_hot"] * infra["storage_hot_tb"] * 1024
    total += storage_hot
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Storage (Hot Tier)",
        monthly_cost=storage_hot,
        annual_cost=storage_hot * 12,
        unit="TB",
        quantity=infra["storage_hot_tb"],
        notes="ADLS Gen2 Hot tier for active data"
    ))

    # Storage - Cool Tier
    storage_cool = AZURE_PRICING_SYDNEY["storage"]["adls_gen2_cool"] * infra["storage_cool_tb"] * 1024
    total += storage_cool
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Storage (Cool Tier)",
        monthly_cost=storage_cool,
        annual_cost=storage_cool * 12,
        unit="TB",
        quantity=infra["storage_cool_tb"],
        notes="ADLS Gen2 Cool tier for archival data"
    ))

    # Azure SQL Database
    sql_cost = AZURE_PRICING_SYDNEY["database"]["sql_gen5_vcore"] * infra["sql_vcores"] * 730
    total += sql_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Azure SQL Database",
        monthly_cost=sql_cost,
        annual_cost=sql_cost * 12,
        unit="vCores",
        quantity=infra["sql_vcores"],
        notes=f"General Purpose Gen5, {int(infra['sql_vcores'])} vCores"
    ))

    # Cosmos DB
    cosmos_cost = AZURE_PRICING_SYDNEY["database"]["cosmosdb_ru_100"] * (infra["cosmos_ru"] / 100) * 730
    total += cosmos_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Cosmos DB",
        monthly_cost=cosmos_cost,
        annual_cost=cosmos_cost * 12,
        unit="RU/s",
        quantity=infra["cosmos_ru"],
        notes=f"{int(infra['cosmos_ru']):,} RU/s provisioned throughput"
    ))

    # Neo4j (self-hosted on VMs)
    if infra["neo4j_nodes"] > 0:
        neo4j_vm = AZURE_PRICING_SYDNEY["compute"]["Standard_D16s_v5"]
        hourly_rate = neo4j_vm["reserved_1yr"] if use_reserved else neo4j_vm["payg"]
        neo4j_cost = hourly_rate * 730 * infra["neo4j_nodes"]
        total += neo4j_cost
        breakdown.append(CostBreakdown(
            category="Infrastructure",
            subcategory="Neo4j Graph Database",
            monthly_cost=neo4j_cost,
            annual_cost=neo4j_cost * 12,
            unit="nodes",
            quantity=infra["neo4j_nodes"],
            notes=f"Standard_D16s_v5 × {int(infra['neo4j_nodes'])} nodes"
        ))

    # Redis Cache
    redis_cost = AZURE_PRICING_SYDNEY["database"]["redis_c6"] * 730
    total += redis_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Redis Cache",
        monthly_cost=redis_cost,
        annual_cost=redis_cost * 12,
        unit="cache",
        quantity=1,
        notes="C6 (6GB) cache for session/response caching"
    ))

    # Networking
    apim_cost = AZURE_PRICING_SYDNEY["networking"]["api_management_standard"]
    total += apim_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="API Management",
        monthly_cost=apim_cost,
        annual_cost=apim_cost * 12,
        unit="gateway",
        quantity=1,
        notes="Standard tier API Gateway"
    ))

    front_door_cost = AZURE_PRICING_SYDNEY["networking"]["front_door_standard"]
    total += front_door_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Azure Front Door",
        monthly_cost=front_door_cost,
        annual_cost=front_door_cost * 12,
        unit="service",
        quantity=1,
        notes="Global load balancing and CDN"
    ))

    firewall_cost = AZURE_PRICING_SYDNEY["networking"]["firewall"] * 730
    total += firewall_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Azure Firewall",
        monthly_cost=firewall_cost,
        annual_cost=firewall_cost * 12,
        unit="firewall",
        quantity=1,
        notes="Network security and filtering"
    ))

    return total, breakdown


def calculate_llm_costs(
    num_users: int,
    queries_per_user: int,
    input_tokens: int,
    output_tokens: int,
    llm_mix: Dict[str, float],
    cache_hit_rate: float,
    use_caching: bool
) -> tuple[float, List[CostBreakdown], float]:
    """Calculate LLM API costs"""
    breakdown = []
    total = 0.0
    savings = 0.0

    total_queries = num_users * queries_per_user
    total_input_tokens = total_queries * input_tokens
    total_output_tokens = total_queries * output_tokens

    for model, percentage in llm_mix.items():
        if percentage == 0:
            continue

        model_queries = (percentage / 100.0) * total_queries
        model_input_tokens = (percentage / 100.0) * total_input_tokens
        model_output_tokens = (percentage / 100.0) * total_output_tokens

        # Get pricing from LLM_PRICING_USD
        if model not in LLM_PRICING_USD:
            continue
            
        llm_pricing = LLM_PRICING_USD[model]

        # Handle Llama (self-hosted)
        if "llama" in model.lower():
            # For Llama, infrastructure cost is included in GPU nodes
            monthly_cost = 0.0  # No additional LLM API cost
            breakdown.append(CostBreakdown(
                category="LLM",
                subcategory=f"{model} (Self-Hosted)",
                monthly_cost=monthly_cost,
                annual_cost=monthly_cost * 12,
                unit="infrastructure",
                quantity=percentage,
                notes=f"{percentage:.0f}% of queries, self-hosted on GPU nodes"
            ))
            continue

        # Get pricing (USD per 1M tokens)
        input_price = llm_pricing.get('input', 0.0)
        output_price = llm_pricing.get('output', 0.0)
        cache_price = llm_pricing.get('cache_read', 0.0)

        # Calculate with caching
        if use_caching and cache_hit_rate > 0:
            # Cached reads
            cached_input_tokens = model_input_tokens * cache_hit_rate
            uncached_input_tokens = model_input_tokens * (1 - cache_hit_rate)

            # Cost calculation (convert to millions)
            cached_input_cost = (cached_input_tokens / 1_000_000) * cache_price
            uncached_input_cost = (uncached_input_tokens / 1_000_000) * input_price
            output_cost = (model_output_tokens / 1_000_000) * output_price

            monthly_cost_usd = cached_input_cost + uncached_input_cost + output_cost

            # Calculate savings
            full_price_input = (model_input_tokens / 1_000_000) * input_price
            current_input = cached_input_cost + uncached_input_cost
            savings += (full_price_input - current_input)
        else:
            # No caching
            input_cost = (model_input_tokens / 1_000_000) * input_price
            output_cost = (model_output_tokens / 1_000_000) * output_price
            monthly_cost_usd = input_cost + output_cost

        # Convert to AUD
        monthly_cost = monthly_cost_usd / AUD_TO_USD
        total += monthly_cost

        cache_note = f" (Cache hit: {cache_hit_rate*100:.0f}%)" if use_caching else ""
        breakdown.append(CostBreakdown(
            category="LLM",
            subcategory=model,
            monthly_cost=monthly_cost,
            annual_cost=monthly_cost * 12,
            unit="tokens",
            quantity=model_input_tokens + model_output_tokens,
            notes=f"{percentage:.0f}% of queries{cache_note}"
        ))

    return total, breakdown, savings / AUD_TO_USD


def calculate_data_source_costs(agent_type: str) -> tuple[float, List[CostBreakdown]]:
    """Calculate data source costs based on agent requirements"""
    breakdown = []
    total = 0.0

    agent = AI_AGENTS[agent_type]
    data_sources = agent["data_sources"]

    # Map data source names to pricing config names
    source_mapping = {
        "ZoomInfo (Premium)": "ZoomInfo",
        "ZoomInfo": "ZoomInfo",
        "LinkedIn Sales Navigator (Premium)": "LinkedIn Sales Navigator",
        "LinkedIn Sales Navigator": "LinkedIn Sales Navigator",
        "Clearbit (Premium)": "Clearbit",
        "Clearbit": "Clearbit",
        "HubSpot/Salesforce CRM (Data Sync only, no UI)": "HubSpot/Salesforce CRM",
        "HubSpot/Salesforce CRM": "HubSpot/Salesforce CRM",
        "News APIs": "News APIs",
        "Social Media APIs": "Social Media APIs",
        "Company Data APIs": "Company Data APIs"
    }

    for source in data_sources:
        mapped_name = source_mapping.get(source, source)
        monthly_cost_usd = DATA_SOURCE_PRICING_USD.get(mapped_name, 0)

        if monthly_cost_usd == 0:
            # Skip zero-cost items (like CRM data sync)
            continue

        monthly_cost = monthly_cost_usd / AUD_TO_USD
        total += monthly_cost
        breakdown.append(CostBreakdown(
            category="Data Sources",
            subcategory=source,
            monthly_cost=monthly_cost,
            annual_cost=monthly_cost * 12,
            unit="subscription",
            quantity=1,
            notes=f"Enterprise tier subscription"
        ))

    return total, breakdown


def calculate_monitoring_costs(data_ingestion_gb: float) -> tuple[float, List[CostBreakdown]]:
    """Calculate monitoring and observability costs"""
    breakdown = []
    total = 0.0

    # Log Analytics
    log_cost = AZURE_PRICING_SYDNEY["monitoring"]["log_analytics_gb"] * data_ingestion_gb
    total += log_cost
    breakdown.append(CostBreakdown(
        category="Monitoring",
        subcategory="Azure Log Analytics",
        monthly_cost=log_cost,
        annual_cost=log_cost * 12,
        unit="GB",
        quantity=data_ingestion_gb,
        notes=f"{data_ingestion_gb:.0f} GB/month log ingestion"
    ))

    # Application Insights
    app_insights_cost = AZURE_PRICING_SYDNEY["monitoring"]["application_insights_gb"] * (data_ingestion_gb * 0.5)
    total += app_insights_cost
    breakdown.append(CostBreakdown(
        category="Monitoring",
        subcategory="Application Insights",
        monthly_cost=app_insights_cost,
        annual_cost=app_insights_cost * 12,
        unit="GB",
        quantity=data_ingestion_gb * 0.5,
        notes="APM and telemetry"
    ))

    # Grafana/Prometheus (self-hosted) - Estimated cost
    grafana_cost = 500.0  # Estimated monthly cost for self-hosted monitoring
    total += grafana_cost
    breakdown.append(CostBreakdown(
        category="Monitoring",
        subcategory="Grafana & Prometheus",
        monthly_cost=grafana_cost,
        annual_cost=grafana_cost * 12,
        unit="service",
        quantity=1,
        notes="Self-hosted dashboards and metrics"
    ))

    return total, breakdown


def calculate_memory_system_costs(memory_type: str, capacity_gb: float = 6) -> tuple[float, List[CostBreakdown]]:
    """
    Calculate memory system costs based on user selection
    THIS ADDRESSES USER'S QUESTION: Memory selection now affects costs!
    """
    breakdown = []

    # Calculate monthly cost based on memory type
    if memory_type == "redis":
        monthly_cost = AZURE_PRICING_SYDNEY["database"]["redis_c6"] * 730
    elif memory_type == "cosmos_db":
        monthly_cost = AZURE_PRICING_SYDNEY["database"]["cosmosdb_ru_100"] * (45000 / 100) * 730
    elif memory_type == "neo4j":
        neo4j_vm = AZURE_PRICING_SYDNEY["compute"]["Standard_D16s_v5"]
        monthly_cost = neo4j_vm["payg"] * 730 * 2  # 2 nodes
    else:  # in_memory
        monthly_cost = 0.0

    if monthly_cost > 0:
        breakdown.append(CostBreakdown(
            category="Memory System",
            subcategory=f"{memory_type.replace('_', ' ').title()}",
            monthly_cost=monthly_cost,
            annual_cost=monthly_cost * 12,
            unit="system",
            quantity=1,
            notes=f"Selected memory system: {memory_type}"
        ))

    return monthly_cost, breakdown


def calculate_mcp_tools_costs(selected_tools: List[str], num_assessments: int = 4000) -> tuple[float, List[CostBreakdown]]:
    """
    Calculate MCP tools costs based on user selection
    THIS ADDRESSES USER'S QUESTION: Tools selection now affects costs!
    """
    breakdown = []

    # Calculate total monthly cost for MCP tools
    total_cost = 0.0
    
    # Simple pricing for MCP tools (estimated)
    mcp_tool_pricing = {
        "CRM Integration": 200.0,  # Monthly cost for CRM sync
        "Email Integration": 150.0,  # Monthly cost for email parsing
        "Calendar Integration": 100.0,  # Monthly cost for calendar sync
        "Document Analysis": 300.0,  # Monthly cost for document processing
        "Web Search": 50.0,  # Monthly cost for web search APIs
        "Data Enrichment": 400.0,  # Monthly cost for data enrichment
    }

    if selected_tools:
        for tool_name in selected_tools:
            tool_cost = mcp_tool_pricing.get(tool_name, 0.0)
            total_cost += tool_cost
            
            breakdown.append(CostBreakdown(
                category="MCP Tools",
                subcategory=tool_name,
                monthly_cost=tool_cost,
                annual_cost=tool_cost * 12,
                unit="service",
                quantity=1,
                notes=f"Monthly subscription for {tool_name}"
            ))

    return total_cost, breakdown


# ===========================
# API ENDPOINT
# ===========================

@router.post("/calculate", response_model=CostCalculatorResponse)
async def calculate_costs(params: CostCalculatorRequest):
    """Calculate comprehensive costs for AI agent deployment"""

    # Validate agent type
    if params.agent_type not in AI_AGENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown agent type. Available: {list(AI_AGENTS.keys())}"
        )

    agent_info = AI_AGENTS[params.agent_type]

    # Get infrastructure configuration
    infra = get_agent_infrastructure(
        params.agent_type,
        params.infrastructure_scale,
        params.custom_infrastructure
    )

    # Calculate all costs
    infra_total, infra_breakdown = calculate_infrastructure_costs(infra, params.use_reserved_instances)

    llm_total, llm_breakdown, cache_savings = calculate_llm_costs(
        params.num_users,
        params.queries_per_user_per_month,
        params.avg_input_tokens,
        params.avg_output_tokens,
        params.llm_mix,
        params.cache_hit_rate,
        params.use_prompt_caching
    )

    data_total, data_breakdown = calculate_data_source_costs(params.agent_type)

    # Estimate data ingestion for monitoring (based on queries and users)
    estimated_data_gb = (params.num_users * params.queries_per_user_per_month * 0.001) + 100  # Base 100GB
    monitor_total, monitor_breakdown = calculate_monitoring_costs(estimated_data_gb)

    # Calculate MEMORY SYSTEM costs (NEW - addresses user's question)
    memory_total, memory_breakdown = calculate_memory_system_costs(
        memory_type=params.memory_type,
        capacity_gb=6.0  # Default capacity
    )

    # Calculate MCP TOOLS costs (NEW - addresses user's question)
    # Calculate number of assessments/queries for tools cost
    total_queries = params.num_users * params.queries_per_user_per_month
    tools_total, tools_breakdown = calculate_mcp_tools_costs(
        selected_tools=params.selected_tools,
        num_assessments=total_queries
    )

    # Calculate totals (INCLUDING new memory and tools costs)
    fixed_monthly = infra_total + data_total + monitor_total + memory_total + tools_total
    variable_monthly = llm_total
    total_monthly = fixed_monthly + variable_monthly
    total_annual = total_monthly * 12

    # Calculate savings
    reserved_savings = 0.0
    if params.use_reserved_instances:
        # Estimate 40% savings on compute
        payg_compute = 0.0
        for item in infra_breakdown:
            if "Node" in item.subcategory or "Database" in item.subcategory:
                payg_compute += item.monthly_cost / 0.6  # Reverse calculate PAYG
        reserved_savings = payg_compute - (payg_compute * 0.6)

    # Metrics
    total_queries = params.num_users * params.queries_per_user_per_month
    total_input_tokens = total_queries * params.avg_input_tokens
    total_output_tokens = total_queries * params.avg_output_tokens

    # Build agent architecture response
    agent_architecture = AgentArchitecture(
        agent_type=params.agent_type,
        agent_name=agent_info["name"],
        description=agent_info["description"],
        agents_count=agent_info["agents_count"],
        agents_list=agent_info["agents"],
        mcp_tools=agent_info.get("mcp_tools", []),  # Include MCP tools if available
        data_buckets=agent_info["data_buckets"],
        data_sources=agent_info["data_sources"],
        complexity=agent_info["complexity"],
        infrastructure=infra
    )

    return CostCalculatorResponse(
        agent_architecture=agent_architecture,
        total_monthly_cost=total_monthly,
        total_annual_cost=total_annual,
        cost_per_user_monthly=total_monthly / params.num_users,
        cost_per_user_annual=total_annual / params.num_users,
        cost_per_query=total_monthly / total_queries,
        fixed_monthly_cost=fixed_monthly,
        variable_monthly_cost=variable_monthly,
        infrastructure_costs=infra_total,
        llm_costs=llm_total,
        data_source_costs=data_total,
        monitoring_costs=monitor_total,
        memory_system_costs=memory_total,  # NEW - memory costs impact!
        mcp_tools_costs=tools_total,       # NEW - tools costs impact!
        infrastructure_breakdown=infra_breakdown,
        llm_breakdown=llm_breakdown,
        data_source_breakdown=data_breakdown,
        monitoring_breakdown=monitor_breakdown,
        memory_system_breakdown=memory_breakdown,  # NEW
        mcp_tools_breakdown=tools_breakdown,       # NEW
        queries_per_month=total_queries,
        input_tokens_per_month=total_input_tokens,
        output_tokens_per_month=total_output_tokens,
        estimated_data_size_gb=infra["storage_hot_tb"] + infra["storage_cool_tb"],
        savings_from_caching=cache_savings,
        savings_from_reserved_instances=reserved_savings
    )


@router.get("/agents")
async def list_agents():
    """Get list of available AI agents"""
    return {
        "agents": [
            {
                "id": key,
                "name": value["name"],
                "description": value["description"],
                "complexity": value["complexity"],
                "agents_count": value["agents_count"]
            }
            for key, value in AI_AGENTS.items()
        ]
    }


@router.get("/agents/{agent_id}")
async def get_agent_details(agent_id: str):
    """Get detailed information about a specific agent"""
    if agent_id not in AI_AGENTS:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    return {
        "agent_id": agent_id,
        **AI_AGENTS[agent_id]
    }
