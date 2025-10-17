import React, { useState, useEffect } from 'react';
import { Briefcase, Settings, Zap, DollarSign, Database, Cpu, Brain, Users, TrendingUp, Target, Shield } from 'lucide-react';

// OPTIMIZED SCIP AGENT CONFIGURATION (Based on Tech_Design_Sales_Coach_AI_Agent_OPTIMIZED.md)
const SCIP_AGENTS = {
  supervisor: {
    id: 'supervisor',
    name: 'Supervisor Agent',
    icon: Settings,
    description: 'Master orchestrator using ImpactWon framework',
    category: 'Orchestration',
    defaultConfig: {
      llm: 'gpt-4o',
      temperature: 0.7,
      max_tokens: 4000,
      memory_type: 'redis',
      memory_window: 10,
      tools: ['all_mcp_tools'],
      usage_probability: 100, // Always used
      avg_tokens_per_request: 3000,
      requests_per_4cs_calculation: 1
    },
    llmOptions: ['gpt-4o', 'claude-3.5-opus', 'gpt-4-turbo'],
    toolsOptions: ['research_tool', 'content_generation_tool', 'competitive_intel_tool', 'fog_analysis_tool', 'engagement_excellence_tool', 'impact_theme_generator_tool'],
    memoryOptions: ['redis', 'cosmos-db', 'in-memory']
  },
  power_plan: {
    id: 'power_plan',
    name: 'Power Plan Agent (4Cs)',
    icon: Target,
    description: 'THE CRITICAL AGENT - Calculate Right to Win via 4Cs scoring',
    category: 'Core',
    defaultConfig: {
      llm: 'gpt-4o',
      temperature: 0.3,
      max_tokens: 6000,
      memory_type: 'cosmos-db',
      memory_window: 20,
      tools: ['research_tool', 'fog_analysis_tool', 'impact_theme_generator_tool'],
      usage_probability: 100, // Always used for 4Cs
      avg_tokens_per_request: 8000,
      requests_per_4cs_calculation: 3
    },
    llmOptions: ['gpt-4o', 'claude-3.5-opus', 'gpt-4-turbo'],
    toolsOptions: ['research_tool', 'fog_analysis_tool', 'impact_theme_generator_tool', 'find_money_validator_tool'],
    memoryOptions: ['cosmos-db', 'azure-sql', 'redis']
  },
  strategic_planning: {
    id: 'strategic_planning',
    name: 'Strategic Planning Agent',
    icon: Brain,
    description: 'CEO Sales Plan + Attainment + Pursuit planning (consolidated)',
    category: 'Core',
    defaultConfig: {
      llm: 'claude-3.5-sonnet',
      temperature: 0.7,
      max_tokens: 8000,
      memory_type: 'cosmos-db',
      memory_window: 15,
      tools: ['research_tool', 'content_generation_tool', 'engagement_excellence_tool'],
      usage_probability: 75, // Used for strategic planning requests
      avg_tokens_per_request: 10000,
      requests_per_4cs_calculation: 2
    },
    llmOptions: ['claude-3.5-sonnet', 'gpt-4o', 'claude-3.5-opus'],
    toolsOptions: ['research_tool', 'content_generation_tool', 'competitive_intel_tool', 'engagement_excellence_tool'],
    memoryOptions: ['cosmos-db', 'azure-sql']
  },
  client_intelligence: {
    id: 'client_intelligence',
    name: 'Client Intelligence Agent',
    icon: Users,
    description: 'Client profiling + BBB stakeholder mapping + Right Clients (consolidated)',
    category: 'Core',
    defaultConfig: {
      llm: 'gpt-4o',
      temperature: 0.5,
      max_tokens: 6000,
      memory_type: 'neo4j',
      memory_window: 25,
      tools: ['research_tool', 'competitive_intel_tool', 'fog_analysis_tool'],
      usage_probability: 90, // High probability for client-related queries
      avg_tokens_per_request: 7000,
      requests_per_4cs_calculation: 2
    },
    llmOptions: ['gpt-4o', 'claude-3.5-sonnet', 'gpt-4-turbo'],
    toolsOptions: ['research_tool', 'competitive_intel_tool', 'fog_analysis_tool'],
    memoryOptions: ['neo4j', 'cosmos-db', 'azure-sql']
  },
  deal_assessment: {
    id: 'deal_assessment',
    name: 'Deal Assessment Agent',
    icon: TrendingUp,
    description: 'Deal qualification + budget validation + risk assessment (consolidated)',
    category: 'Core',
    defaultConfig: {
      llm: 'gpt-4o',
      temperature: 0.4,
      max_tokens: 5000,
      memory_type: 'cosmos-db',
      memory_window: 15,
      tools: ['research_tool', 'competitive_intel_tool', 'find_money_validator_tool'],
      usage_probability: 85, // Used for deal qualification
      avg_tokens_per_request: 6000,
      requests_per_4cs_calculation: 2
    },
    llmOptions: ['gpt-4o', 'claude-3.5-sonnet', 'gpt-4-turbo'],
    toolsOptions: ['research_tool', 'competitive_intel_tool', 'find_money_validator_tool'],
    memoryOptions: ['cosmos-db', 'azure-sql']
  },
  team_orchestration: {
    id: 'team_orchestration',
    name: 'Team Orchestration Agent',
    icon: Shield,
    description: 'Team planning + right team selection (consolidated)',
    category: 'Supporting',
    defaultConfig: {
      llm: 'gpt-4o',
      temperature: 0.6,
      max_tokens: 4000,
      memory_type: 'cosmos-db',
      memory_window: 10,
      tools: ['research_tool', 'license_to_sell_tool'],
      usage_probability: 60, // Used for team-related queries
      avg_tokens_per_request: 5000,
      requests_per_4cs_calculation: 1
    },
    llmOptions: ['gpt-4o', 'claude-3.5-sonnet', 'gpt-4-turbo'],
    toolsOptions: ['research_tool', 'license_to_sell_tool'],
    memoryOptions: ['cosmos-db', 'azure-sql']
  },
  realtime_coach: {
    id: 'realtime_coach',
    name: 'Real-time Coach Agent',
    icon: Zap,
    description: 'OPTIONAL: Live meeting coaching with transcription',
    category: 'Optional',
    defaultConfig: {
      llm: 'gpt-4o',
      temperature: 0.5,
      max_tokens: 3000,
      memory_type: 'redis',
      memory_window: 50,
      tools: ['speech_to_text', 'fog_analysis_tool'],
      usage_probability: 30, // Optional feature
      avg_tokens_per_request: 4000,
      requests_per_4cs_calculation: 0
    },
    llmOptions: ['gpt-4o', 'gpt-4-turbo'],
    toolsOptions: ['speech_to_text', 'fog_analysis_tool'],
    memoryOptions: ['redis', 'in-memory']
  }
};

const SalesCoach = () => {
  const [activeAgent, setActiveAgent] = useState('supervisor');
  const [agentConfigs, setAgentConfigs] = useState(() => {
    // Initialize with default configs
    const configs = {};
    Object.keys(SCIP_AGENTS).forEach(agentId => {
      configs[agentId] = { ...SCIP_AGENTS[agentId].defaultConfig };
    });
    return configs;
  });

  // Global parameters
  const [globalParams, setGlobalParams] = useState({
    num_users: 100,
    assessments_per_user_per_month: 40, // 10 deals x 4 assessments each
    avg_deal_size: 500000 // $500K average deal size
  });

  const currentAgent = SCIP_AGENTS[activeAgent];
  const currentConfig = agentConfigs[activeAgent];

  const handleConfigChange = (field, value) => {
    setAgentConfigs(prev => ({
      ...prev,
      [activeAgent]: {
        ...prev[activeAgent],
        [field]: value
      }
    }));
  };

  const handleToolToggle = (tool) => {
    const currentTools = currentConfig.tools || [];
    const newTools = currentTools.includes(tool)
      ? currentTools.filter(t => t !== tool)
      : [...currentTools, tool];
    handleConfigChange('tools', newTools);
  };

  const handleGlobalParamChange = (field, value) => {
    setGlobalParams(prev => ({ ...prev, [field]: value }));
  };

  // Calculate estimated monthly cost based on agent configuration
  const calculateAgentCost = () => {
    const config = agentConfigs[activeAgent];
    const totalRequests = globalParams.num_users * globalParams.assessments_per_user_per_month;
    const agentRequests = (totalRequests * config.usage_probability / 100) * config.requests_per_4cs_calculation;

    // LLM pricing (simplified - should match backend)
    const llmPricing = {
      'gpt-4o': { input: 2.50, output: 10.00 },
      'gpt-4-turbo': { input: 10.00, output: 30.00 },
      'claude-3.5-sonnet': { input: 3.00, output: 15.00 },
      'claude-3.5-opus': { input: 15.00, output: 75.00 }
    };

    const pricing = llmPricing[config.llm] || llmPricing['gpt-4o'];
    const inputTokens = agentRequests * config.avg_tokens_per_request * 0.7; // 70% input
    const outputTokens = agentRequests * config.avg_tokens_per_request * 0.3; // 30% output

    const monthlyCostUSD = (inputTokens / 1000000 * pricing.input) + (outputTokens / 1000000 * pricing.output);
    const monthlyCostAUD = monthlyCostUSD / 0.65; // USD to AUD

    return {
      monthlyAUD: monthlyCostAUD,
      annualAUD: monthlyCostAUD * 12,
      requests: agentRequests
    };
  };

  const agentCost = calculateAgentCost();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-2">
            <Briefcase className="w-10 h-10 text-indigo-600" />
            <h1 className="text-4xl font-bold text-gray-900">Sales Coach in the Pocket</h1>
          </div>
          <p className="text-gray-600">
            Configure the 6-7 optimized AI agents for ImpactWon 4Cs assessment • Lean Agents + Rich Tools Architecture
          </p>
        </div>

        {/* Global Parameters */}
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <Settings className="w-5 h-5 mr-2 text-indigo-600" />
            Global Usage Parameters
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Users: {globalParams.num_users}
              </label>
              <input
                type="range"
                min="10"
                max="500"
                step="10"
                value={globalParams.num_users}
                onChange={(e) => handleGlobalParamChange('num_users', parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Assessments per User/Month: {globalParams.assessments_per_user_per_month}
              </label>
              <input
                type="range"
                min="10"
                max="100"
                step="5"
                value={globalParams.assessments_per_user_per_month}
                onChange={(e) => handleGlobalParamChange('assessments_per_user_per_month', parseInt(e.target.value))}
                className="w-full"
              />
              <p className="text-xs text-gray-500 mt-1">Typical: 10 deals × 4 assessments = 40/month</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Avg Deal Size: ${(globalParams.avg_deal_size / 1000).toFixed(0)}K
              </label>
              <input
                type="range"
                min="100000"
                max="5000000"
                step="100000"
                value={globalParams.avg_deal_size}
                onChange={(e) => handleGlobalParamChange('avg_deal_size', parseInt(e.target.value))}
                className="w-full"
              />
            </div>
          </div>
        </div>

        {/* Agent Tabs */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 mb-6">
          <div className="border-b border-gray-200 overflow-x-auto">
            <div className="flex">
              {Object.entries(SCIP_AGENTS).map(([agentId, agent]) => {
                const Icon = agent.icon;
                return (
                  <button
                    key={agentId}
                    onClick={() => setActiveAgent(agentId)}
                    className={`px-6 py-4 font-medium transition-colors whitespace-nowrap flex items-center space-x-2 ${
                      activeAgent === agentId
                        ? 'text-indigo-600 border-b-2 border-indigo-600 bg-indigo-50'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{agent.name}</span>
                    {agent.category === 'Core' && (
                      <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 text-xs rounded-full">Core</span>
                    )}
                    {agent.category === 'Optional' && (
                      <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">Optional</span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Agent Configuration Panel */}
          <div className="p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{currentAgent.name}</h2>
              <p className="text-gray-600">{currentAgent.description}</p>
              <div className="mt-2">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  currentAgent.category === 'Orchestration' ? 'bg-purple-100 text-purple-700' :
                  currentAgent.category === 'Core' ? 'bg-indigo-100 text-indigo-700' :
                  currentAgent.category === 'Supporting' ? 'bg-blue-100 text-blue-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {currentAgent.category}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Column: LLM & Memory Config */}
              <div className="space-y-6">
                {/* LLM Selection */}
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-5 border border-purple-200">
                  <label className="block text-sm font-semibold text-purple-900 mb-3 flex items-center">
                    <Brain className="w-4 h-4 mr-2" />
                    LLM Model
                  </label>
                  <select
                    value={currentConfig.llm}
                    onChange={(e) => handleConfigChange('llm', e.target.value)}
                    className="w-full rounded-md border-purple-300 shadow-sm p-3 bg-white"
                  >
                    {currentAgent.llmOptions.map(model => (
                      <option key={model} value={model}>{model}</option>
                    ))}
                  </select>
                  <div className="mt-3 grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-medium text-purple-700 mb-1">Temperature</label>
                      <input
                        type="number"
                        min="0"
                        max="1"
                        step="0.1"
                        value={currentConfig.temperature}
                        onChange={(e) => handleConfigChange('temperature', parseFloat(e.target.value))}
                        className="w-full rounded-md border-purple-300 p-2 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-purple-700 mb-1">Max Tokens</label>
                      <input
                        type="number"
                        min="1000"
                        max="32000"
                        step="1000"
                        value={currentConfig.max_tokens}
                        onChange={(e) => handleConfigChange('max_tokens', parseInt(e.target.value))}
                        className="w-full rounded-md border-purple-300 p-2 text-sm"
                      />
                    </div>
                  </div>
                </div>

                {/* Memory Configuration */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-5 border border-blue-200">
                  <label className="block text-sm font-semibold text-blue-900 mb-3 flex items-center">
                    <Database className="w-4 h-4 mr-2" />
                    Memory System
                  </label>
                  <select
                    value={currentConfig.memory_type}
                    onChange={(e) => handleConfigChange('memory_type', e.target.value)}
                    className="w-full rounded-md border-blue-300 shadow-sm p-3 bg-white mb-3"
                  >
                    {currentAgent.memoryOptions.map(memory => (
                      <option key={memory} value={memory}>{memory}</option>
                    ))}
                  </select>
                  <div>
                    <label className="block text-xs font-medium text-blue-700 mb-1">
                      Memory Window: {currentConfig.memory_window} conversations
                    </label>
                    <input
                      type="range"
                      min="5"
                      max="50"
                      step="5"
                      value={currentConfig.memory_window}
                      onChange={(e) => handleConfigChange('memory_window', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>
                </div>

                {/* Usage Parameters */}
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-5 border border-green-200">
                  <label className="block text-sm font-semibold text-green-900 mb-3 flex items-center">
                    <Cpu className="w-4 h-4 mr-2" />
                    Usage Parameters
                  </label>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs font-medium text-green-700 mb-1">
                        Usage Probability: {currentConfig.usage_probability}%
                      </label>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        step="5"
                        value={currentConfig.usage_probability}
                        onChange={(e) => handleConfigChange('usage_probability', parseInt(e.target.value))}
                        className="w-full"
                      />
                      <p className="text-xs text-green-600 mt-1">
                        Probability this agent is invoked per 4Cs calculation
                      </p>
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-green-700 mb-1">Avg Tokens/Request</label>
                      <input
                        type="number"
                        min="1000"
                        max="20000"
                        step="500"
                        value={currentConfig.avg_tokens_per_request}
                        onChange={(e) => handleConfigChange('avg_tokens_per_request', parseInt(e.target.value))}
                        className="w-full rounded-md border-green-300 p-2 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-green-700 mb-1">Requests per 4Cs Calculation</label>
                      <input
                        type="number"
                        min="0"
                        max="10"
                        step="1"
                        value={currentConfig.requests_per_4cs_calculation}
                        onChange={(e) => handleConfigChange('requests_per_4cs_calculation', parseInt(e.target.value))}
                        className="w-full rounded-md border-green-300 p-2 text-sm"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column: Tools & Cost */}
              <div className="space-y-6">
                {/* MCP Tools */}
                <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg p-5 border border-amber-200">
                  <label className="block text-sm font-semibold text-amber-900 mb-3 flex items-center">
                    <Zap className="w-4 h-4 mr-2" />
                    MCP Tools & Functions
                  </label>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {currentAgent.toolsOptions.map(tool => (
                      <label key={tool} className="flex items-center space-x-2 cursor-pointer hover:bg-amber-50 p-2 rounded">
                        <input
                          type="checkbox"
                          checked={(currentConfig.tools || []).includes(tool)}
                          onChange={() => handleToolToggle(tool)}
                          className="rounded border-amber-300"
                        />
                        <span className="text-sm text-gray-700">{tool}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Cost Estimation */}
                <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-lg p-5 border border-indigo-200">
                  <h3 className="text-sm font-semibold text-indigo-900 mb-3 flex items-center">
                    <DollarSign className="w-4 h-4 mr-2" />
                    Estimated Cost (This Agent Only)
                  </h3>
                  <div className="space-y-3">
                    <div className="bg-white rounded-lg p-4 border border-indigo-300">
                      <div className="text-xs text-indigo-600 font-medium mb-1">Monthly Cost</div>
                      <div className="text-2xl font-bold text-indigo-900">
                        ${agentCost.monthlyAUD.toFixed(0)} AUD
                      </div>
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-indigo-300">
                      <div className="text-xs text-indigo-600 font-medium mb-1">Annual Cost</div>
                      <div className="text-2xl font-bold text-indigo-900">
                        ${agentCost.annualAUD.toFixed(0)} AUD
                      </div>
                    </div>
                    <div className="bg-white rounded-lg p-3 border border-indigo-200">
                      <div className="text-xs text-gray-600">Estimated Requests/Month</div>
                      <div className="text-lg font-semibold text-gray-900">
                        {agentCost.requests.toFixed(0)}
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 text-xs text-indigo-700 bg-white p-3 rounded border border-indigo-200">
                    <strong>Note:</strong> This is the cost for {currentAgent.name} only.
                    See the Cost Calculator tab for complete system costs including infrastructure, tools, and all agents.
                  </div>
                </div>

                {/* Info Box */}
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <h4 className="text-sm font-semibold text-blue-900 mb-2">Configuration Tips</h4>
                  <ul className="text-xs text-blue-800 space-y-1">
                    <li>• <strong>Temperature:</strong> Lower (0.1-0.4) for factual tasks, higher (0.6-0.9) for creative tasks</li>
                    <li>• <strong>Usage Probability:</strong> 100% for critical agents, lower for optional features</li>
                    <li>• <strong>Memory Window:</strong> Larger for context-heavy agents (Power Plan, Client Intelligence)</li>
                    <li>• <strong>Tools:</strong> Select only tools actually used by this agent to reduce latency</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Info Footer */}
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-3">About the Optimized SCIP Architecture</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
            <div>
              <h4 className="font-semibold text-gray-800 mb-2">Lean Agents + Rich Tools</h4>
              <p>
                Reduced from 21 agents to 6-7 optimized agents following AI best practices.
                Complex reasoning stays in agents; data retrieval and templates moved to MCP tools.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-800 mb-2">Cost Savings</h4>
              <p>
                70% reduction in agents = 57% cost savings ($15K → $6.5K/month) with 50-60% faster response times.
                Each agent configuration directly impacts the Cost Calculator.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SalesCoach;
