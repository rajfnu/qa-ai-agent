import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, Server, Database, Cloud, BarChart3, Users, Zap, Settings } from 'lucide-react';
import axios from 'axios';

const CostCalculator = () => {
  // Available AI Agents
  const [availableAgents, setAvailableAgents] = useState([]);
  
  // Current selection and parameters
  const [selectedAgent, setSelectedAgent] = useState('sales-coach');
  const [agentDetails, setAgentDetails] = useState(null);
  
  // Active tab
  const [activeTab, setActiveTab] = useState('overview');
  
  // Cost calculation results
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  // Parameters
  const [params, setParams] = useState({
    agent_type: 'sales-coach',
    num_users: 100,
    queries_per_user_per_month: 1000,
    avg_input_tokens: 10000,
    avg_output_tokens: 1000,
    infrastructure_scale: 1.0,
    llm_mix: {
      'gpt-4o': 60.0,
      'claude-3.5-sonnet': 30.0,
      'llama-3.1-70b': 10.0
    },
    cache_hit_rate: 0.70,
    use_prompt_caching: true,
    use_reserved_instances: true
  });

  // Fetch available agents on mount
  useEffect(() => {
    fetchAgents();
  }, []);

  // Fetch agent list
  const fetchAgents = async () => {
    try {
      const response = await axios.get('/api/cost/agents');
      setAvailableAgents(response.data.agents);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  // Fetch agent details when selection changes
  useEffect(() => {
    if (selectedAgent) {
      fetchAgentDetails(selectedAgent);
    }
  }, [selectedAgent]);

  const fetchAgentDetails = async (agentId) => {
    try {
      const response = await axios.get(`/api/cost/agents/${agentId}`);
      setAgentDetails(response.data);
    } catch (error) {
      console.error('Error fetching agent details:', error);
    }
  };

  // Calculate costs on param changes
  useEffect(() => {
    const timer = setTimeout(() => {
      calculateCosts();
    }, 500); // Debounce
    return () => clearTimeout(timer);
  }, [params]);

  const calculateCosts = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/cost/calculate', params);
      setResults(response.data);
    } catch (error) {
      console.error('Error calculating costs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleParamChange = (key, value) => {
    setParams(prev => ({ ...prev, [key]: value }));
  };

  const handleLLMMixChange = (model, value) => {
    setParams(prev => ({
      ...prev,
      llm_mix: { ...prev.llm_mix, [model]: parseFloat(value) }
    }));
  };

  const handleAgentChange = (agentId) => {
    setSelectedAgent(agentId);
    setParams(prev => ({ ...prev, agent_type: agentId }));
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  // Tab content components
  const OverviewTab = () => (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium opacity-90">Monthly Cost</h3>
            <DollarSign className="w-5 h-5 opacity-75" />
          </div>
          <p className="text-3xl font-bold">{results ? formatCurrency(results.total_monthly_cost) : '-'}</p>
          <p className="text-xs opacity-75 mt-1">Total infrastructure + LLM</p>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium opacity-90">Per User/Month</h3>
            <Users className="w-5 h-5 opacity-75" />
          </div>
          <p className="text-3xl font-bold">{results ? formatCurrency(results.cost_per_user_monthly) : '-'}</p>
          <p className="text-xs opacity-75 mt-1">{params.num_users} users</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium opacity-90">Per Query</h3>
            <Zap className="w-5 h-5 opacity-75" />
          </div>
          <p className="text-3xl font-bold">{results ? formatCurrency(results.cost_per_query) : '-'}</p>
          <p className="text-xs opacity-75 mt-1">{results ? formatNumber(results.queries_per_month) : 0} queries/mo</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium opacity-90">Annual Cost</h3>
            <TrendingUp className="w-5 h-5 opacity-75" />
          </div>
          <p className="text-3xl font-bold">{results ? formatCurrency(results.total_annual_cost) : '-'}</p>
          <p className="text-xs opacity-75 mt-1">12-month projection</p>
        </div>
      </div>

      {/* Agent Architecture */}
      {results && results.agent_architecture && (
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <Settings className="w-6 h-6 mr-2 text-blue-600" />
            {results.agent_architecture.agent_name}
          </h3>
          <p className="text-gray-600 mb-4">{results.agent_architecture.description}</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-sm font-medium text-blue-600 mb-1">Sub-Agents</div>
              <div className="text-2xl font-bold text-blue-900">{results.agent_architecture.agents_count}</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-sm font-medium text-green-600 mb-1">Data Buckets</div>
              <div className="text-2xl font-bold text-green-900">{results.agent_architecture.data_buckets}</div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <div className="text-sm font-medium text-purple-600 mb-1">Complexity</div>
              <div className="text-2xl font-bold text-purple-900 capitalize">{results.agent_architecture.complexity}</div>
            </div>
          </div>

          <div className="mb-4">
            <h4 className="font-semibold text-gray-700 mb-2">Sub-Agents:</h4>
            <div className="flex flex-wrap gap-2">
              {results.agent_architecture.agents_list.map((agent, idx) => (
                <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                  {agent}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-700 mb-2">Data Sources:</h4>
            <div className="flex flex-wrap gap-2">
              {results.agent_architecture.data_sources.map((source, idx) => (
                <span key={idx} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                  {source}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Cost Breakdown */}
      {results && (
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Cost Breakdown</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center">
                <Server className="w-5 h-5 mr-3 text-blue-600" />
                <span className="font-medium text-gray-700">Infrastructure</span>
              </div>
              <span className="text-lg font-bold text-blue-900">{formatCurrency(results.infrastructure_costs)}</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center">
                <Zap className="w-5 h-5 mr-3 text-purple-600" />
                <span className="font-medium text-gray-700">LLM API Costs</span>
              </div>
              <span className="text-lg font-bold text-purple-900">{formatCurrency(results.llm_costs)}</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center">
                <Database className="w-5 h-5 mr-3 text-green-600" />
                <span className="font-medium text-gray-700">Data Sources</span>
              </div>
              <span className="text-lg font-bold text-green-900">{formatCurrency(results.data_source_costs)}</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
              <div className="flex items-center">
                <BarChart3 className="w-5 h-5 mr-3 text-orange-600" />
                <span className="font-medium text-gray-700">Monitoring</span>
              </div>
              <span className="text-lg font-bold text-orange-900">{formatCurrency(results.monitoring_costs)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Savings */}
      {results && (results.savings_from_caching > 0 || results.savings_from_reserved_instances > 0) && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
          <h3 className="text-lg font-bold text-green-800 mb-4">💰 Cost Savings</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.savings_from_caching > 0 && (
              <div>
                <div className="text-sm text-green-600 font-medium">Prompt Caching</div>
                <div className="text-2xl font-bold text-green-900">{formatCurrency(results.savings_from_caching)}/mo</div>
              </div>
            )}
            {results.savings_from_reserved_instances > 0 && (
              <div>
                <div className="text-sm text-green-600 font-medium">Reserved Instances</div>
                <div className="text-2xl font-bold text-green-900">{formatCurrency(results.savings_from_reserved_instances)}/mo</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );

  const InfrastructureTab = () => (
    <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Infrastructure Costs (Azure Australia East)</h3>
      {results && results.infrastructure_breakdown && results.infrastructure_breakdown.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Resource</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Quantity</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Monthly</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Annual</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Notes</th>
              </tr>
            </thead>
            <tbody>
              {results.infrastructure_breakdown.map((item, idx) => (
                <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium text-gray-800">{item.subcategory}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{item.quantity.toFixed(0)} {item.unit}</td>
                  <td className="py-3 px-4 text-right font-semibold text-gray-900">{formatCurrency(item.monthly_cost)}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{formatCurrency(item.annual_cost)}</td>
                  <td className="py-3 px-4 text-sm text-gray-500">{item.notes}</td>
                </tr>
              ))}
              <tr className="bg-blue-50 font-bold">
                <td className="py-3 px-4 text-gray-900" colSpan="2">Total Infrastructure</td>
                <td className="py-3 px-4 text-right text-blue-900">{formatCurrency(results.infrastructure_costs)}</td>
                <td className="py-3 px-4 text-right text-blue-900">{formatCurrency(results.infrastructure_costs * 12)}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500">No infrastructure data available</p>
      )}
    </div>
  );

  const LLMTab = () => (
    <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
      <h3 className="text-xl font-bold text-gray-800 mb-4">LLM API Costs</h3>
      {results && results.llm_breakdown && results.llm_breakdown.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Model</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Tokens</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Monthly</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Annual</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Details</th>
              </tr>
            </thead>
            <tbody>
              {results.llm_breakdown.map((item, idx) => (
                <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium text-gray-800">{item.subcategory}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{formatNumber(item.quantity)}</td>
                  <td className="py-3 px-4 text-right font-semibold text-gray-900">{formatCurrency(item.monthly_cost)}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{formatCurrency(item.annual_cost)}</td>
                  <td className="py-3 px-4 text-sm text-gray-500">{item.notes}</td>
                </tr>
              ))}
              <tr className="bg-purple-50 font-bold">
                <td className="py-3 px-4 text-gray-900" colSpan="2">Total LLM Costs</td>
                <td className="py-3 px-4 text-right text-purple-900">{formatCurrency(results.llm_costs)}</td>
                <td className="py-3 px-4 text-right text-purple-900">{formatCurrency(results.llm_costs * 12)}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500">No LLM data available</p>
      )}
    </div>
  );

  const DataSourcesTab = () => (
    <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Premium Data Sources</h3>
      {results && results.data_source_breakdown && results.data_source_breakdown.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Data Source</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Monthly</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Annual</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Plan</th>
              </tr>
            </thead>
            <tbody>
              {results.data_source_breakdown.map((item, idx) => (
                <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium text-gray-800">{item.subcategory}</td>
                  <td className="py-3 px-4 text-right font-semibold text-gray-900">{formatCurrency(item.monthly_cost)}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{formatCurrency(item.annual_cost)}</td>
                  <td className="py-3 px-4 text-sm text-gray-500">{item.notes}</td>
                </tr>
              ))}
              <tr className="bg-green-50 font-bold">
                <td className="py-3 px-4 text-gray-900">Total Data Sources</td>
                <td className="py-3 px-4 text-right text-green-900">{formatCurrency(results.data_source_costs)}</td>
                <td className="py-3 px-4 text-right text-green-900">{formatCurrency(results.data_source_costs * 12)}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500">No premium data sources for this agent</p>
      )}
    </div>
  );

  const MonitoringTab = () => (
    <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Monitoring & Observability</h3>
      {results && results.monitoring_breakdown && results.monitoring_breakdown.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Service</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Quantity</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Monthly</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Annual</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Description</th>
              </tr>
            </thead>
            <tbody>
              {results.monitoring_breakdown.map((item, idx) => (
                <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium text-gray-800">{item.subcategory}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{item.quantity.toFixed(0)} {item.unit}</td>
                  <td className="py-3 px-4 text-right font-semibold text-gray-900">{formatCurrency(item.monthly_cost)}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{formatCurrency(item.annual_cost)}</td>
                  <td className="py-3 px-4 text-sm text-gray-500">{item.notes}</td>
                </tr>
              ))}
              <tr className="bg-orange-50 font-bold">
                <td className="py-3 px-4 text-gray-900" colSpan="2">Total Monitoring</td>
                <td className="py-3 px-4 text-right text-orange-900">{formatCurrency(results.monitoring_costs)}</td>
                <td className="py-3 px-4 text-right text-orange-900">{formatCurrency(results.monitoring_costs * 12)}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500">No monitoring data available</p>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">AI Agent Cost Calculator</h1>
          <p className="text-gray-600">Production-ready cost estimation for Azure Australia East (Sydney) deployment</p>
        </div>

        {/* Agent Selector */}
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Select AI Agent</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {availableAgents.map((agent) => (
              <button
                key={agent.id}
                onClick={() => handleAgentChange(agent.id)}
                className={`p-4 rounded-lg border-2 text-left transition-all ${
                  selectedAgent === agent.id
                    ? 'border-blue-500 bg-blue-50 shadow-md'
                    : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                }`}
              >
                <h3 className="font-bold text-gray-900 mb-1">{agent.name}</h3>
                <p className="text-sm text-gray-600 mb-2">{agent.description}</p>
                <div className="flex gap-2 text-xs">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">{agent.agents_count} agents</span>
                  <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded capitalize">{agent.complexity}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Parameters Control */}
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Usage Parameters</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Queries per User/Month: {params.queries_per_user_per_month}
              </label>
              <input
                type="range"
                min="100"
                max="5000"
                step="100"
                value={params.queries_per_user_per_month}
                onChange={(e) => handleParamChange('queries_per_user_per_month', parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Infrastructure Scale: {params.infrastructure_scale}x
              </label>
              <input
                type="range"
                min="0.5"
                max="3"
                step="0.1"
                value={params.infrastructure_scale}
                onChange={(e) => handleParamChange('infrastructure_scale', parseFloat(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cache Hit Rate: {(params.cache_hit_rate * 100).toFixed(0)}%
              </label>
              <input
                type="range"
                min="0"
                max="0.95"
                step="0.05"
                value={params.cache_hit_rate}
                onChange={(e) => handleParamChange('cache_hit_rate', parseFloat(e.target.value))}
                className="w-full"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="caching"
                checked={params.use_prompt_caching}
                onChange={(e) => handleParamChange('use_prompt_caching', e.target.checked)}
                className="mr-2"
              />
              <label htmlFor="caching" className="text-sm font-medium text-gray-700">
                Use Prompt Caching (90% discount)
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="reserved"
                checked={params.use_reserved_instances}
                onChange={(e) => handleParamChange('use_reserved_instances', e.target.checked)}
                className="mr-2"
              />
              <label htmlFor="reserved" className="text-sm font-medium text-gray-700">
                Use Reserved Instances (40% off)
              </label>
            </div>
          </div>

          {/* LLM Mix */}
          <div className="mt-6">
            <h3 className="font-semibold text-gray-800 mb-3">LLM Model Mix</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(params.llm_mix).map(([model, percent]) => (
                <div key={model}>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {model}: {percent.toFixed(0)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={percent}
                    onChange={(e) => handleLLMMixChange(model, e.target.value)}
                    className="w-full"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200">
          <div className="border-b border-gray-200">
            <div className="flex overflow-x-auto">
              {['overview', 'infrastructure', 'llm', 'data-sources', 'monitoring'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-6 py-4 font-medium transition-colors whitespace-nowrap ${
                    activeTab === tab
                      ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  {tab.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                </button>
              ))}
            </div>
          </div>

          <div className="p-6">
            {loading && (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="text-gray-600 mt-4">Calculating costs...</p>
              </div>
            )}

            {!loading && activeTab === 'overview' && <OverviewTab />}
            {!loading && activeTab === 'infrastructure' && <InfrastructureTab />}
            {!loading && activeTab === 'llm' && <LLMTab />}
            {!loading && activeTab === 'data-sources' && <DataSourcesTab />}
            {!loading && activeTab === 'monitoring' && <MonitoringTab />}
          </div>
        </div>

        {/* Footer Note */}
        <div className="mt-6 text-center text-sm text-gray-500">
          <p>💡 All prices in AUD for Azure Australia East (Sydney) region</p>
          <p>Pricing updated: January 2025 | Includes Reserved Instance discounts & Prompt Caching savings</p>
        </div>
      </div>
    </div>
  );
};

export default CostCalculator;
