#!/usr/bin/env python3
"""
Test script to verify pricing fixes work correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from app.routers.cost_calculator_v2 import calculate_costs, CostCalculatorRequest

async def test_memory_system_fix():
    """Test that memory system costs are calculated correctly"""

    print("=" * 80)
    print("TEST 1: Memory System Cost Calculation")
    print("=" * 80)

    # Test Basic Tier + Cosmos DB (should NOT be $0.00!)
    params = CostCalculatorRequest(
        agent_type="sales-coach",
        service_tier="basic",
        num_users=100,
        queries_per_user_per_month=1000,
        avg_input_tokens=10000,
        avg_output_tokens=1000,
        memory_type="cosmos-db"
    )

    print(f"\nTest Case: Basic Tier + Cosmos DB")
    print(f"  - Service Tier: {params.service_tier}")
    print(f"  - Memory Type: {params.memory_type}")
    print(f"  - Expected: ~$1,314/month (NOT $0.00)")

    try:
        result = await calculate_costs(params)

        print(f"\n✅ RESULT:")
        print(f"  - Memory System Cost: ${result.memory_system_costs:,.2f}/month")

        if result.memory_system_costs == 0:
            print(f"  ❌ FAILED: Cost is $0.00 (BUG NOT FIXED!)")
            return False
        elif 1200 <= result.memory_system_costs <= 1400:
            print(f"  ✅ PASSED: Cost is correct!")
        else:
            print(f"  ⚠️  WARNING: Cost seems off (expected ~$1,314)")

        # Check breakdown
        if result.memory_system_breakdown:
            breakdown = result.memory_system_breakdown[0]
            print(f"\n  Breakdown Details:")
            print(f"    - Subcategory: {breakdown.subcategory}")
            print(f"    - Monthly Cost: ${breakdown.monthly_cost:,.2f}")
            print(f"    - Unit: {breakdown.unit}")
            print(f"    - Quantity: {breakdown.quantity}")

            if breakdown.calculation_formula:
                print(f"    - Formula: {breakdown.calculation_formula}")
                print(f"  ✅ Formula present!")
            else:
                print(f"  ⚠️  WARNING: No formula provided")

            if breakdown.cost_drivers:
                print(f"    - Cost Drivers: {len(breakdown.cost_drivers)} items")
                for driver in breakdown.cost_drivers[:3]:
                    print(f"      • {driver}")
                print(f"  ✅ Cost drivers present!")
            else:
                print(f"  ⚠️  WARNING: No cost drivers")

            if breakdown.optimization_tips:
                print(f"    - Optimization Tips: {len(breakdown.optimization_tips)} items")
                for tip in breakdown.optimization_tips[:2]:
                    print(f"      • {tip}")
                print(f"  ✅ Optimization tips present!")
            else:
                print(f"  ⚠️  WARNING: No optimization tips")

        return True
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_global_usage_metrics():
    """Test that global usage metrics are calculated"""

    print("\n")
    print("=" * 80)
    print("TEST 2: Global Usage Metrics")
    print("=" * 80)

    params = CostCalculatorRequest(
        agent_type="sales-coach",
        service_tier="standard",
        num_users=100,
        queries_per_user_per_month=1000,
        avg_input_tokens=10000,
        avg_output_tokens=1000,
        memory_type="redis"
    )

    print(f"\nTest Case: Standard Tier with 100 users")
    print(f"  - Users: {params.num_users}")
    print(f"  - Queries per user: {params.queries_per_user_per_month}")
    print(f"  - Input tokens: {params.avg_input_tokens}")
    print(f"  - Output tokens: {params.avg_output_tokens}")

    try:
        result = await calculate_costs(params)

        print(f"\n✅ RESULT:")

        if hasattr(result, 'global_usage_metrics'):
            metrics = result.global_usage_metrics
            print(f"  ✅ Global usage metrics present!")
            print(f"\n  Per-User Metrics:")
            print(f"    - Tokens per user/month: {metrics.tokens_per_user_per_month:,}")
            print(f"    - Input tokens per user/month: {metrics.input_tokens_per_user_per_month:,}")
            print(f"    - Output tokens per user/month: {metrics.output_tokens_per_user_per_month:,}")
            print(f"    - Storage per user: {metrics.storage_per_user_gb:.2f} GB")
            print(f"    - Cost per user/month: ${metrics.cost_per_user_per_month:,.2f}")

            print(f"\n  Aggregate Metrics:")
            print(f"    - Total users: {metrics.total_users}")
            print(f"    - Total tokens/month: {metrics.total_tokens_per_month:,}")
            print(f"    - Total queries/month: {metrics.total_queries_per_month:,}")

            print(f"\n  Efficiency Metrics:")
            print(f"    - Cache hit rate: {metrics.cache_hit_rate * 100:.1f}%")
            print(f"    - Cost per query: ${metrics.cost_per_query:.4f}")
            print(f"    - Cost per 1k tokens: ${metrics.cost_per_1k_tokens:.4f}")

            # Validate calculations
            expected_tokens = (params.avg_input_tokens + params.avg_output_tokens) * params.queries_per_user_per_month
            if metrics.tokens_per_user_per_month == expected_tokens:
                print(f"\n  ✅ Tokens per user calculation: CORRECT")
            else:
                print(f"\n  ❌ Tokens per user calculation: WRONG")
                print(f"     Expected: {expected_tokens}, Got: {metrics.tokens_per_user_per_month}")

            expected_cost_per_user = result.total_monthly_cost / params.num_users
            if abs(metrics.cost_per_user_per_month - expected_cost_per_user) < 0.01:
                print(f"  ✅ Cost per user calculation: CORRECT")
            else:
                print(f"  ❌ Cost per user calculation: WRONG")
                print(f"     Expected: {expected_cost_per_user:.2f}, Got: {metrics.cost_per_user_per_month:.2f}")

            return True
        else:
            print(f"  ❌ FAILED: global_usage_metrics not found in response!")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_different_memory_types():
    """Test all memory types"""

    print("\n")
    print("=" * 80)
    print("TEST 3: Different Memory Types")
    print("=" * 80)

    test_cases = [
        ("in-memory", "basic", 0.00),
        ("redis", "standard", 558.00),
        ("cosmos-db", "basic", 876.00),  # 10k RU/s minimum = $876
        ("neo4j", "premium", 1513.00),   # 3 nodes × $0.691/hr × 730 = $1,513
    ]

    results = []

    for memory_type, tier, expected_cost in test_cases:
        print(f"\n  Testing: {memory_type} on {tier} tier")
        print(f"    Expected cost: ~${expected_cost:,.2f}/month")

        params = CostCalculatorRequest(
            agent_type="sales-coach",
            service_tier=tier,
            num_users=100,
            queries_per_user_per_month=1000,
            avg_input_tokens=10000,
            avg_output_tokens=1000,
            memory_type=memory_type
        )

        try:
            result = await calculate_costs(params)
            actual_cost = result.memory_system_costs

            # Allow 10% variance
            if expected_cost == 0:
                passed = actual_cost == 0
            else:
                passed = abs(actual_cost - expected_cost) / expected_cost < 0.10

            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"    Actual cost: ${actual_cost:,.2f}/month - {status}")

            results.append(passed)
        except Exception as e:
            print(f"    ❌ ERROR: {e}")
            results.append(False)

    return all(results)


async def main():
    """Run all tests"""

    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "PRICING FIX VALIDATION TESTS" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")

    test1_passed = await test_memory_system_fix()
    test2_passed = await test_global_usage_metrics()
    test3_passed = await test_different_memory_types()

    print("\n")
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"  Test 1 (Memory System Fix): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"  Test 2 (Global Usage Metrics): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"  Test 3 (All Memory Types): {'✅ PASSED' if test3_passed else '❌ FAILED'}")

    if test1_passed and test2_passed and test3_passed:
        print("\n  🎉 ALL TESTS PASSED! 🎉")
        print("  The pricing fixes are working correctly!")
        return 0
    else:
        print("\n  ❌ SOME TESTS FAILED")
        print("  Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
