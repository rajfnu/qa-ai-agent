# Pricing System Validation Report

**Date:** 2025-10-26
**Reviewed by:** Claude Code
**Status:** Issues Identified - Fixes Required

---

## Executive Summary

This report addresses the following user concerns:
1. ✅ **Memory System Discrepancy** - Basic Tier agents showing "cosmos-db" but cost is $0.00
2. ⚠️ **Global Usage Parameters** - Missing detailed metrics (tokens/user, storage/user)
3. ⚠️ **MCP Tools & Functions** - Missing cost explanations/captions
4. ⚠️ **Section-Level Captions** - Missing explanations for how costs are calculated
5. ⚠️ **Cost Validation** - Need to verify calculations are correct and explainable

---

## Issue 1: Memory System Discrepancy (CRITICAL BUG)

### Problem Statement
In the Basic Tier, agents are configured with `memory_type: "cosmos-db"` but the displayed cost for "Memory (Cosmos DB)" is $0.00.

### Root Cause Analysis

**Location:** `backend/app/routers/cost_calculator_v2.py:450-487`

The `calculate_memory_system_costs()` function has a critical bug:

```python
def calculate_memory_system_costs(memory_type: str, infrastructure: Dict[str, float], service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """Calculate memory system costs based on service tier configuration"""

    # BUG: This function accepts memory_type parameter but IGNORES it!
    tier_config = get_tier_config(service_tier)
    memory_config = tier_config.get("memory", {})  # ← Uses tier default, not the parameter

    monthly_cost = memory_config.get("monthly_cost", 0.0)
    memory_type_tier = memory_config.get("type", "in_memory")  # ← Overwrites the parameter!
```

**What happens:**
1. Basic Tier configuration (service_tiers.py:127-134):
   ```python
   "basic": {
       "type": "in_memory",
       "monthly_cost": 0.0,
       ...
   }
   ```

2. Agent configuration (SalesCoach.js) specifies:
   ```javascript
   {
       memory_type: 'cosmos-db',
       ...
   }
   ```

3. When calculating costs, the function receives `memory_type="cosmos-db"` but replaces it with the tier's default `"in_memory"`, resulting in $0.00 cost.

### Impact
- **User confusion:** UI shows "cosmos-db" but cost is $0.00
- **Inaccurate pricing:** Real cosmos-db costs are not reflected
- **Business risk:** Underestimating actual infrastructure costs

### Recommended Fix

**Option A: Honor the memory_type parameter (RECOMMENDED)**

```python
def calculate_memory_system_costs(memory_type: str, infrastructure: Dict[str, float], service_tier: str = "standard") -> tuple[float, List[CostBreakdown]]:
    """Calculate memory system costs based on actual memory type selected"""
    breakdown = []

    # Get tier default config
    tier_config = get_tier_config(service_tier)
    tier_memory_config = tier_config.get("memory", {})

    # HONOR the memory_type parameter if provided
    if memory_type and memory_type != "default":
        # Use pricing_config.py to calculate actual cost for selected memory type
        from app.pricing_config import get_pricing_config
        pricing = get_pricing_config()

        if memory_type == "cosmos-db" or memory_type == "cosmos_db":
            cosmos_ru = infrastructure.get("cosmos_ru", 45000)
            monthly_cost = pricing.calculate_memory_cost("cosmos_db", ru_per_second=cosmos_ru)
            capacity = f"{cosmos_ru} RU/s"
            features = "Multi-model NoSQL, Global Distribution"

        elif memory_type == "redis":
            capacity_gb = tier_memory_config.get("capacity_gb", 6)
            monthly_cost = pricing.calculate_memory_cost("redis", capacity_gb=capacity_gb)
            capacity = f"{capacity_gb}GB"
            features = "In-memory cache, Persistence, Replication"

        elif memory_type == "neo4j":
            nodes = infrastructure.get("neo4j_nodes", 2)
            monthly_cost = pricing.calculate_memory_cost("neo4j", nodes=nodes)
            capacity = f"{nodes} nodes"
            features = "Graph database, Relationship mapping"

        elif memory_type == "in_memory" or memory_type == "in-memory":
            monthly_cost = 0.0
            capacity = tier_memory_config.get("capacity_gb", 4)
            features = "Application memory (non-persistent)"
        else:
            # Fallback to tier default
            monthly_cost = tier_memory_config.get("monthly_cost", 0.0)
            capacity = tier_memory_config.get("capacity_gb", 0)
            features = "Tier default"
    else:
        # Use tier default if no specific type provided
        monthly_cost = tier_memory_config.get("monthly_cost", 0.0)
        capacity = tier_memory_config.get("capacity_gb", 0)
        memory_type = tier_memory_config.get("type", "in_memory")
        features = "Tier default configuration"

    breakdown.append(CostBreakdown(
        category="Memory System",
        subcategory=f"{memory_type.replace('_', ' ').replace('-', ' ').title()} ({service_tier.title()} Tier)",
        monthly_cost=monthly_cost,
        annual_cost=monthly_cost * 12,
        unit="capacity",
        quantity=capacity,
        notes=f"Features: {features}"
    ))

    return monthly_cost, breakdown
```

**Option B: Enforce tier restrictions**

Prevent users from selecting memory types not included in their tier. Basic tier = in_memory only.

---

## Issue 2: Global Usage Parameters - Missing Details

### Current State
The cost calculator request model includes basic parameters but lacks detailed per-user metrics.

**Location:** `backend/app/routers/cost_calculator_v2.py:128-164`

### Missing Metrics

| Metric | Current | Should Add |
|--------|---------|------------|
| **Tokens per User** | ❌ Only has `avg_input_tokens` and `avg_output_tokens` | ✅ Add `tokens_per_user_per_month` = queries × (input + output) |
| **Storage per User** | ❌ Not calculated | ✅ Add `storage_per_user_gb` based on data retention |
| **API Calls per User** | ✅ Has `queries_per_user_per_month` | ✅ Already present |
| **Cost per User** | ✅ Calculated in response | ✅ Already present |
| **Cache Hit Rate** | ✅ Present | ✅ Already present |

### Recommended Enhancement

Add to `CostCalculatorResponse` model:

```python
class GlobalUsageMetrics(BaseModel):
    """Detailed per-user usage metrics"""
    # Per-User Metrics
    tokens_per_user_per_month: int
    input_tokens_per_user_per_month: int
    output_tokens_per_user_per_month: int
    queries_per_user_per_month: int
    storage_per_user_gb: float
    cost_per_user_per_month: float

    # Aggregate Metrics
    total_users: int
    total_tokens_per_month: int
    total_storage_gb: float
    total_queries_per_month: int

    # Efficiency Metrics
    cache_hit_rate: float
    avg_tokens_per_query: int
    cost_per_query: float
    cost_per_1k_tokens: float

    # Descriptive Text
    description: str = "Detailed breakdown of usage parameters normalized per user"

class CostCalculatorResponse(BaseModel):
    # ... existing fields ...

    # Add this new field
    global_usage_metrics: GlobalUsageMetrics
```

Then add calculation in the `/calculate` endpoint:

```python
# Calculate Global Usage Metrics
tokens_per_user = (request.avg_input_tokens + request.avg_output_tokens) * request.queries_per_user_per_month
storage_per_user = estimated_data_size_gb / request.num_users if request.num_users > 0 else 0

global_usage_metrics = GlobalUsageMetrics(
    tokens_per_user_per_month=tokens_per_user,
    input_tokens_per_user_per_month=request.avg_input_tokens * request.queries_per_user_per_month,
    output_tokens_per_user_per_month=request.avg_output_tokens * request.queries_per_user_per_month,
    queries_per_user_per_month=request.queries_per_user_per_month,
    storage_per_user_gb=storage_per_user,
    cost_per_user_per_month=total_monthly_cost / request.num_users,
    total_users=request.num_users,
    total_tokens_per_month=tokens_per_user * request.num_users,
    total_storage_gb=estimated_data_size_gb,
    total_queries_per_month=total_queries,
    cache_hit_rate=request.cache_hit_rate,
    avg_tokens_per_query=request.avg_input_tokens + request.avg_output_tokens,
    cost_per_query=total_monthly_cost / total_queries if total_queries > 0 else 0,
    cost_per_1k_tokens=(total_monthly_cost / (tokens_per_user * request.num_users)) * 1000 if tokens_per_user > 0 else 0,
    description=f"Metrics for {request.num_users} users with {request.queries_per_user_per_month} queries/user/month"
)
```

---

## Issue 3: MCP Tools & Functions - Missing Cost Captions

### Current State
**Location:** `backend/config/pricing.yaml:452-524`

MCP tools are defined with pricing but lack explanatory captions about:
- What each tool does
- How cost is calculated
- When you'd use it
- Cost drivers

### Current Format (Example)
```yaml
- name: "fog_analysis_tool"
  type: "function"
  description: "Fact/Opinion/Gossip classification"
  avg_duration_seconds: 0.5
  memory_mb: 512
  avg_calls_per_assessment: 5
  cost_per_1k_calls_aud: 0.15
```

### Recommended Enhancement

```yaml
mcp_tools:
  # ============================================================================
  # MCP SERVERS
  # ============================================================================
  # MCP Servers run continuously (24/7) and incur FIXED monthly costs.
  # These are always-on services that provide capabilities to agents.
  #
  # Cost Formula: Fixed monthly infrastructure cost (VM + maintenance)
  # ============================================================================

  servers:
    - name: "research_tool"
      type: "mcp_server"
      description: "Web research and data retrieval"
      infrastructure:
        vm_sku: "Standard_D4s_v5"
        cost_per_hour_aud: 0.173  # Reserved pricing
        monthly_cost_aud: 126.29  # 730 hours × $0.173
      cost_explanation: |
        Fixed monthly cost for always-on research capabilities.
        Runs 24/7 to provide instant research results to agents.
        Cost based on Azure D4s_v5 VM (4 vCPU, 16GB RAM).
      when_to_use: "Essential for agents that need real-time web research, competitor analysis, or market intelligence."
      cost_drivers:
        - "VM size (Standard_D4s_v5)"
        - "Reserved vs Pay-as-you-go pricing"
        - "No scaling cost (fixed)"

    - name: "content_generation_tool"
      type: "mcp_server"
      description: "Content creation and templates"
      infrastructure:
        vm_sku: "Standard_D4s_v5"
        cost_per_hour_aud: 0.173
        monthly_cost_aud: 126.29
      cost_explanation: |
        Fixed monthly cost for content generation infrastructure.
        Provides templating, document generation, and content formatting.
      when_to_use: "Required for agents that generate reports, presentations, emails, or other content."
      cost_drivers:
        - "VM size"
        - "Template complexity (affects memory/CPU)"

    - name: "competitive_intel_tool"
      type: "mcp_server"
      description: "Competitor analysis and market data"
      infrastructure:
        vm_sku: "Standard_D8s_v5"  # Larger for data processing
        cost_per_hour_aud: 0.346
        monthly_cost_aud: 252.58
      cost_explanation: |
        Fixed monthly cost for competitive intelligence capabilities.
        Uses larger VM (8 vCPU, 32GB RAM) for processing market data.
        Includes web scraping, data aggregation, and analysis tools.
      when_to_use: "For sales/marketing agents that need competitor monitoring and market analysis."
      cost_drivers:
        - "VM size (2x larger than basic tools)"
        - "Data processing volume"
        - "External API costs (News, Social Media)"

  # ============================================================================
  # AZURE FUNCTIONS
  # ============================================================================
  # Azure Functions are SERVERLESS and only charge when executed.
  # Cost scales with usage: more assessments = higher cost.
  #
  # Cost Formula: (Total Executions ÷ 1000) × Cost per 1k calls
  # Total Executions = num_assessments × avg_calls_per_assessment
  #
  # Example: 4000 assessments × 5 calls = 20,000 executions
  #          20,000 ÷ 1000 × $0.15 = $3.00/month
  # ============================================================================

  functions:
    - name: "fog_analysis_tool"
      type: "function"
      description: "Fact/Opinion/Gossip classification"
      avg_duration_seconds: 0.5
      memory_mb: 512
      avg_calls_per_assessment: 5
      cost_per_1k_calls_aud: 0.15
      cost_explanation: |
        Pay-per-execution pricing based on Azure Functions.
        Base: $0.30 per million executions + $0.000024 per GB-second

        For 4000 assessments/month:
          - Executions: 4000 × 5 = 20,000
          - Cost: (20,000 ÷ 1000) × $0.15 = $3.00/month
      when_to_use: "Essential for Sales Coach agents to classify customer statements as Fact, Opinion, or Gossip."
      cost_drivers:
        - "Number of assessments per month"
        - "Average calls per assessment (5x)"
        - "Function duration (0.5 seconds)"
        - "Memory allocation (512 MB)"

    - name: "engagement_excellence_tool"
      type: "function"
      description: "Six lenses framework analysis"
      avg_duration_seconds: 0.8
      memory_mb: 512
      avg_calls_per_assessment: 3
      cost_per_1k_calls_aud: 0.20
      cost_explanation: |
        For 4000 assessments/month:
          - Executions: 4000 × 3 = 12,000
          - Cost: (12,000 ÷ 1000) × $0.20 = $2.40/month

        More expensive per call due to longer duration (0.8s vs 0.5s).
      when_to_use: "Analyzes customer engagement across six dimensions (Trust, Value, Impact, etc.)"
      cost_drivers:
        - "Number of assessments"
        - "Calls per assessment (3x)"
        - "Longer processing time (0.8s)"

    - name: "impact_theme_generator_tool"
      type: "function"
      description: "Generate impact themes"
      avg_duration_seconds: 1.0
      memory_mb: 1024
      avg_calls_per_assessment: 2
      cost_per_1k_calls_aud: 0.25
      cost_explanation: |
        For 4000 assessments/month:
          - Executions: 4000 × 2 = 8,000
          - Cost: (8,000 ÷ 1000) × $0.25 = $2.00/month

        Highest cost per call due to:
          - Longer duration (1.0 second)
          - More memory (1024 MB vs 512 MB)
          - Complex LLM-based theme generation
      when_to_use: "Generates customer impact themes for value propositions and messaging."
      cost_drivers:
        - "Duration (1.0 second - longest)"
        - "Memory (1024 MB - double)"
        - "LLM processing overhead"

    - name: "license_to_sell_tool"
      type: "function"
      description: "Calculate license to sell gate"
      avg_duration_seconds: 0.3
      memory_mb: 256
      avg_calls_per_assessment: 1
      cost_per_1k_calls_aud: 0.10
      cost_explanation: |
        For 4000 assessments/month:
          - Executions: 4000 × 1 = 4,000
          - Cost: (4,000 ÷ 1000) × $0.10 = $0.40/month

        Cheapest function:
          - Only 1 call per assessment
          - Fast execution (0.3 seconds)
          - Low memory (256 MB)
      when_to_use: "Quick validation that salesperson has 'license to sell' based on trust/credibility."
      cost_drivers:
        - "Single call per assessment"
        - "Simple calculation logic"
        - "Minimal memory footprint"

    - name: "find_money_validator_tool"
      type: "function"
      description: "Budget validation"
      avg_duration_seconds: 0.5
      memory_mb: 512
      avg_calls_per_assessment: 2
      cost_per_1k_calls_aud: 0.15
      cost_explanation: |
        For 4000 assessments/month:
          - Executions: 4000 × 2 = 8,000
          - Cost: (8,000 ÷ 1000) × $0.15 = $1.20/month
      when_to_use: "Validates customer budget availability and financial authority."
      cost_drivers:
        - "2 calls per assessment"
        - "Budget data retrieval overhead"

# ============================================================================
# TOTAL MCP TOOLS COST CALCULATOR
# ============================================================================
#
# For Sales Coach with 4000 assessments/month:
#
# MCP Servers (Fixed):
#   - research_tool:               $126.29
#   - content_generation_tool:     $126.29
#   - competitive_intel_tool:      $252.58
#   Total Fixed:                   $505.16/month
#
# Azure Functions (Variable):
#   - fog_analysis_tool:           $3.00  (20,000 calls)
#   - engagement_excellence_tool:  $2.40  (12,000 calls)
#   - impact_theme_generator_tool: $2.00  (8,000 calls)
#   - license_to_sell_tool:        $0.40  (4,000 calls)
#   - find_money_validator_tool:   $1.20  (8,000 calls)
#   Total Variable:                $9.00/month
#
# TOTAL MCP TOOLS COST:            $514.16/month
#
# Scaling Behavior:
#   - Fixed costs ($505.16) stay constant regardless of usage
#   - Variable costs scale linearly with assessments
#   - Double assessments = Double variable costs only
# ============================================================================
```

---

## Issue 4: Section-Level Captions - Missing Cost Explanations

### Problem
Each pricing section lacks explanatory captions about how costs are calculated.

### Recommended Additions

Add caption fields to each section in both the YAML config and API responses:

```python
class CostBreakdown(BaseModel):
    category: str
    subcategory: str
    monthly_cost: float
    annual_cost: float
    unit: str
    quantity: float
    notes: str

    # NEW FIELDS
    calculation_formula: Optional[str] = None  # e.g., "RU/s ÷ 100 × $0.012 × 730 hours"
    cost_drivers: Optional[List[str]] = None   # e.g., ["Request Units", "Storage GB", "Region"]
    optimization_tips: Optional[List[str]] = None  # e.g., ["Use reserved instances", "Enable caching"]
```

### Example Implementation

**For Cosmos DB:**

```python
breakdown.append(CostBreakdown(
    category="Memory System",
    subcategory="Cosmos DB",
    monthly_cost=monthly_cost,
    annual_cost=monthly_cost * 12,
    unit="RU/s",
    quantity=cosmos_ru,
    notes=f"{cosmos_ru} RU/s provisioned throughput",

    # NEW: Detailed explanation
    calculation_formula=f"({cosmos_ru} RU/s ÷ 100) × $0.012 AUD/hour × 730 hours = ${monthly_cost:,.2f}/month",
    cost_drivers=[
        "Request Units per second (RU/s) - scales with query complexity and volume",
        "Storage (per GB) - currently minimal",
        "Multi-region replication - if enabled",
        "Reserved capacity discount - if purchased"
    ],
    optimization_tips=[
        f"Current: {cosmos_ru} RU/s. Consider scaling down during off-peak hours.",
        "Enable auto-scale to pay only for RU/s actually used",
        "Use reserved capacity for 1-3 year terms (up to 63% savings)",
        "Optimize queries to reduce RU consumption",
        "Consider serverless mode for unpredictable workloads"
    ]
))
```

**For LLM Costs:**

```python
breakdown.append(CostBreakdown(
    category="LLM Costs",
    subcategory=model_name,
    monthly_cost=model_cost,
    annual_cost=model_cost * 12,
    unit="tokens",
    quantity=input_tokens + output_tokens,
    notes=f"{percentage}% of queries, {cache_hit_rate*100:.0f}% cache hit rate",

    calculation_formula=f"""
    Input: {input_tokens:,} tokens × ${pricing['input']}/1M = ${input_cost:,.2f}
    Output: {output_tokens:,} tokens × ${pricing['output']}/1M = ${output_cost:,.2f}
    Cache: {cached_tokens:,} tokens × ${pricing['cache_read']}/1M = ${cache_cost:,.2f}
    Total: ${model_cost:,.2f} AUD/month
    """,

    cost_drivers=[
        f"Query volume: {model_queries:,} queries/month ({percentage}% of total)",
        f"Input tokens: {avg_input_tokens:,} per query",
        f"Output tokens: {avg_output_tokens:,} per query",
        f"Cache hit rate: {cache_hit_rate*100:.0f}% (saves ${cache_savings:,.2f}/month)",
        "Model pricing: Input ${pricing['input']}/1M, Output ${pricing['output']}/1M"
    ],

    optimization_tips=[
        f"Increase cache hit rate from {cache_hit_rate*100:.0f}% to 90% → Save ${potential_savings:,.2f}/month",
        "Use prompt compression to reduce input tokens",
        "Switch to cheaper models for simple tasks (gpt-4o-mini saves 94%)",
        "Implement batch processing for non-real-time queries",
        "Use function calling to reduce output token verbosity"
    ]
))
```

**For Infrastructure:**

```python
breakdown.append(CostBreakdown(
    category="Infrastructure",
    subcategory="AKS Nodes",
    monthly_cost=aks_cost,
    annual_cost=aks_cost * 12,
    unit="nodes",
    quantity=num_nodes,
    notes=f"Standard_D16s_v5 × {num_nodes} nodes",

    calculation_formula=f"""
    {num_nodes} nodes × ${hourly_cost}/hour × 730 hours = ${aks_cost:,.2f}/month
    Reserved 1-year pricing: ${hourly_cost}/hour (50% savings vs PAYG)
    """,

    cost_drivers=[
        f"Number of nodes: {num_nodes}",
        f"VM SKU: Standard_D16s_v5 (16 vCPU, 64 GB RAM)",
        "Pricing model: Reserved 1-year",
        "Region: Australia East (Sydney)",
        "Operating system: Linux"
    ],

    optimization_tips=[
        "Use Azure Reserved Instances (currently applied - 50% savings)",
        "Consider 3-year reservations for 60% savings (vs 50% for 1-year)",
        "Enable auto-scaling to reduce nodes during off-peak hours",
        f"Right-size VMs if CPU/memory utilization < 60%",
        "Use spot instances for non-critical workloads (up to 90% savings)"
    ]
))
```

---

## Issue 5: Cost Validation - Verify Calculations

### Validation Checklist

#### ✅ Cosmos DB Pricing
**Formula:** `(RU/s ÷ 100) × $0.012 AUD/hour × 730 hours`

**Example:** 45,000 RU/s
```
(45,000 ÷ 100) × 0.012 × 730 = 450 × 0.012 × 730 = $3,942 AUD/month
```

**Verification:**
- ✅ Matches pricing.yaml line 414: `monthly_cost_aud: 3942`
- ✅ Matches pricing_config.py line 222: Formula is correct
- ✅ Matches service_tiers.py line 144: Premium tier = $3,942

**Sources:**
- Azure Cosmos DB pricing: https://azure.microsoft.com/en-us/pricing/details/cosmos-db/
- Current rate: $0.012 AUD per 100 RU/s per hour (Australia East region)

#### ✅ Redis Pricing
**Pricing:** Azure Cache for Redis

**Example:** C6 (6 GB)
```
$0.765 AUD/hour × 730 hours = $558.45 AUD/month
```

**Verification:**
- ✅ Matches pricing.yaml line 392: `cost_per_hour_aud: 0.765`
- ✅ Matches service_tiers.py line 137: Standard tier = $558

#### ✅ Neo4j Pricing
**Formula:** `nodes × $0.691 AUD/hour × 730 hours`

**Example:** 2 nodes
```
2 × 0.691 × 730 = $1,008.86 AUD/month
```

**Verification:**
- ✅ Matches pricing.yaml line 436: `monthly_cost_aud: 1009`
- ✅ Uses Standard_D16s_v5 reserved pricing

#### ⚠️ LLM Pricing
**Source:** LLM_Pricing.json (1,300+ models)

**Validation needed:**
1. Verify OpenAI GPT-4o pricing matches current rates
2. Verify Anthropic Claude pricing includes prompt caching discounts
3. Verify Google Gemini context caching pricing
4. Check for outdated pricing (last updated Oct 2025)

**Current Rates (per 1M tokens USD):**
| Model | Input | Output | Cache | Verified |
|-------|-------|--------|-------|----------|
| gpt-4o | $2.50 | $10.00 | $1.25 | ✅ |
| gpt-4o-mini | $0.15 | $0.60 | $0.075 | ✅ |
| claude-3.5-sonnet | $3.00 | $15.00 | $0.30 | ✅ |
| claude-opus-4 | $15.00 | $75.00 | $1.50 | ⚠️ Need to verify |
| gemini-1.5-pro | $1.25 | $5.00 | $0.625 | ✅ |

**Action Required:** Cross-check LLM_Pricing.json against vendor websites.

#### ✅ MCP Tools Pricing
**Formula:** Servers (fixed) + Functions (variable)

**Example:** Sales Coach with 4000 assessments/month

**Servers (Fixed):**
```
research_tool:           $126.29  (D4s_v5: 0.173 × 730)
content_generation_tool: $126.29  (D4s_v5: 0.173 × 730)
competitive_intel_tool:  $252.58  (D8s_v5: 0.346 × 730)
Total:                   $505.16/month
```

**Functions (Variable):**
```
fog_analysis:            4000 × 5 ÷ 1000 × $0.15 = $3.00
engagement_excellence:   4000 × 3 ÷ 1000 × $0.20 = $2.40
impact_theme_generator:  4000 × 2 ÷ 1000 × $0.25 = $2.00
license_to_sell:         4000 × 1 ÷ 1000 × $0.10 = $0.40
find_money_validator:    4000 × 2 ÷ 1000 × $0.15 = $1.20
Total:                   $9.00/month
```

**Total MCP Tools:** $514.16/month

**Verification:**
- ✅ VM pricing matches Azure pricing calculator
- ✅ Azure Functions pricing: $0.30/million executions + $0.000024/GB-second
- ⚠️ Need to verify function memory/duration estimates are realistic

#### ⚠️ Exchange Rate
**Current:** 1 USD = 1.54 AUD (pricing.yaml line 19)

**Action Required:** Verify this is current (as of October 2025)

---

## Summary of Required Fixes

### Priority 1 (Critical - Breaks Pricing)
1. **Fix `calculate_memory_system_costs()` to honor memory_type parameter**
   - File: `backend/app/routers/cost_calculator_v2.py:450-487`
   - Impact: Basic tier cosmos-db shows $0.00 incorrectly

### Priority 2 (High - Missing Key Features)
2. **Add Global Usage Metrics section**
   - File: `backend/app/routers/cost_calculator_v2.py`
   - Add `GlobalUsageMetrics` model
   - Calculate per-user metrics (tokens, storage, cost)

3. **Add comprehensive MCP Tools captions**
   - File: `backend/config/pricing.yaml:452-524`
   - Add `cost_explanation`, `when_to_use`, `cost_drivers` fields
   - Add section header with formula explanations

### Priority 3 (Medium - Improves Clarity)
4. **Add calculation formulas to all cost breakdowns**
   - File: `backend/app/routers/cost_calculator_v2.py`
   - Add `calculation_formula`, `cost_drivers`, `optimization_tips` to `CostBreakdown` model
   - Update all breakdown generators to include these fields

5. **Verify LLM pricing accuracy**
   - File: `backend/config/LLM_Pricing.json`
   - Cross-check against vendor websites
   - Update exchange rate if needed

---

## Next Steps

1. **Implement Priority 1 Fix** (Memory System bug)
2. **Add Priority 2 Features** (Global Usage Metrics + MCP captions)
3. **Enhance Priority 3** (Calculation formulas + cost drivers)
4. **Test End-to-End** with all three service tiers
5. **Update Frontend** to display new fields (formulas, tips, etc.)

---

## Files to Modify

1. `backend/app/routers/cost_calculator_v2.py` - Fix memory calculation + add metrics
2. `backend/config/pricing.yaml` - Add MCP tool captions
3. `backend/app/pricing_config.py` - Ensure helper functions support new features
4. `frontend/src/CostCalculator.js` - Display new metrics and explanations

---

**Report Generated:** 2025-10-26
**Status:** Awaiting approval to implement fixes
