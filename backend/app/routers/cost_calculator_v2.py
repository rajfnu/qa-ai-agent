import sys
import os

# Add the config directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import json

# Import service tier configurations
from config.service_tiers import (
    SERVICE_TIERS,
    LLM_CATEGORIES,
    get_tier_config,
    get_llm_models_for_tier,
    get_tier_summary,
    calculate_on_premise_cost
)

# Load LLM pricing from LLM_Pricing.json
def load_llm_pricing():
    """Load LLM pricing from LLM_Pricing.json file"""
    config_path = os.path.join(os.path.dirname(__file__), '../../config/LLM_Pricing.json')
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            # Flatten the providers structure to model_id: {input, output, ...}
            pricing = {}
            for provider, models in data.get('providers', {}).items():
                for model_id, model_data in models.items():
                    pricing[model_id] = {
                        'input': model_data.get('input', 0.0),
                        'output': model_data.get('output', 0.0),
                        'cache_read': model_data.get('cachedInput', 0.0)
                    }
            return pricing
    except Exception as e:
        print(f"Error loading LLM_Pricing.json: {e}")
        return {}

# Load pricing on module import
LLM_PRICING_USD = load_llm_pricing()

# ===========================
# PRICING CONFIGURATION
# ===========================

# Azure Pricing (AUD) - Sydney Region - January 2025
# Source: Azure Pricing Calculator
AZURE_PRICING_SYDNEY = {
    "compute": {
        "Standard_D16s_v5": {
            "payg": 1.44,  # per hour
            "reserved_1yr": 0.72,  # 50% discount
            "reserved_3yr": 0.58   # 60% discount
        },
        "Standard_NC6s_v3": {  # GPU node
            "payg": 3.06,  # per hour
            "reserved_1yr": 1.53,  # 50% discount
            "reserved_3yr": 1.22   # 60% discount
        }
    },
    "database": {
        "cosmosdb_ru_100": 0.008,  # per 100 RU/s per hour
        "redis_c6": 0.192,  # per hour
        "sql_standard": 0.192  # per vCore per hour
    },
    "storage": {
        "hot_lrs": 0.04,  # per GB per month
        "cool_lrs": 0.01,  # per GB per month
        "archive_lrs": 0.002  # per GB per month
    },
    "monitoring": {
        "log_analytics_gb": 2.30,  # per GB
        "application_insights_gb": 2.30  # per GB
    }
}

# Premium Data Source Pricing (USD per month) - January 2025
DATA_SOURCE_PRICING_USD = {
    "ZoomInfo": 15000,  # Enterprise tier
    "LinkedIn Sales Navigator": 9900,  # Enterprise tier
    "Clearbit": 5000,  # Enterprise tier
    "HubSpot/Salesforce CRM": 0,  # Data sync only, no UI
    "News APIs": 2000,  # Multiple news sources
    "Social Media APIs": 1500,  # Twitter, LinkedIn, etc.
    "Company Data APIs": 3000   # Various company data providers
}

# Exchange rate (AUD to USD)
AUD_TO_USD = 0.65

# ===========================
# AI AGENT CONFIGURATIONS
# ===========================

AI_AGENTS = {
    "sales-coach": {
        "name": "Sales Coach in the Pocket",
        "description": "Multi-agent sales coaching system with 4Cs framework",
        "data_sources": [
            "ZoomInfo",
            "LinkedIn Sales Navigator", 
            "Clearbit",
            "HubSpot/Salesforce CRM",
            "News APIs",
            "Social Media APIs",
            "Company Data APIs"
        ],
        "infrastructure": {
            "aks_nodes": 8,
            "gpu_nodes": 2,
            "sql_vcores": 12,
            "cosmos_ru": 45000,
            "neo4j_nodes": 2,
            "storage_hot_tb": 0.5,
            "storage_cool_tb": 2.0
        }
    }
}

# ===========================
# MODELS
# ===========================

class CostCalculatorRequest(BaseModel):
    # AI Agent Selection
    agent_type: str = Field(default="sales-coach", description="Type of AI agent")

    # Service Tier Selection (NEW - for end-user pricing plans)
    service_tier: str = Field(
        default="standard",
        description="Service tier: basic ($30/user), standard ($149/user), premium ($999/user)"
    )

    # Deployment Type (NEW - cloud API vs on-premise)
    deployment_type: str = Field(
        default="cloud_api",
        description="Deployment type: cloud_api (token-based pricing) or on_premise (infrastructure-based pricing)"
    )

    # User Parameters
    num_users: int = Field(default=100, ge=1, le=10000)
    queries_per_user_per_month: int = Field(default=1000, ge=10, le=10000)  # Lowered from 100 to 10 for Sales Coach assessments
    avg_input_tokens: int = Field(default=10000, ge=1000, le=100000)
    avg_output_tokens: int = Field(default=1000, ge=100, le=10000)

    # Infrastructure Parameters
    infrastructure_scale: float = Field(default=1.0, ge=0.1, le=5.0)
    memory_type: str = Field(default="redis", description="Memory system: redis, cosmos-db, neo4j, in_memory")

    # LLM Configuration
    llm_mix: Dict[str, float] = Field(
        default={"gpt-4o": 60.0, "claude-3.5-sonnet": 30.0, "llama-3.1-70b": 10.0},
        description="LLM model distribution (percentages must sum to 100)"
    )

    # Optimization Settings
    cache_hit_rate: float = Field(default=0.70, ge=0.0, le=1.0)
    use_prompt_caching: bool = Field(default=True)
    use_reserved_instances: bool = Field(default=True)

    # MCP Tools (NEW - addresses user's question)
    mcp_tools: List[str] = Field(
        default=[],
        description="Selected MCP tools for the agent"
    )

class AgentCostRequest(BaseModel):
    """Request model for calculating individual agent LLM costs"""
    llm_model: str = Field(..., description="The LLM model used by this agent")
    deployment_type: str = Field(default="cloud_api", description="cloud_api or on_premise")
    num_users: int = Field(default=100, ge=1, le=10000)
    queries_per_user_per_month: int = Field(default=40, ge=1, le=10000)
    avg_tokens_per_request: int = Field(default=5000, ge=100, le=100000)
    cache_hit_rate: float = Field(default=0.70, ge=0.0, le=1.0)
    use_prompt_caching: bool = Field(default=True)

class AgentCostResponse(BaseModel):
    """Response model for individual agent cost"""
    agent_llm_cost_monthly: float
    agent_llm_cost_annual: float
    total_queries_per_month: int
    total_input_tokens_per_month: int
    total_output_tokens_per_month: int
    llm_model: str
    deployment_type: str

class CostBreakdown(BaseModel):
    category: str
    subcategory: str
    monthly_cost: float
    annual_cost: float
    unit: str
    quantity: float
    notes: str

class AgentArchitecture(BaseModel):
    name: str
    description: str
    data_sources: List[str]
    infrastructure: Dict[str, float]

class CostCalculatorResponse(BaseModel):
    # Total Costs
    total_monthly_cost: float
    total_annual_cost: float
    
    # Cost Breakdown by Category
    llm_costs: float
    infrastructure_costs: float
    data_source_costs: float
    monitoring_costs: float
    memory_system_costs: float  # Tier-based
    retrieval_costs: float  # NEW - Tier-based RAG/Vector DB costs
    security_costs: float  # NEW - Tier-based security costs
    prompt_tuning_costs: float  # NEW - Tier-based prompt optimization costs
    mcp_tools_costs: float  # User-selected tools

    # Detailed Breakdown by Tab
    llm_breakdown: List[CostBreakdown]
    infrastructure_breakdown: List[CostBreakdown]
    data_source_breakdown: List[CostBreakdown]
    monitoring_breakdown: List[CostBreakdown]
    memory_system_breakdown: List[CostBreakdown]
    retrieval_breakdown: List[CostBreakdown]  # NEW
    security_breakdown: List[CostBreakdown]  # NEW
    prompt_tuning_breakdown: List[CostBreakdown]  # NEW
    mcp_tools_breakdown: List[CostBreakdown]

    # Metrics
    queries_per_month: int
    input_tokens_per_month: int
    output_tokens_per_month: int
    estimated_data_size_gb: float
    savings_from_caching: float
    savings_from_reserved_instances: float

# ===========================
# COST CALCULATION FUNCTIONS
# ===========================

def get_agent_infrastructure(agent_type: str, service_tier: str, scale: float, custom: Optional[Dict] = None) -> Dict[str, float]:
    """
    Get infrastructure configuration for an agent based on service tier.
    Uses tier-specific infrastructure from service_tiers.py instead of agent defaults.
    """
    from config.service_tiers import INFRASTRUCTURE_CONFIGS

    # Get tier-specific infrastructure configuration
    tier_infra = INFRASTRUCTURE_CONFIGS.get(service_tier.lower(), INFRASTRUCTURE_CONFIGS["standard"])

    # Convert storage from GB to TB for compatibility with existing calculations
    base_infra = {
        "aks_nodes": tier_infra.get("aks_nodes", 5),
        "gpu_nodes": 0,  # No GPU nodes in tier configs, set to 0
        "sql_vcores": tier_infra.get("sql_vcores", 6),
        "cosmos_ru": tier_infra.get("cosmos_ru", 15000),
        "neo4j_nodes": tier_infra.get("neo4j_nodes", 1),
        "storage_hot_tb": tier_infra.get("storage_hot_gb", 500) / 1024.0,  # Convert GB to TB
        "storage_cool_tb": tier_infra.get("storage_cool_gb", 4000) / 1024.0,  # Convert GB to TB
    }

    # Apply custom overrides if provided
    if custom:
        base_infra = {**base_infra, **custom}

    # Apply scale multiplier
    return {key: value * scale for key, value in base_infra.items()}

def calculate_infrastructure_costs(infra: Dict[str, float], use_reserved: bool) -> tuple[float, List[CostBreakdown]]:
    """Calculate infrastructure costs based on Azure pricing"""
    breakdown = []
    total = 0.0

    # AKS Nodes
    aks_cost = AZURE_PRICING_SYDNEY["compute"]["Standard_D16s_v5"]["reserved_1yr" if use_reserved else "payg"] * infra["aks_nodes"] * 730
    total += aks_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="AKS Nodes",
        monthly_cost=aks_cost,
        annual_cost=aks_cost * 12,
        unit="nodes",
        quantity=infra["aks_nodes"],
        notes=f"Standard_D16s_v5 × {int(infra['aks_nodes'])} nodes"
    ))

    # GPU Nodes (if any)
    if infra["gpu_nodes"] > 0:
        gpu_cost = AZURE_PRICING_SYDNEY["compute"]["Standard_NC6s_v3"]["reserved_1yr" if use_reserved else "payg"] * infra["gpu_nodes"] * 730
        total += gpu_cost
        breakdown.append(CostBreakdown(
            category="Infrastructure",
            subcategory="GPU Nodes",
            monthly_cost=gpu_cost,
            annual_cost=gpu_cost * 12,
            unit="nodes",
            quantity=infra["gpu_nodes"],
            notes=f"Standard_NC6s_v3 × {int(infra['gpu_nodes'])} nodes"
        ))

    # SQL Database
    sql_cost = AZURE_PRICING_SYDNEY["database"]["sql_standard"] * infra["sql_vcores"] * 730
    total += sql_cost
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="SQL Database",
        monthly_cost=sql_cost,
        annual_cost=sql_cost * 12,
        unit="vCores",
        quantity=infra["sql_vcores"],
        notes=f"Standard tier × {int(infra['sql_vcores'])} vCores"
    ))

    # Storage
    hot_storage_cost = AZURE_PRICING_SYDNEY["storage"]["hot_lrs"] * infra["storage_hot_tb"] * 1024  # TB to GB
    cool_storage_cost = AZURE_PRICING_SYDNEY["storage"]["cool_lrs"] * infra["storage_cool_tb"] * 1024
    storage_total = hot_storage_cost + cool_storage_cost
    total += storage_total
    breakdown.append(CostBreakdown(
        category="Infrastructure",
        subcategory="Storage",
        monthly_cost=storage_total,
        annual_cost=storage_total * 12,
        unit="GB",
        quantity=infra["storage_hot_tb"] + infra["storage_cool_tb"],
        notes=f"{infra['storage_hot_tb']}TB hot + {infra['storage_cool_tb']}TB cool"
    ))

    return total, breakdown

def calculate_llm_costs(
    llm_mix: Dict[str, float],
    total_queries: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    cache_hit_rate: float,
    use_prompt_caching: bool
) -> tuple[float, List[CostBreakdown]]:
    """Calculate LLM costs based on token usage and pricing"""
    breakdown = []
    total = 0.0

    for model, percentage in llm_mix.items():
        if percentage <= 0:
            continue

        # Get pricing for this model
        pricing = LLM_PRICING_USD.get(model, {"input": 2.50, "output": 10.00, "cache_read": 1.25})
        
        # Calculate tokens for this model
        model_queries = total_queries * (percentage / 100)
        input_tokens = model_queries * avg_input_tokens
        output_tokens = model_queries * avg_output_tokens

        # Apply caching
        if use_prompt_caching and "cache_read" in pricing:
            cached_input_tokens = input_tokens * cache_hit_rate
            fresh_input_tokens = input_tokens * (1 - cache_hit_rate)
            
            # Cost calculation
            input_cost = (cached_input_tokens / 1000000 * pricing["cache_read"] + 
                         fresh_input_tokens / 1000000 * pricing["input"])
        else:
            input_cost = input_tokens / 1000000 * pricing["input"]
        
        output_cost = output_tokens / 1000000 * pricing["output"]
        model_cost = (input_cost + output_cost) / AUD_TO_USD  # Convert to AUD
        
        total += model_cost
        
        breakdown.append(CostBreakdown(
            category="LLM Costs",
            subcategory=model,
            monthly_cost=model_cost,
            annual_cost=model_cost * 12,
            unit="tokens",
            quantity=input_tokens + output_tokens,
            notes=f"{percentage}% of queries, {cache_hit_rate*100:.0f}% cache hit rate"
        ))

    return total, breakdown

def calculate_data_source_costs(agent_type: str, service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """Calculate data source costs based on service tier (NOT agent requirements)"""
    breakdown = []

    # Get tier-specific data source configuration from service_tiers.py
    tier_config = get_tier_config(service_tier)
    data_sources_config = tier_config.get("data_sources", {})

    # Use the tier-specific monthly cost directly
    monthly_cost_aud = data_sources_config.get("monthly_cost", 0.0)
    sources = data_sources_config.get("sources", [])

    if monthly_cost_aud > 0:
        # If there's a cost, add breakdown for included data sources
        sources_str = ", ".join(sources) if sources else "No premium data sources"
        breakdown.append(CostBreakdown(
            category="Data Sources",
            subcategory=f"{service_tier.title()} Tier Data Sources",
            monthly_cost=monthly_cost_aud,
            annual_cost=monthly_cost_aud * 12,
            unit="subscription",
            quantity=len(sources),
            notes=f"Included sources: {sources_str}"
        ))
    else:
        # Basic tier - no premium data sources
        breakdown.append(CostBreakdown(
            category="Data Sources",
            subcategory="No Premium Data Sources",
            monthly_cost=0.0,
            annual_cost=0.0,
            unit="subscription",
            quantity=0,
            notes="Basic tier includes no premium data sources"
        ))

    return monthly_cost_aud, breakdown

def calculate_monitoring_costs(data_ingestion_gb: float, service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """Calculate monitoring and observability costs based on service tier"""
    breakdown = []

    # Get tier-specific monitoring configuration from service_tiers.py
    tier_config = get_tier_config(service_tier)
    monitoring_config = tier_config.get("monitoring", {})

    monthly_cost = monitoring_config.get("monthly_cost", 0.0)
    apm_tool = monitoring_config.get("apm_tool", "basic_logging")
    features = monitoring_config.get("features", [])
    features_str = ", ".join(features)

    breakdown.append(CostBreakdown(
        category="Monitoring",
        subcategory=f"{apm_tool} ({service_tier.title()} Tier)",
        monthly_cost=monthly_cost,
        annual_cost=monthly_cost * 12,
        unit="service",
        quantity=1,
        notes=f"Features: {features_str}"
    ))

    return monthly_cost, breakdown

def calculate_memory_system_costs(memory_type: str, infrastructure: Dict[str, float], service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """
    Calculate memory system costs based on service tier configuration
    THIS ADDRESSES USER'S QUESTION: Memory selection now affects costs based on tier!
    """
    breakdown = []

    # Get tier-specific memory configuration from service_tiers.py
    tier_config = get_tier_config(service_tier)
    memory_config = tier_config.get("memory", {})

    monthly_cost = memory_config.get("monthly_cost", 0.0)
    memory_type_tier = memory_config.get("type", "in_memory")
    capacity_gb = memory_config.get("capacity_gb", 0)
    persistence = memory_config.get("persistence", False)
    replication = memory_config.get("replication", False)

    features = []
    if persistence:
        features.append("Persistence")
    if replication:
        features.append("Replication")
    if memory_config.get("global_distribution"):
        features.append("Global Distribution")

    features_str = ", ".join(features) if features else "No advanced features"

    breakdown.append(CostBreakdown(
        category="Memory System",
        subcategory=f"{memory_type_tier.title()} ({service_tier.title()} Tier)",
        monthly_cost=monthly_cost,
        annual_cost=monthly_cost * 12,
        unit="GB",
        quantity=capacity_gb,
        notes=f"{capacity_gb}GB capacity. Features: {features_str}"
    ))

    return monthly_cost, breakdown

def calculate_mcp_tools_costs(selected_tools: List[str], num_assessments: int = 4000) -> tuple[float, List[CostBreakdown]]:
    """Calculate MCP tools costs based on selected tools"""
    breakdown = []
    
    # Calculate total monthly cost for MCP tools
    total_cost = 0.0

    # Simple pricing for MCP tools (estimated)
    mcp_tool_pricing = {
        "research_tool": 0.50,  # $0.50 per assessment
        "content_generation_tool": 0.30,  # $0.30 per assessment
        "competitive_intel_tool": 0.75,  # $0.75 per assessment
        "fog_analysis_tool": 0.40,  # $0.40 per assessment
        "engagement_excellence_tool": 0.60,  # $0.60 per assessment
        "impact_theme_generator_tool": 0.35,  # $0.35 per assessment
        "license_to_sell_tool": 0.25,  # $0.25 per assessment
        "find_money_validator_tool": 0.45,  # $0.45 per assessment
        "speech_to_text": 0.20  # $0.20 per assessment
    }

    for tool_name in selected_tools:
        if tool_name in mcp_tool_pricing:
            tool_cost = mcp_tool_pricing.get(tool_name, 0.0)
            total_cost += tool_cost

            breakdown.append(CostBreakdown(
                category="MCP Tools",
                subcategory=tool_name,
                monthly_cost=tool_cost,
                annual_cost=tool_cost * 12,
                unit="assessment",
                quantity=num_assessments,
                notes=f"Per assessment cost for {tool_name}"
            ))

    return total_cost, breakdown

def calculate_retrieval_costs(service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """Calculate retrieval/RAG costs based on service tier"""
    breakdown = []

    # Get tier-specific retrieval configuration from service_tiers.py
    tier_config = get_tier_config(service_tier)
    retrieval_config = tier_config.get("retrieval", {})

    monthly_cost = retrieval_config.get("monthly_cost", 0.0)
    vector_db = retrieval_config.get("vector_db", "in_memory")
    max_vectors = retrieval_config.get("max_vectors", 0)
    indexing = retrieval_config.get("indexing", "flat")

    features = []
    if retrieval_config.get("metadata_filtering"):
        features.append("Metadata Filtering")
    if retrieval_config.get("hybrid_search"):
        features.append("Hybrid Search")

    features_str = ", ".join(features) if features else f"Indexing: {indexing}"

    breakdown.append(CostBreakdown(
        category="Retrieval/RAG",
        subcategory=f"{vector_db} ({service_tier.title()} Tier)",
        monthly_cost=monthly_cost,
        annual_cost=monthly_cost * 12,
        unit="vectors",
        quantity=max_vectors,
        notes=f"{max_vectors:,} max vectors. {features_str}"
    ))

    return monthly_cost, breakdown

def calculate_security_costs(service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """Calculate security costs based on service tier"""
    breakdown = []

    # Get tier-specific security configuration from service_tiers.py
    tier_config = get_tier_config(service_tier)
    security_config = tier_config.get("security", {})

    monthly_cost = security_config.get("monthly_cost", 0.0)
    level = security_config.get("level", "basic")
    features = security_config.get("features", [])
    features_str = ", ".join(features)

    compliance = security_config.get("compliance", [])
    compliance_str = f" Compliance: {', '.join(compliance)}" if compliance else ""

    breakdown.append(CostBreakdown(
        category="Security",
        subcategory=f"{level.title()} Security ({service_tier.title()} Tier)",
        monthly_cost=monthly_cost,
        annual_cost=monthly_cost * 12,
        unit="service",
        quantity=1,
        notes=f"Features: {features_str}.{compliance_str}"
    ))

    return monthly_cost, breakdown

def calculate_prompt_tuning_costs(service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """Calculate prompt tuning costs based on service tier"""
    breakdown = []

    # Get tier-specific prompt tuning configuration from service_tiers.py
    tier_config = get_tier_config(service_tier)
    prompt_tuning_config = tier_config.get("prompt_tuning", {})

    monthly_cost = prompt_tuning_config.get("monthly_cost", 0.0)
    approach = prompt_tuning_config.get("approach", "manual")
    features = prompt_tuning_config.get("features", [])
    features_str = ", ".join(features)

    breakdown.append(CostBreakdown(
        category="Prompt Tuning",
        subcategory=f"{approach.replace('_', ' ').title()} ({service_tier.title()} Tier)",
        monthly_cost=monthly_cost,
        annual_cost=monthly_cost * 12,
        unit="service",
        quantity=1,
        notes=f"Features: {features_str}"
    ))

    return monthly_cost, breakdown

def apply_service_tier_config(params: CostCalculatorRequest) -> CostCalculatorRequest:
    """Apply service tier configuration to request parameters"""

    # If service_tier is provided and exists in SERVICE_TIERS
    if params.service_tier and params.service_tier.lower() in SERVICE_TIERS:
        tier_config = SERVICE_TIERS[params.service_tier.lower()]

        # Override LLM mix with tier configuration (using deployment_type)
        # Build LLM mix based on available models in tier
        llm_models = tier_config["llm_models"].get(params.deployment_type, [])
        if llm_models:
            # Distribute evenly across available models
            percentage_per_model = 100.0 / len(llm_models)
            params.llm_mix = {model: percentage_per_model for model in llm_models}

        # Override caching settings from limits
        limits = tier_config.get("limits", {})
        params.cache_hit_rate = limits.get("cache_hit_rate", 0.70)

        # Override features
        features = tier_config.get("features", {})
        params.use_prompt_caching = features.get("use_prompt_caching", True)
        params.use_reserved_instances = features.get("use_reserved_instances", False)

    return params

# ===========================
# MAIN COST CALCULATION
# ===========================

async def calculate_costs(params: CostCalculatorRequest):
    """Calculate comprehensive costs for AI agent deployment"""

    # Apply service tier configuration (Basic, Standard, Premium)
    params = apply_service_tier_config(params)

    # Validate agent type
    if params.agent_type not in AI_AGENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Agent type '{params.agent_type}' not supported. Available: {list(AI_AGENTS.keys())}"
        )

    # Get agent configuration
    agent = AI_AGENTS[params.agent_type]

    # Get infrastructure configuration (tier-based)
    infra = get_agent_infrastructure(
        params.agent_type,
        params.service_tier,
        params.infrastructure_scale,
        None  # No custom infrastructure for now
    )

    # Calculate costs
    total_queries = params.num_users * params.queries_per_user_per_month
    total_input_tokens = total_queries * params.avg_input_tokens
    total_output_tokens = total_queries * params.avg_output_tokens

    # Calculate LLM costs
    llm_total, llm_breakdown = calculate_llm_costs(
        params.llm_mix,
        total_queries,
        params.avg_input_tokens,
        params.avg_output_tokens,
        params.cache_hit_rate,
        params.use_prompt_caching
    )

    # Calculate infrastructure costs
    infra_total, infra_breakdown = calculate_infrastructure_costs(infra, params.use_reserved_instances)

    # Calculate tier-based costs using service_tiers.py configurations
    data_total, data_breakdown = calculate_data_source_costs(params.agent_type, params.service_tier)

    # Estimate data ingestion for monitoring (based on queries and users)
    estimated_data_gb = (params.num_users * params.queries_per_user_per_month * 0.001) + 100  # Base 100GB
    monitor_total, monitor_breakdown = calculate_monitoring_costs(estimated_data_gb, params.service_tier)

    # Calculate MEMORY SYSTEM costs (tier-based)
    memory_total, memory_breakdown = calculate_memory_system_costs(
        memory_type=params.memory_type,
        infrastructure=infra,
        service_tier=params.service_tier
    )

    # Calculate RETRIEVAL/RAG costs (NEW - tier-based)
    retrieval_total, retrieval_breakdown = calculate_retrieval_costs(params.service_tier)

    # Calculate SECURITY costs (NEW - tier-based)
    security_total, security_breakdown = calculate_security_costs(params.service_tier)

    # Calculate PROMPT TUNING costs (NEW - tier-based)
    prompt_tuning_total, prompt_tuning_breakdown = calculate_prompt_tuning_costs(params.service_tier)

    # Calculate MCP TOOLS costs (user-selected)
    total_queries = params.num_users * params.queries_per_user_per_month
    tools_total, tools_breakdown = calculate_mcp_tools_costs(
        params.mcp_tools,
        total_queries
    )

    # Calculate savings
    cache_savings = llm_total * (1 - params.cache_hit_rate) if params.use_prompt_caching else 0
    reserved_savings = infra_total * 0.5 if params.use_reserved_instances else 0

    # Calculate totals (INCLUDING all tier-based costs)
    fixed_monthly = (infra_total + data_total + monitor_total + memory_total +
                    retrieval_total + security_total + prompt_tuning_total + tools_total)
    variable_monthly = llm_total
    total_monthly = fixed_monthly + variable_monthly

    return CostCalculatorResponse(
        total_monthly_cost=total_monthly,
        total_annual_cost=total_monthly * 12,
        llm_costs=llm_total,
        infrastructure_costs=infra_total,
        data_source_costs=data_total,
        monitoring_costs=monitor_total,
        memory_system_costs=memory_total,
        retrieval_costs=retrieval_total,  # NEW - tier-based RAG costs
        security_costs=security_total,  # NEW - tier-based security costs
        prompt_tuning_costs=prompt_tuning_total,  # NEW - tier-based prompt tuning costs
        mcp_tools_costs=tools_total,
        infrastructure_breakdown=infra_breakdown,
        llm_breakdown=llm_breakdown,
        data_source_breakdown=data_breakdown,
        monitoring_breakdown=monitor_breakdown,
        memory_system_breakdown=memory_breakdown,
        retrieval_breakdown=retrieval_breakdown,  # NEW
        security_breakdown=security_breakdown,  # NEW
        prompt_tuning_breakdown=prompt_tuning_breakdown,  # NEW
        mcp_tools_breakdown=tools_breakdown,
        queries_per_month=total_queries,
        input_tokens_per_month=total_input_tokens,
        output_tokens_per_month=total_output_tokens,
        estimated_data_size_gb=infra["storage_hot_tb"] + infra["storage_cool_tb"],
        savings_from_caching=cache_savings,
        savings_from_reserved_instances=reserved_savings
    )

# ===========================
# API ROUTES
# ===========================

router = APIRouter()

@router.post("/calculate", response_model=CostCalculatorResponse)
async def calculate_costs_endpoint(params: CostCalculatorRequest):
    """Calculate comprehensive costs for AI agent deployment"""
    return await calculate_costs(params)

@router.get("/agents")
async def list_agents():
    """List all available AI agents"""
    return {
        "agents": [
            {
                "id": agent_id,
                "name": agent["name"],
                "description": agent["description"],
                "data_sources": agent["data_sources"]
            }
            for agent_id, agent in AI_AGENTS.items()
        ]
    }

@router.get("/agents/{agent_id}")
async def get_agent_details(agent_id: str):
    """Get detailed information about a specific agent"""
    if agent_id not in AI_AGENTS:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    agent = AI_AGENTS[agent_id]
    return {
        "id": agent_id,
        "name": agent["name"],
        "description": agent["description"],
        "data_sources": agent["data_sources"],
        "infrastructure": agent["infrastructure"]
    }

@router.get("/tiers")
async def list_service_tiers():
    """List all available service tiers"""
    return {
        "tiers": [
            {
                "tier_id": key,
                "name": value["name"],
                "target_price_per_user_monthly": value["target_price_per_user_monthly"],
                "description": value.get("description", ""),
                "data_sources_included": value.get("data_sources", {}).get("sources", [])
            }
            for key, value in SERVICE_TIERS.items()
        ]
    }

@router.get("/tiers/{tier_id}")
async def get_tier_details(tier_id: str):
    """Get detailed information about a specific service tier"""
    if tier_id.lower() not in SERVICE_TIERS:
        raise HTTPException(status_code=404, detail=f"Tier {tier_id} not found")

    tier_config = SERVICE_TIERS[tier_id.lower()]
    return {
        "tier_id": tier_id.lower(),
        "name": tier_config["name"],
        "description": tier_config.get("description", ""),
        "target_price_per_user_monthly": tier_config["target_price_per_user_monthly"],
        "data_sources_included": tier_config.get("data_sources", {}).get("sources", [])
    }

@router.get("/tiers/{tier_id}/models")
async def get_tier_models(tier_id: str, deployment_type: str = "cloud_api"):
    """Get available LLM models for a specific tier and deployment type"""
    if tier_id.lower() not in SERVICE_TIERS:
        raise HTTPException(status_code=404, detail=f"Tier {tier_id} not found")

    models = get_llm_models_for_tier(tier_id.lower(), deployment_type)
    return {
        "tier_id": tier_id.lower(),
        "deployment_type": deployment_type,
        "models": models
    }

@router.post("/calculate-agent", response_model=AgentCostResponse)
async def calculate_agent_cost_endpoint(params: AgentCostRequest):
    """
    Calculate LLM costs for a SINGLE agent only (no infrastructure costs).
    This endpoint is designed for per-agent cost calculation in the Sales Coach UI.
    """
    # Calculate total queries for this agent
    total_queries = params.num_users * params.queries_per_user_per_month

    # Calculate input/output tokens (70/30 split)
    avg_input_tokens = int(params.avg_tokens_per_request * 0.7)
    avg_output_tokens = int(params.avg_tokens_per_request * 0.3)

    total_input_tokens = total_queries * avg_input_tokens
    total_output_tokens = total_queries * avg_output_tokens

    # Handle on-premise deployment differently
    if params.deployment_type == "on_premise":
        # Find GPU type for this model from LLM_CATEGORIES
        from config.service_tiers import LLM_CATEGORIES

        gpu_type = "A100"  # Default
        for category in LLM_CATEGORIES.values():
            for model in category.get("on_premise", []):
                if model["id"] == params.llm_model:
                    gpu_type = model.get("gpu_type", "A100")
                    break

        # Calculate hours needed per month (rough estimate based on query load)
        # Assuming 1 query takes ~2 seconds on average
        hours_per_month = (total_queries * 2) / 3600  # Convert seconds to hours
        hours_per_month = max(730, hours_per_month)  # Minimum of full month (730 hours)

        # Use hourly GPU cost
        from config.service_tiers import GPU_COSTS
        monthly_cost_usd = GPU_COSTS[gpu_type]["hourly_cost"] * hours_per_month

        # Convert USD to AUD
        monthly_cost_aud = monthly_cost_usd / AUD_TO_USD
    else:
        # Cloud API - Calculate LLM costs using token pricing
        llm_total, _ = calculate_llm_costs(
            llm_mix={params.llm_model: 100.0},  # 100% of this single model
            total_queries=total_queries,
            avg_input_tokens=avg_input_tokens,
            avg_output_tokens=avg_output_tokens,
            cache_hit_rate=params.cache_hit_rate,
            use_prompt_caching=params.use_prompt_caching
        )
        monthly_cost_aud = llm_total

    return AgentCostResponse(
        agent_llm_cost_monthly=monthly_cost_aud,
        agent_llm_cost_annual=monthly_cost_aud * 12,
        total_queries_per_month=total_queries,
        total_input_tokens_per_month=total_input_tokens,
        total_output_tokens_per_month=total_output_tokens,
        llm_model=params.llm_model,
        deployment_type=params.deployment_type
    )
