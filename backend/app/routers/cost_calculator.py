from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum

router = APIRouter()


class VMSize(str, Enum):
    D4S_V5 = "Standard_D4s_v5"  # 4 vCPU, 16 GB
    D8S_V5 = "Standard_D8s_v5"  # 8 vCPU, 32 GB
    D16S_V5 = "Standard_D16s_v5"  # 16 vCPU, 64 GB
    NC6S_V3 = "Standard_NC6s_v3"  # GPU: V100 16GB


class LLMModel(str, Enum):
    GPT4O = "gpt-4o"
    GPT4_TURBO = "gpt-4-turbo"
    CLAUDE_OPUS = "claude-3.5-opus"
    CLAUDE_SONNET = "claude-3.5-sonnet"
    LLAMA_70B = "llama-3.1-70b"


class CostCalculatorRequest(BaseModel):
    # User Parameters
    num_users: int = Field(default=100, ge=1, le=10000, description="Number of sales reps")
    queries_per_user_per_month: int = Field(default=1000, ge=100, le=10000)
    avg_input_tokens: int = Field(default=10000, ge=1000, le=100000)
    avg_output_tokens: int = Field(default=1000, ge=100, le=10000)

    # Infrastructure Parameters
    aks_agent_nodes_baseline: int = Field(default=10, ge=3, le=100)
    aks_gpu_nodes_baseline: int = Field(default=3, ge=0, le=20)

    # Database Parameters
    azure_sql_vcores: int = Field(default=16, ge=4, le=128)
    cosmosdb_ru_baseline: int = Field(default=50000, ge=10000, le=1000000)
    neo4j_cluster_size: int = Field(default=3, ge=1, le=5)

    # Storage Parameters
    adls_hot_tier_tb: int = Field(default=20, ge=1, le=1000)
    adls_cool_tier_tb: int = Field(default=150, ge=10, le=5000)

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

    # Premium Data Sources
    use_zoominfo: bool = Field(default=True)
    use_linkedin_sales_nav: bool = Field(default=True)
    use_clearbit: bool = Field(default=True)


class CostBreakdown(BaseModel):
    category: str
    subcategory: str
    monthly_cost: float
    annual_cost: float
    unit: str
    quantity: float
    notes: str


class CostCalculatorResponse(BaseModel):
    # Summary
    total_monthly_cost: float
    total_annual_cost: float
    cost_per_user_monthly: float
    cost_per_user_annual: float

    # Fixed vs Variable
    fixed_monthly_cost: float
    variable_monthly_cost: float

    # Detailed Breakdown
    compute_costs: float
    storage_costs: float
    database_costs: float
    networking_costs: float
    llm_costs: float
    data_source_costs: float
    monitoring_costs: float

    # Detailed Line Items
    breakdown: List[CostBreakdown]

    # Metrics
    queries_per_month: int
    tokens_per_month: int
    estimated_data_size_gb: float

    # ROI
    roi_analysis: Dict


# Pricing Constants (Azure East US 2, as of Oct 2025)
PRICING = {
    "vm": {
        "Standard_D4s_v5": {"payg": 0.288, "reserved_1yr": 0.173},
        "Standard_D8s_v5": {"payg": 0.576, "reserved_1yr": 0.346},
        "Standard_D16s_v5": {"payg": 1.152, "reserved_1yr": 0.691},
        "Standard_NC6s_v3": {"payg": 3.36, "reserved_1yr": 2.016},
    },
    "storage": {
        "adls_hot_gb": 0.0184,
        "adls_cool_gb": 0.01,
        "blob_premium_gb": 0.1472,
        "blob_cool_gb": 0.01,
    },
    "database": {
        "sql_vcore_bc": 282.06,  # per vCore per month (Business Critical)
        "cosmosdb_ru_100": 0.008,  # per 100 RU/s per hour
        "neo4j_enterprise_monthly": 6000,
        "redis_p3_shard": 1107,
    },
    "networking": {
        "apim_premium_unit": 2799.50,
        "front_door_base": 330,
        "firewall_deployment_hour": 1.25,
        "private_endpoint": 7.30,
    },
    "llm": {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "claude-3.5-opus": {"input": 15.00, "output": 75.00},
        "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
        "claude-sonnet-cache-write": 3.75,
        "claude-sonnet-cache-read": 0.30,
        "text-embedding-3-small": 0.02,
        "llama-3.1-70b": {"input": 0.00, "output": 0.00},  # Self-hosted, compute only
    },
    "data_sources": {
        "zoominfo": 14999,  # annual / 12
        "linkedin_sales_nav": 99.99,  # per user/month
        "clearbit": 999,  # per month
        "pitchbook": 2999,  # per month
    }
}


def calculate_compute_costs(params: CostCalculatorRequest) -> tuple[float, List[CostBreakdown]]:
    """Calculate AKS compute costs"""
    costs = []
    total = 0

    use_reserved = params.use_reserved_instances
    pricing_key = "reserved_1yr" if use_reserved else "payg"

    # System nodes (always 3)
    vm_price = PRICING["vm"]["Standard_D4s_v5"][pricing_key]
    monthly = vm_price * 24 * 30 * 3
    total += monthly
    costs.append(CostBreakdown(
        category="Compute",
        subcategory="AKS System Nodes",
        monthly_cost=monthly,
        annual_cost=monthly * 12,
        unit="nodes",
        quantity=3,
        notes=f"Standard_D4s_v5, {pricing_key}"
    ))

    # Agent nodes
    vm_price = PRICING["vm"]["Standard_D8s_v5"][pricing_key]
    monthly = vm_price * 24 * 30 * params.aks_agent_nodes_baseline
    total += monthly
    costs.append(CostBreakdown(
        category="Compute",
        subcategory="AKS Agent Nodes",
        monthly_cost=monthly,
        annual_cost=monthly * 12,
        unit="nodes",
        quantity=params.aks_agent_nodes_baseline,
        notes=f"Standard_D8s_v5, {pricing_key}, auto-scale baseline"
    ))

    # GPU nodes (if any)
    if params.aks_gpu_nodes_baseline > 0:
        vm_price = PRICING["vm"]["Standard_NC6s_v3"][pricing_key]
        monthly = vm_price * 24 * 30 * params.aks_gpu_nodes_baseline
        total += monthly
        costs.append(CostBreakdown(
            category="Compute",
            subcategory="AKS GPU Nodes (Llama)",
            monthly_cost=monthly,
            annual_cost=monthly * 12,
            unit="nodes",
            quantity=params.aks_gpu_nodes_baseline,
            notes=f"Standard_NC6s_v3 (V100), {pricing_key}"
        ))

    # Azure Functions
    functions_cost = 369  # Fixed based on Premium EP2
    total += functions_cost
    costs.append(CostBreakdown(
        category="Compute",
        subcategory="Azure Functions",
        monthly_cost=functions_cost,
        annual_cost=functions_cost * 12,
        unit="instances",
        quantity=2,
        notes="Premium EP2, always ready"
    ))

    # Databricks (usage-based, estimate)
    databricks_cost = 2477  # Fixed for ETL jobs
    total += databricks_cost
    costs.append(CostBreakdown(
        category="Compute",
        subcategory="Databricks",
        monthly_cost=databricks_cost,
        annual_cost=databricks_cost * 12,
        unit="hours",
        quantity=200,
        notes="200 hours/month, Standard_D32s_v5 workers"
    ))

    return total, costs


def calculate_storage_costs(params: CostCalculatorRequest) -> tuple[float, List[CostBreakdown]]:
    """Calculate storage costs"""
    costs = []
    total = 0

    # ADLS Hot Tier
    hot_storage = params.adls_hot_tier_tb * 1000 * PRICING["storage"]["adls_hot_gb"]
    hot_ops = 65 + 32.50  # Write + Read operations (estimated)
    hot_total = (hot_storage + hot_ops) * 2  # 2x for GRS
    total += hot_total
    costs.append(CostBreakdown(
        category="Storage",
        subcategory="ADLS Hot Tier",
        monthly_cost=hot_total,
        annual_cost=hot_total * 12,
        unit="TB",
        quantity=params.adls_hot_tier_tb,
        notes="Includes GRS replication, operations"
    ))

    # ADLS Cool Tier
    cool_storage = params.adls_cool_tier_tb * 1000 * PRICING["storage"]["adls_cool_gb"]
    cool_ops = 10 + 5
    cool_total = (cool_storage + cool_ops) * 2
    total += cool_total
    costs.append(CostBreakdown(
        category="Storage",
        subcategory="ADLS Cool Tier",
        monthly_cost=cool_total,
        annual_cost=cool_total * 12,
        unit="TB",
        quantity=params.adls_cool_tier_tb,
        notes="Includes GRS replication, operations"
    ))

    # Blob Storage (fixed estimate)
    blob_cost = 1657
    total += blob_cost
    costs.append(CostBreakdown(
        category="Storage",
        subcategory="Blob Storage",
        monthly_cost=blob_cost,
        annual_cost=blob_cost * 12,
        unit="GB",
        quantity=100000,
        notes="Premium + Cool tiers, documents & recordings"
    ))

    return total, costs


def calculate_database_costs(params: CostCalculatorRequest) -> tuple[float, List[CostBreakdown]]:
    """Calculate database costs"""
    costs = []
    total = 0

    # Azure SQL Database
    sql_compute = params.azure_sql_vcores * PRICING["database"]["sql_vcore_bc"]
    sql_storage = 2000 * 0.25  # 2 TB at $0.25/GB
    sql_backup = 2000 * 0.20   # Backup storage
    sql_total = sql_compute + sql_storage + sql_backup
    total += sql_total
    costs.append(CostBreakdown(
        category="Database",
        subcategory="Azure SQL (Business Critical)",
        monthly_cost=sql_total,
        annual_cost=sql_total * 12,
        unit="vCores",
        quantity=params.azure_sql_vcores,
        notes=f"Includes 2TB storage, 3 replicas, zone redundancy"
    ))

    # Cosmos DB
    cosmos_ru_cost = (params.cosmosdb_ru_baseline / 100) * PRICING["database"]["cosmosdb_ru_100"] * 24 * 30
    cosmos_regions = 3  # Multi-region
    cosmos_storage = 500 * 0.25 * cosmos_regions
    cosmos_total = (cosmos_ru_cost * cosmos_regions) + cosmos_storage
    total += cosmos_total
    costs.append(CostBreakdown(
        category="Database",
        subcategory="Cosmos DB",
        monthly_cost=cosmos_total,
        annual_cost=cosmos_total * 12,
        unit="RU/s",
        quantity=params.cosmosdb_ru_baseline,
        notes=f"Multi-region (3), 500GB data, Strong consistency"
    ))

    # Neo4j Enterprise
    neo4j_license = PRICING["database"]["neo4j_enterprise_monthly"]
    neo4j_storage = params.neo4j_cluster_size * 122.88  # Premium SSD per node
    neo4j_total = neo4j_license + neo4j_storage
    total += neo4j_total
    costs.append(CostBreakdown(
        category="Database",
        subcategory="Neo4j Enterprise",
        monthly_cost=neo4j_total,
        annual_cost=neo4j_total * 12,
        unit="nodes",
        quantity=params.neo4j_cluster_size,
        notes="Enterprise license, causal cluster, 1TB per node"
    ))

    # Milvus (open source, storage only)
    milvus_storage = 2 * 122.88  # 2 TB
    total += milvus_storage
    costs.append(CostBreakdown(
        category="Database",
        subcategory="Milvus Vector DB",
        monthly_cost=milvus_storage,
        annual_cost=milvus_storage * 12,
        unit="TB",
        quantity=2,
        notes="Open source, storage cost only"
    ))

    # Redis Premium
    redis_shards = 10
    redis_total = redis_shards * PRICING["database"]["redis_p3_shard"]
    redis_geo = redis_total * 0.5  # Geo-replication
    redis_total += redis_geo
    total += redis_total
    costs.append(CostBreakdown(
        category="Database",
        subcategory="Azure Cache for Redis",
        monthly_cost=redis_total,
        annual_cost=redis_total * 12,
        unit="shards",
        quantity=redis_shards,
        notes="Premium P3, cluster mode, geo-replication"
    ))

    return total, costs


def calculate_networking_costs() -> tuple[float, List[CostBreakdown]]:
    """Calculate networking costs (mostly fixed)"""
    costs = []
    total = 0

    # API Management
    apim = PRICING["networking"]["apim_premium_unit"] * 2
    total += apim
    costs.append(CostBreakdown(
        category="Networking",
        subcategory="API Management",
        monthly_cost=apim,
        annual_cost=apim * 12,
        unit="units",
        quantity=2,
        notes="Premium tier, multi-region"
    ))

    # Front Door
    front_door = 1600  # Base + WAF + traffic
    total += front_door
    costs.append(CostBreakdown(
        category="Networking",
        subcategory="Azure Front Door",
        monthly_cost=front_door,
        annual_cost=front_door * 12,
        unit="service",
        quantity=1,
        notes="Premium, WAF, DDoS protection"
    ))

    # Firewall
    firewall = PRICING["networking"]["firewall_deployment_hour"] * 2 * 24 * 30 + 328
    total += firewall
    costs.append(CostBreakdown(
        category="Networking",
        subcategory="Azure Firewall",
        monthly_cost=firewall,
        annual_cost=firewall * 12,
        unit="deployments",
        quantity=2,
        notes="Premium tier, TLS inspection, IDPS"
    ))

    # Private Link
    private_link = 10 * PRICING["networking"]["private_endpoint"] + 102.40
    total += private_link
    costs.append(CostBreakdown(
        category="Networking",
        subcategory="Private Link",
        monthly_cost=private_link,
        annual_cost=private_link * 12,
        unit="endpoints",
        quantity=10,
        notes="Private endpoints for databases, storage"
    ))

    return total, costs


def calculate_llm_costs(params: CostCalculatorRequest) -> tuple[float, List[CostBreakdown]]:
    """Calculate LLM and AI model costs"""
    costs = []
    total = 0

    total_queries = params.num_users * params.queries_per_user_per_month

    # Calculate cached vs fresh queries
    cached_queries = int(total_queries * params.cache_hit_rate)
    fresh_queries = total_queries - cached_queries

    # Cached queries cost (if using prompt caching)
    if params.use_prompt_caching:
        # Assume 90% of context is cached with Claude
        cached_token_ratio = 0.90
        fresh_token_ratio = 0.10

        cached_input = params.avg_input_tokens * cached_token_ratio
        fresh_input = params.avg_input_tokens * fresh_token_ratio

        # Cached reads (90% discount)
        claude_cache_cost = (
            cached_queries *
            (cached_input / 1_000_000 * PRICING["llm"]["claude-sonnet-cache-read"] +
             fresh_input / 1_000_000 * PRICING["llm"]["claude-3.5-sonnet"]["input"] +
             params.avg_output_tokens / 1_000_000 * PRICING["llm"]["claude-3.5-sonnet"]["output"])
        )
        total += claude_cache_cost
        costs.append(CostBreakdown(
            category="AI/LLM",
            subcategory="Cached Queries (Claude)",
            monthly_cost=claude_cache_cost,
            annual_cost=claude_cache_cost * 12,
            unit="queries",
            quantity=cached_queries,
            notes=f"90% cache hit, prompt caching enabled"
        ))

    # Fresh queries - distributed by LLM mix
    for model, percentage in params.llm_mix.items():
        if percentage == 0:
            continue

        model_queries = int(fresh_queries * (percentage / 100))

        if model == "llama-3.1-70b":
            # Local model - no per-token cost, just GPU infrastructure
            costs.append(CostBreakdown(
                category="AI/LLM",
                subcategory=f"Llama 3.1 70B ({percentage}%)",
                monthly_cost=0,
                annual_cost=0,
                unit="queries",
                quantity=model_queries,
                notes="Self-hosted on GPU nodes, cost in compute"
            ))
        else:
            pricing_key = model
            if "claude" in model:
                pricing_key = "claude-3.5-sonnet" if "sonnet" in model else "claude-3.5-opus"

            model_cost = (
                model_queries *
                (params.avg_input_tokens / 1_000_000 * PRICING["llm"][pricing_key]["input"] +
                 params.avg_output_tokens / 1_000_000 * PRICING["llm"][pricing_key]["output"])
            )
            total += model_cost
            costs.append(CostBreakdown(
                category="AI/LLM",
                subcategory=f"{model.upper()} ({percentage}%)",
                monthly_cost=model_cost,
                annual_cost=model_cost * 12,
                unit="queries",
                quantity=model_queries,
                notes=f"Fresh queries, {params.avg_input_tokens}in + {params.avg_output_tokens}out tokens"
            ))

    # Embeddings
    total_embeddings = params.num_users * 5000  # 5K embeddings per user/month (documents, emails)
    embedding_cost = total_embeddings * 1000 / 1_000_000 * PRICING["llm"]["text-embedding-3-small"]
    total += embedding_cost
    costs.append(CostBreakdown(
        category="AI/LLM",
        subcategory="Embeddings (OpenAI)",
        monthly_cost=embedding_cost,
        annual_cost=embedding_cost * 12,
        unit="tokens",
        quantity=total_embeddings * 1000,
        notes="text-embedding-3-small for vector search"
    ))

    return total, costs


def calculate_data_source_costs(params: CostCalculatorRequest) -> tuple[float, List[CostBreakdown]]:
    """Calculate premium data source costs"""
    costs = []
    total = 0

    if params.use_zoominfo:
        zoominfo = PRICING["data_sources"]["zoominfo"]
        total += zoominfo
        costs.append(CostBreakdown(
            category="Data Sources",
            subcategory="ZoomInfo",
            monthly_cost=zoominfo,
            annual_cost=zoominfo * 12,
            unit="subscription",
            quantity=1,
            notes="Enterprise plan, contact data"
        ))

    if params.use_linkedin_sales_nav:
        linkedin = PRICING["data_sources"]["linkedin_sales_nav"] * params.num_users
        total += linkedin
        costs.append(CostBreakdown(
            category="Data Sources",
            subcategory="LinkedIn Sales Navigator",
            monthly_cost=linkedin,
            annual_cost=linkedin * 12,
            unit="users",
            quantity=params.num_users,
            notes="Per user/month"
        ))

    if params.use_clearbit:
        clearbit = PRICING["data_sources"]["clearbit"]
        total += clearbit
        costs.append(CostBreakdown(
            category="Data Sources",
            subcategory="Clearbit",
            monthly_cost=clearbit,
            annual_cost=clearbit * 12,
            unit="subscription",
            quantity=1,
            notes="Enrichment API"
        ))

    return total, costs


def calculate_monitoring_costs() -> tuple[float, List[CostBreakdown]]:
    """Calculate monitoring and observability costs"""
    costs = []
    total = 0

    # Azure Monitor
    monitor = 7044
    total += monitor
    costs.append(CostBreakdown(
        category="Monitoring",
        subcategory="Azure Monitor",
        monthly_cost=monitor,
        annual_cost=monitor * 12,
        unit="GB",
        quantity=800,
        notes="Logs, metrics, traces, 90-day retention"
    ))

    # Grafana Cloud
    grafana = 1469
    total += grafana
    costs.append(CostBreakdown(
        category="Monitoring",
        subcategory="Grafana Cloud",
        monthly_cost=grafana,
        annual_cost=grafana * 12,
        unit="users",
        quantity=20,
        notes="Pro plan, custom dashboards"
    ))

    # LangSmith
    langsmith = 2500
    total += langsmith
    costs.append(CostBreakdown(
        category="Monitoring",
        subcategory="LangSmith",
        monthly_cost=langsmith,
        annual_cost=langsmith * 12,
        unit="traces",
        quantity=10000000,
        notes="LLM observability, 10M traces/month"
    ))

    # Security (Defender, Key Vault)
    security = 881 + 251
    total += security
    costs.append(CostBreakdown(
        category="Monitoring",
        subcategory="Security (Defender + Key Vault)",
        monthly_cost=security,
        annual_cost=security * 12,
        unit="services",
        quantity=1,
        notes="Defender for Cloud, Key Vault Premium"
    ))

    return total, costs


def calculate_roi(total_annual_cost: float, num_users: int) -> Dict:
    """Calculate ROI based on sales improvement metrics"""

    cost_per_user_annual = total_annual_cost / num_users

    # Conservative estimates based on industry benchmarks
    assumptions = {
        "avg_deal_size_before": 50000,
        "avg_deals_per_rep_per_year": 20,
        "deal_size_increase_pct": 30,  # 30% increase
        "win_rate_before": 0.20,
        "win_rate_increase_pct": 35,  # 35% improvement in win rate
        "sales_cycle_reduction_days": 30,  # 30 days faster
        "time_saved_hours_per_week": 10,  # 10 hours/week saved on research
    }

    # Calculate revenue impact
    revenue_before = (
        assumptions["avg_deal_size_before"] *
        assumptions["avg_deals_per_rep_per_year"] *
        assumptions["win_rate_before"]
    )

    new_deal_size = assumptions["avg_deal_size_before"] * (1 + assumptions["deal_size_increase_pct"] / 100)
    new_win_rate = assumptions["win_rate_before"] * (1 + assumptions["win_rate_increase_pct"] / 100)

    revenue_after = new_deal_size * assumptions["avg_deals_per_rep_per_year"] * new_win_rate

    additional_revenue_per_rep = revenue_after - revenue_before
    total_additional_revenue = additional_revenue_per_rep * num_users

    # ROI calculation
    roi_percentage = ((total_additional_revenue - total_annual_cost) / total_annual_cost) * 100
    payback_months = (total_annual_cost / total_additional_revenue) * 12

    return {
        "cost_per_user_annual": round(cost_per_user_annual, 2),
        "revenue_before_per_rep": round(revenue_before, 2),
        "revenue_after_per_rep": round(revenue_after, 2),
        "additional_revenue_per_rep": round(additional_revenue_per_rep, 2),
        "total_additional_revenue": round(total_additional_revenue, 2),
        "roi_percentage": round(roi_percentage, 2),
        "roi_ratio": f"{round(total_additional_revenue / total_annual_cost, 1)}:1",
        "payback_months": round(payback_months, 1),
        "assumptions": assumptions
    }


@router.post("/calculate", response_model=CostCalculatorResponse)
async def calculate_costs(params: CostCalculatorRequest):
    """
    Calculate comprehensive costs for Sales Coach AI Agent deployment
    """

    try:
        # Calculate all cost categories
        compute_total, compute_breakdown = calculate_compute_costs(params)
        storage_total, storage_breakdown = calculate_storage_costs(params)
        database_total, database_breakdown = calculate_database_costs(params)
        networking_total, networking_breakdown = calculate_networking_costs()
        llm_total, llm_breakdown = calculate_llm_costs(params)
        data_source_total, data_source_breakdown = calculate_data_source_costs(params)
        monitoring_total, monitoring_breakdown = calculate_monitoring_costs()

        # DevOps (fixed)
        devops_total = 586 + 756 + 0  # Azure DevOps + ACR
        devops_breakdown = [
            CostBreakdown(
                category="DevOps",
                subcategory="Azure DevOps + ACR",
                monthly_cost=devops_total,
                annual_cost=devops_total * 12,
                unit="services",
                quantity=1,
                notes="Pipelines, repos, container registry"
            )
        ]

        # Aggregate
        all_breakdowns = (
            compute_breakdown +
            storage_breakdown +
            database_breakdown +
            networking_breakdown +
            llm_breakdown +
            data_source_breakdown +
            monitoring_breakdown +
            devops_breakdown
        )

        # Calculate fixed vs variable
        # Fixed: Infrastructure that runs regardless of usage
        fixed_monthly = (
            compute_total +
            storage_total +
            database_total +
            networking_total +
            monitoring_total +
            devops_total
        )

        # Variable: Usage-based costs (LLM, data sources scale with users)
        variable_monthly = llm_total + data_source_total

        total_monthly = fixed_monthly + variable_monthly
        total_annual = total_monthly * 12

        cost_per_user_monthly = total_monthly / params.num_users
        cost_per_user_annual = total_annual / params.num_users

        # Calculate metrics
        queries_per_month = params.num_users * params.queries_per_user_per_month
        tokens_per_month = queries_per_month * (params.avg_input_tokens + params.avg_output_tokens)
        estimated_data_size_gb = params.adls_hot_tier_tb * 1000 + params.adls_cool_tier_tb * 1000

        # ROI analysis
        roi_analysis = calculate_roi(total_annual, params.num_users)

        return CostCalculatorResponse(
            total_monthly_cost=round(total_monthly, 2),
            total_annual_cost=round(total_annual, 2),
            cost_per_user_monthly=round(cost_per_user_monthly, 2),
            cost_per_user_annual=round(cost_per_user_annual, 2),
            fixed_monthly_cost=round(fixed_monthly, 2),
            variable_monthly_cost=round(variable_monthly, 2),
            compute_costs=round(compute_total, 2),
            storage_costs=round(storage_total, 2),
            database_costs=round(database_total, 2),
            networking_costs=round(networking_total, 2),
            llm_costs=round(llm_total, 2),
            data_source_costs=round(data_source_total, 2),
            monitoring_costs=round(monitoring_total, 2),
            breakdown=all_breakdowns,
            queries_per_month=queries_per_month,
            tokens_per_month=tokens_per_month,
            estimated_data_size_gb=round(estimated_data_size_gb, 2),
            roi_analysis=roi_analysis
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/defaults", response_model=CostCalculatorRequest)
async def get_defaults():
    """Get default configuration parameters"""
    return CostCalculatorRequest()
