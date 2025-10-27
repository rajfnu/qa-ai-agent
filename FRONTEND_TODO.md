# Frontend TODO - Display New Backend Features

**Status:** ❌ NOT IMPLEMENTED YET
**Impact:** Backend returns new data but frontend doesn't display it

---

## Current Situation

### ✅ Backend is Ready
The backend API now returns:
1. ✅ `global_usage_metrics` - 15 new per-user metrics
2. ✅ `calculation_formula` - Shows how each cost is calculated
3. ✅ `cost_drivers` - Lists what affects each cost
4. ✅ `optimization_tips` - Suggestions to save money

### ❌ Frontend is NOT Updated
The frontend (`CostCalculator.js`) currently:
- ❌ Does NOT display `global_usage_metrics`
- ❌ Does NOT display `calculation_formula`
- ❌ Does NOT display `cost_drivers`
- ❌ Does NOT display `optimization_tips`
- ✅ Only displays: subcategory, quantity, monthly_cost, annual_cost, notes

---

## What the Frontend Currently Shows

### Current Breakdown Display (lines 321-328):
```jsx
<tr key={idx}>
  <td>{item.subcategory}</td>              {/* ✅ Shows */}
  <td>{item.quantity} {item.unit}</td>     {/* ✅ Shows */}
  <td>{formatCurrency(item.monthly_cost)}</td>  {/* ✅ Shows */}
  <td>{formatCurrency(item.annual_cost)}</td>   {/* ✅ Shows */}
  <td>{item.notes}</td>                    {/* ✅ Shows */}

  {/* ❌ MISSING: item.calculation_formula */}
  {/* ❌ MISSING: item.cost_drivers */}
  {/* ❌ MISSING: item.optimization_tips */}
</tr>
```

### Current Overview Cards (lines 143-179):
```jsx
<div>Monthly Cost</div>          {/* ✅ Shows */}
<div>Per User/Month</div>        {/* ✅ Shows */}
<div>Per Query</div>             {/* ✅ Shows */}
<div>Annual Cost</div>           {/* ✅ Shows */}

{/* ❌ MISSING: Global Usage Metrics section */}
```

---

## TODO 1: Add Global Usage Metrics Section ❌

### What to Add
Create a new section in the Overview tab to display all per-user metrics.

### Location
Add after the Summary Cards (around line 179)

### Code to Add
```jsx
{/* Global Usage Parameters */}
{results && results.global_usage_metrics && (
  <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
    <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
      <Users className="w-6 h-6 mr-2 text-blue-600" />
      Global Usage Parameters
    </h3>
    <p className="text-sm text-gray-600 mb-4">
      {results.global_usage_metrics.description}
    </p>

    {/* Per-User Metrics */}
    <div className="mb-6">
      <h4 className="font-semibold text-gray-700 mb-3">Per-User Metrics</h4>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-sm text-blue-600 font-medium">Tokens/User/Month</div>
          <div className="text-2xl font-bold text-blue-900">
            {formatNumber(results.global_usage_metrics.tokens_per_user_per_month)}
          </div>
          <div className="text-xs text-blue-600 mt-1">
            Input: {formatNumber(results.global_usage_metrics.input_tokens_per_user_per_month)} |
            Output: {formatNumber(results.global_usage_metrics.output_tokens_per_user_per_month)}
          </div>
        </div>

        <div className="bg-green-50 rounded-lg p-4">
          <div className="text-sm text-green-600 font-medium">Storage/User</div>
          <div className="text-2xl font-bold text-green-900">
            {results.global_usage_metrics.storage_per_user_gb.toFixed(2)} GB
          </div>
          <div className="text-xs text-green-600 mt-1">
            Total: {results.global_usage_metrics.total_storage_gb} GB
          </div>
        </div>

        <div className="bg-purple-50 rounded-lg p-4">
          <div className="text-sm text-purple-600 font-medium">Cost/User/Month</div>
          <div className="text-2xl font-bold text-purple-900">
            {formatCurrency(results.global_usage_metrics.cost_per_user_per_month)}
          </div>
          <div className="text-xs text-purple-600 mt-1">
            {results.global_usage_metrics.queries_per_user_per_month} queries/user
          </div>
        </div>
      </div>
    </div>

    {/* Efficiency Metrics */}
    <div>
      <h4 className="font-semibold text-gray-700 mb-3">Efficiency Metrics</h4>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-orange-50 rounded-lg p-4">
          <div className="text-sm text-orange-600 font-medium">Cost/Query</div>
          <div className="text-xl font-bold text-orange-900">
            ${results.global_usage_metrics.cost_per_query.toFixed(4)}
          </div>
        </div>

        <div className="bg-pink-50 rounded-lg p-4">
          <div className="text-sm text-pink-600 font-medium">Cost/1K Tokens</div>
          <div className="text-xl font-bold text-pink-900">
            ${results.global_usage_metrics.cost_per_1k_tokens.toFixed(4)}
          </div>
        </div>

        <div className="bg-indigo-50 rounded-lg p-4">
          <div className="text-sm text-indigo-600 font-medium">Cache Hit Rate</div>
          <div className="text-xl font-bold text-indigo-900">
            {(results.global_usage_metrics.cache_hit_rate * 100).toFixed(1)}%
          </div>
        </div>

        <div className="bg-teal-50 rounded-lg p-4">
          <div className="text-sm text-teal-600 font-medium">Tokens/Query</div>
          <div className="text-xl font-bold text-teal-900">
            {formatNumber(results.global_usage_metrics.avg_tokens_per_query)}
          </div>
        </div>
      </div>
    </div>
  </div>
)}
```

### Expected Result
A new section showing:
- Per-user tokens, storage, cost
- Efficiency metrics like cost/query, cost/1k tokens
- Cache hit rate and tokens/query

---

## TODO 2: Display Calculation Formulas ❌

### What to Add
Show the calculation formula for each cost item (especially Memory System)

### Location
Update breakdown rendering (lines 321-328, 361-368, etc.)

### Code to Add
Add an expandable row or tooltip showing the formula:

```jsx
<tr key={idx}>
  <td colSpan="5" className="bg-gray-50 p-4">
    {item.calculation_formula && (
      <div className="text-sm">
        <span className="font-semibold text-gray-700">Formula: </span>
        <code className="bg-gray-100 px-2 py-1 rounded text-xs font-mono">
          {item.calculation_formula}
        </code>
      </div>
    )}
  </td>
</tr>
```

OR use a tooltip/popover on hover:

```jsx
<td className="py-3 px-4 font-medium text-gray-800 relative group">
  {item.subcategory}
  {item.calculation_formula && (
    <div className="absolute hidden group-hover:block bg-gray-900 text-white text-xs rounded p-2 -mt-2 ml-4 w-64 z-10">
      <div className="font-semibold mb-1">Calculation:</div>
      <code className="text-xs">{item.calculation_formula}</code>
    </div>
  )}
</td>
```

### Expected Result
Users can see HOW each cost was calculated by:
- Hovering over the cost item, OR
- Clicking to expand details

---

## TODO 3: Display Cost Drivers ❌

### What to Add
Show what factors affect each cost

### Code to Add
```jsx
{item.cost_drivers && item.cost_drivers.length > 0 && (
  <div className="mt-2 text-sm">
    <span className="font-semibold text-gray-700">Cost Drivers:</span>
    <ul className="list-disc list-inside ml-2 text-gray-600">
      {item.cost_drivers.map((driver, i) => (
        <li key={i}>{driver}</li>
      ))}
    </ul>
  </div>
)}
```

### Expected Result
Shows a bullet list of factors like:
- Request Units: 10,000 RU/s (primary driver)
- Storage: Minimal impact
- Multi-region replication: If enabled

---

## TODO 4: Display Optimization Tips ❌

### What to Add
Show suggestions to reduce costs

### Code to Add
```jsx
{item.optimization_tips && item.optimization_tips.length > 0 && (
  <div className="mt-2 bg-green-50 border border-green-200 rounded p-3">
    <div className="flex items-center mb-2">
      <span className="text-green-700 font-semibold text-sm">💡 Optimization Tips:</span>
    </div>
    <ul className="list-disc list-inside ml-2 text-sm text-green-700">
      {item.optimization_tips.map((tip, i) => (
        <li key={i}>{tip}</li>
      ))}
    </ul>
  </div>
)}
```

### Expected Result
Shows actionable tips like:
- Enable auto-scale to pay only for RU/s used
- Use reserved capacity for up to 63% savings
- Optimize queries to reduce RU consumption

---

## TODO 5: Add Expandable Details Row ❌

### What to Add
Make each cost breakdown row expandable to show formula + drivers + tips

### Code to Add
```jsx
const [expandedRow, setExpandedRow] = useState(null);

// In the table row:
<tr
  key={idx}
  onClick={() => setExpandedRow(expandedRow === idx ? null : idx)}
  className="cursor-pointer hover:bg-gray-50"
>
  <td>{item.subcategory}</td>
  <td>{item.quantity} {item.unit}</td>
  <td>{formatCurrency(item.monthly_cost)}</td>
  <td>{formatCurrency(item.annual_cost)}</td>
  <td>{item.notes}</td>
</tr>

{/* Expanded details */}
{expandedRow === idx && (item.calculation_formula || item.cost_drivers || item.optimization_tips) && (
  <tr>
    <td colSpan="5" className="bg-gray-50 p-4 border-t">
      {item.calculation_formula && (
        <div className="mb-3">
          <span className="font-semibold">Formula:</span>
          <code className="block bg-gray-100 p-2 rounded mt-1 text-sm">
            {item.calculation_formula}
          </code>
        </div>
      )}

      {item.cost_drivers && (
        <div className="mb-3">
          <span className="font-semibold">Cost Drivers:</span>
          <ul className="list-disc list-inside ml-2 mt-1 text-sm">
            {item.cost_drivers.map((d, i) => <li key={i}>{d}</li>)}
          </ul>
        </div>
      )}

      {item.optimization_tips && (
        <div>
          <span className="font-semibold text-green-700">Optimization Tips:</span>
          <ul className="list-disc list-inside ml-2 mt-1 text-sm text-green-700">
            {item.optimization_tips.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </div>
      )}
    </td>
  </tr>
)}
```

### Expected Result
Click a row → Expands to show formula, drivers, and tips

---

## Summary: What Needs to be Updated

### File: `frontend/src/CostCalculator.js`

**Add:**
1. ❌ Global Usage Metrics section (~50 lines)
2. ❌ Expandable row state management
3. ❌ Display calculation_formula in breakdown
4. ❌ Display cost_drivers in breakdown
5. ❌ Display optimization_tips in breakdown

**Estimated Effort:** 1-2 hours

**Priority:**
- HIGH: Global Usage Metrics (user specifically asked for this)
- MEDIUM: Calculation formulas (transparency)
- LOW: Cost drivers and optimization tips (nice to have)

---

## Quick Test After Implementation

1. Open `http://localhost:3000`
2. Navigate to Cost Calculator
3. Check Overview tab for "Global Usage Parameters" section
4. Click on a Memory System cost item
5. Verify expanded details show:
   - ✅ Formula
   - ✅ Cost drivers
   - ✅ Optimization tips

---

**Status:** NEEDS FRONTEND DEVELOPER
**Backend Status:** ✅ COMPLETE
**Frontend Status:** ❌ NOT STARTED
