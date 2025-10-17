import React, { useState, useEffect } from 'react';
import { DollarSign, Users, Cpu, Database, Network, Brain, TrendingUp, Save, Download } from 'lucide-react';
import axios from 'axios';

const CostCalculator = () => {
  const [params, setParams] = useState({
    num_users: 100,
    queries_per_user_per_month: 1000,
    avg_input_tokens: 10000,
    avg_output_tokens: 1000,
    aks_agent_nodes_baseline: 10,
    aks_gpu_nodes_baseline: 3,
    azure_sql_vcores: 16,
    cosmosdb_ru_baseline: 50000,
    neo4j_cluster_size: 3,
    adls_hot_tier_tb: 20,
    adls_cool_tier_tb: 150,
    llm_mix: {
      "gpt-4o": 60.0,
      "claude-3.5-sonnet": 30.0,
      "llama-3.1-70b": 10.0
    },
    cache_hit_rate: 0.70,
    use_prompt_caching: true,
    use_reserved_instances: true,
    use_zoominfo: true,
    use_linkedin_sales_nav: true,
    use_clearbit: true
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  const calculateCosts = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/cost/calculate', params);
      setResults(response.data);
    } catch (error) {
      console.error('Error calculating costs:', error);
      alert('Failed to calculate costs. Please check console.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Calculate on initial load
    calculateCosts();
  }, []);

  const handleParamChange = (key, value) => {
    setParams(prev => ({ ...prev, [key]: value }));
  };

  const handleLLMMixChange = (model, value) => {
    setParams(prev => ({
      ...prev,
      llm_mix: { ...prev.llm_mix, [model]: parseFloat(value) }
    }));
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 flex items-center">
                <DollarSign className="mr-3 text-green-600" size={40} />
                Sales Coach AI - Cost Calculator
              </h1>
              <p className="text-gray-600 mt-2">Configure your deployment and see real-time cost estimates</p>
            </div>
            <button
              onClick={calculateCosts}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold shadow-lg transition-all flex items-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Calculating...
                </>
              ) : (
                <>
                  <TrendingUp className="mr-2" size={20} />
                  Recalculate
                </>
              )}
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-lg mb-6 p-2 flex space-x-2">
          {['overview', 'infrastructure', 'llm', 'data', 'breakdown'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${
                activeTab === tab
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Configuration */}
          <div className="lg:col-span-1 space-y-6">

            {/* Users & Usage */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <Users className="mr-2 text-blue-600" />
                Users & Usage
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Number of Users: {params.num_users}
                  </label>
                  <input
                    type="range"
                    min="10"
                    max="1000"
                    step="10"
                    value={params.num_users}
                    onChange={(e) => handleParamChange('num_users', parseInt(e.target.value))}
                    className="w-full h-2 bg-blue-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>10</span>
                    <span>1000</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Queries/User/Month: {params.queries_per_user_per_month}
                  </label>
                  <input
                    type="range"
                    min="100"
                    max="5000"
                    step="100"
                    value={params.queries_per_user_per_month}
                    onChange={(e) => handleParamChange('queries_per_user_per_month', parseInt(e.target.value))}
                    className="w-full h-2 bg-blue-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Avg Input Tokens: {params.avg_input_tokens}
                  </label>
                  <input
                    type="range"
                    min="1000"
                    max="50000"
                    step="1000"
                    value={params.avg_input_tokens}
                    onChange={(e) => handleParamChange('avg_input_tokens', parseInt(e.target.value))}
                    className="w-full h-2 bg-blue-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Cache Hit Rate: {(params.cache_hit_rate * 100).toFixed(0)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="95"
                    step="5"
                    value={params.cache_hit_rate * 100}
                    onChange={(e) => handleParamChange('cache_hit_rate', parseInt(e.target.value) / 100)}
                    className="w-full h-2 bg-green-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>
              </div>
            </div>

            {/* Infrastructure */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <Cpu className="mr-2 text-purple-600" />
                Compute
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    AKS Agent Nodes: {params.aks_agent_nodes_baseline}
                  </label>
                  <input
                    type="range"
                    min="3"
                    max="50"
                    value={params.aks_agent_nodes_baseline}
                    onChange={(e) => handleParamChange('aks_agent_nodes_baseline', parseInt(e.target.value))}
                    className="w-full h-2 bg-purple-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    GPU Nodes (Llama): {params.aks_gpu_nodes_baseline}
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    value={params.aks_gpu_nodes_baseline}
                    onChange={(e) => handleParamChange('aks_gpu_nodes_baseline', parseInt(e.target.value))}
                    className="w-full h-2 bg-purple-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>
              </div>
            </div>

            {/* LLM Mix */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <Brain className="mr-2 text-pink-600" />
                LLM Mix
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    GPT-4o: {params.llm_mix['gpt-4o']}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={params.llm_mix['gpt-4o']}
                    onChange={(e) => handleLLMMixChange('gpt-4o', e.target.value)}
                    className="w-full h-2 bg-pink-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Claude 3.5 Sonnet: {params.llm_mix['claude-3.5-sonnet']}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={params.llm_mix['claude-3.5-sonnet']}
                    onChange={(e) => handleLLMMixChange('claude-3.5-sonnet', e.target.value)}
                    className="w-full h-2 bg-pink-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Llama 3.1 70B (Local): {params.llm_mix['llama-3.1-70b']}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={params.llm_mix['llama-3.1-70b']}
                    onChange={(e) => handleLLMMixChange('llama-3.1-70b', e.target.value)}
                    className="w-full h-2 bg-pink-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <div className="text-xs text-gray-500">
                  Total: {Object.values(params.llm_mix).reduce((a, b) => a + b, 0).toFixed(0)}%
                </div>
              </div>
            </div>

            {/* Toggles */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Options</h3>

              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={params.use_prompt_caching}
                    onChange={(e) => handleParamChange('use_prompt_caching', e.target.checked)}
                    className="mr-3 w-5 h-5"
                  />
                  <span className="text-sm">Enable Prompt Caching (Claude)</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={params.use_reserved_instances}
                    onChange={(e) => handleParamChange('use_reserved_instances', e.target.checked)}
                    className="mr-3 w-5 h-5"
                  />
                  <span className="text-sm">Use Reserved Instances (40% off)</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={params.use_zoominfo}
                    onChange={(e) => handleParamChange('use_zoominfo', e.target.checked)}
                    className="mr-3 w-5 h-5"
                  />
                  <span className="text-sm">ZoomInfo ($15K/year)</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={params.use_linkedin_sales_nav}
                    onChange={(e) => handleParamChange('use_linkedin_sales_nav', e.target.checked)}
                    className="mr-3 w-5 h-5"
                  />
                  <span className="text-sm">LinkedIn Sales Navigator</span>
                </label>
              </div>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2 space-y-6">

            {results && (
              <>
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl shadow-xl p-6 text-white">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-blue-100 text-sm font-medium">Monthly Cost</p>
                        <p className="text-4xl font-bold mt-2">{formatCurrency(results.total_monthly_cost)}</p>
                        <p className="text-blue-100 text-sm mt-2">
                          {formatCurrency(results.cost_per_user_monthly)}/user
                        </p>
                      </div>
                      <DollarSign size={64} className="opacity-20" />
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl shadow-xl p-6 text-white">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-green-100 text-sm font-medium">Annual Cost</p>
                        <p className="text-4xl font-bold mt-2">{formatCurrency(results.total_annual_cost)}</p>
                        <p className="text-green-100 text-sm mt-2">
                          {formatCurrency(results.cost_per_user_annual)}/user/year
                        </p>
                      </div>
                      <TrendingUp size={64} className="opacity-20" />
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl shadow-xl p-6 text-white">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-purple-100 text-sm font-medium">Fixed Infrastructure</p>
                        <p className="text-4xl font-bold mt-2">{formatCurrency(results.fixed_monthly_cost)}</p>
                        <p className="text-purple-100 text-sm mt-2">
                          {((results.fixed_monthly_cost / results.total_monthly_cost) * 100).toFixed(0)}% of total
                        </p>
                      </div>
                      <Database size={64} className="opacity-20" />
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-orange-600 to-orange-700 rounded-xl shadow-xl p-6 text-white">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-orange-100 text-sm font-medium">Variable Usage</p>
                        <p className="text-4xl font-bold mt-2">{formatCurrency(results.variable_monthly_cost)}</p>
                        <p className="text-orange-100 text-sm mt-2">
                          {((results.variable_monthly_cost / results.total_monthly_cost) * 100).toFixed(0)}% of total
                        </p>
                      </div>
                      <Network size={64} className="opacity-20" />
                    </div>
                  </div>
                </div>

                {/* ROI Card */}
                {results.roi_analysis && (
                  <div className="bg-gradient-to-br from-emerald-600 to-teal-700 rounded-xl shadow-xl p-8 text-white">
                    <h3 className="text-2xl font-bold mb-6">Return on Investment (ROI)</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                      <div>
                        <p className="text-emerald-100 text-sm">ROI Ratio</p>
                        <p className="text-3xl font-bold mt-2">{results.roi_analysis.roi_ratio}</p>
                      </div>
                      <div>
                        <p className="text-emerald-100 text-sm">ROI Percentage</p>
                        <p className="text-3xl font-bold mt-2">{results.roi_analysis.roi_percentage}%</p>
                      </div>
                      <div>
                        <p className="text-emerald-100 text-sm">Payback Period</p>
                        <p className="text-3xl font-bold mt-2">{results.roi_analysis.payback_months} mo</p>
                      </div>
                      <div>
                        <p className="text-emerald-100 text-sm">Additional Revenue</p>
                        <p className="text-3xl font-bold mt-2">{formatCurrency(results.roi_analysis.total_additional_revenue / 1000000)}M</p>
                      </div>
                    </div>
                    <div className="mt-6 pt-6 border-t border-emerald-400">
                      <p className="text-sm text-emerald-100">
                        Based on {params.num_users} users generating {formatCurrency(results.roi_analysis.additional_revenue_per_rep)}
                        additional revenue per rep annually
                      </p>
                    </div>
                  </div>
                )}

                {/* Cost Breakdown Chart */}
                <div className="bg-white rounded-xl shadow-xl p-6">
                  <h3 className="text-2xl font-bold text-gray-800 mb-6">Cost Breakdown by Category</h3>

                  <div className="space-y-4">
                    {[
                      { name: 'Compute', value: results.compute_costs, color: 'bg-blue-500' },
                      { name: 'Databases', value: results.database_costs, color: 'bg-purple-500' },
                      { name: 'LLM/AI', value: results.llm_costs, color: 'bg-pink-500' },
                      { name: 'Storage', value: results.storage_costs, color: 'bg-green-500' },
                      { name: 'Networking', value: results.networking_costs, color: 'bg-indigo-500' },
                      { name: 'Data Sources', value: results.data_source_costs, color: 'bg-yellow-500' },
                      { name: 'Monitoring', value: results.monitoring_costs, color: 'bg-red-500' },
                    ].map(category => (
                      <div key={category.name} className="flex items-center">
                        <div className="w-32 text-sm font-medium text-gray-700">{category.name}</div>
                        <div className="flex-1 mx-4">
                          <div className="bg-gray-200 rounded-full h-8 relative overflow-hidden">
                            <div
                              className={`${category.color} h-full rounded-full flex items-center justify-end pr-3 text-white text-sm font-bold transition-all duration-500`}
                              style={{ width: `${(category.value / results.total_monthly_cost) * 100}%` }}
                            >
                              {((category.value / results.total_monthly_cost) * 100).toFixed(1)}%
                            </div>
                          </div>
                        </div>
                        <div className="w-32 text-right text-sm font-bold text-gray-800">
                          {formatCurrency(category.value)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Detailed Breakdown Table */}
                <div className="bg-white rounded-xl shadow-xl p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-2xl font-bold text-gray-800">Detailed Line Items</h3>
                    <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-semibold flex items-center">
                      <Download size={18} className="mr-2" />
                      Export
                    </button>
                  </div>

                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b-2 border-gray-200">
                          <th className="text-left py-3 px-4 text-sm font-bold text-gray-700">Category</th>
                          <th className="text-left py-3 px-4 text-sm font-bold text-gray-700">Subcategory</th>
                          <th className="text-right py-3 px-4 text-sm font-bold text-gray-700">Quantity</th>
                          <th className="text-right py-3 px-4 text-sm font-bold text-gray-700">Monthly</th>
                          <th className="text-right py-3 px-4 text-sm font-bold text-gray-700">Annual</th>
                        </tr>
                      </thead>
                      <tbody>
                        {results.breakdown.map((item, idx) => (
                          <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                            <td className="py-3 px-4 text-sm text-gray-700">{item.category}</td>
                            <td className="py-3 px-4 text-sm text-gray-600">{item.subcategory}</td>
                            <td className="py-3 px-4 text-sm text-gray-600 text-right">
                              {formatNumber(item.quantity)} {item.unit}
                            </td>
                            <td className="py-3 px-4 text-sm font-semibold text-gray-800 text-right">
                              {formatCurrency(item.monthly_cost)}
                            </td>
                            <td className="py-3 px-4 text-sm font-semibold text-gray-800 text-right">
                              {formatCurrency(item.annual_cost)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                      <tfoot>
                        <tr className="border-t-2 border-gray-300 font-bold">
                          <td colSpan="3" className="py-4 px-4 text-gray-900">TOTAL</td>
                          <td className="py-4 px-4 text-right text-gray-900">
                            {formatCurrency(results.total_monthly_cost)}
                          </td>
                          <td className="py-4 px-4 text-right text-gray-900">
                            {formatCurrency(results.total_annual_cost)}
                          </td>
                        </tr>
                      </tfoot>
                    </table>
                  </div>
                </div>

                {/* Usage Metrics */}
                <div className="bg-white rounded-xl shadow-xl p-6">
                  <h3 className="text-2xl font-bold text-gray-800 mb-6">Usage Metrics</h3>

                  <div className="grid grid-cols-3 gap-6">
                    <div className="text-center">
                      <p className="text-gray-600 text-sm">Total Queries/Month</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">
                        {formatNumber(results.queries_per_month)}
                      </p>
                    </div>
                    <div className="text-center">
                      <p className="text-gray-600 text-sm">Total Tokens/Month</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">
                        {formatNumber(Math.round(results.tokens_per_month / 1000000))}M
                      </p>
                    </div>
                    <div className="text-center">
                      <p className="text-gray-600 text-sm">Data Size</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">
                        {formatNumber(Math.round(results.estimated_data_size_gb / 1000))} TB
                      </p>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CostCalculator;
