import React, { useState, useCallback } from 'react';
import { RefreshCw, Play, Upload, GitBranch, Zap, Cpu, Settings, DollarSign } from 'lucide-react';
import axios from 'axios';
import CostCalculator from './CostCalculator';

// === DATA MOCKING & CONSTANTS ===
const AGENT_MODELS = ['GPT-4 (Simulated)', 'Claude-3 (Simulated)', 'Gemini (Simulated)', 'Custom LLM (Simulated)'];
const AUTOMATION_FRAMEWORKS = ['Playwright', 'Selenium', 'Cypress'];
const TEST_TYPES = ['Functional Testing', 'Regression Testing', 'Performance Testing', 'Security/Pen Testing'];
const REQUIREMENTS_SOURCES = ['Upload Document', 'Connect to Confluence (Simulated)', 'Connect to SharePoint (Simulated)'];

const INITIAL_STATE = {
  appName: 'E-Commerce Checkout Service',
  appType: 'Web App',
  testUrl: 'https://demo.app/checkout',
  reqSource: 'Upload Document',
  testTypes: new Set(['Functional Testing', 'Regression Testing']),
  scope: 'Test user login, shopping cart additions, and payment submission.',
  reasoningModel: AGENT_MODELS[0],
  generationModel: AGENT_MODELS[1],
  automationFramework: AUTOMATION_FRAMEWORKS[0],
  status: 'IDLE', // IDLE, RUNNING, COMPLETE, FAILED
  workflow: [
    { name: 'Perception Agent', icon: Cpu, status: 'PENDING', log: 'Awaiting context ingestion...' },
    { name: 'Planner Agent (Reasoning)', icon: GitBranch, status: 'PENDING', log: 'Awaiting structured test plan generation...' },
    { name: 'Generator Agent', icon: Play, status: 'PENDING', log: 'Awaiting executable script writing...' },
    { name: 'Execution Agent', icon: Zap, status: 'PENDING', log: 'Awaiting environment setup and test run...' },
    { name: 'Healer Agent', icon: RefreshCw, status: 'PENDING', log: 'Awaiting results analysis and feedback loop...' },
  ],
  logHistory: [],
  finalReport: null,
};

// === COMPONENT: AgentControlCenter ===
const App = () => {
  const [currentView, setCurrentView] = useState('qa-agent'); // 'qa-agent' or 'cost-calculator'
  const [state, setState] = useState(INITIAL_STATE);
  const { status, workflow, logHistory, finalReport } = state;

  // Utility to update workflow status and append to log history
  const updateWorkflow = useCallback((agentIndex, newStatus, message) => {
    setState(prevState => {
      const newWorkflow = [...prevState.workflow];
      newWorkflow[agentIndex] = { ...newWorkflow[agentIndex], status: newStatus, log: message };

      return {
        ...prevState,
        workflow: newWorkflow,
        logHistory: [...prevState.logHistory, { agent: newWorkflow[agentIndex].name, message, type: newStatus.toLowerCase() }],
      };
    });
  }, []);

  const runAgent = useCallback(async (agentIndex, apiEndpoint, requestData) => {
    const agent = workflow[agentIndex];
    updateWorkflow(agentIndex, 'RUNNING', `${agent.name} started at ${new Date().toLocaleTimeString()}.`);

    try {
      const response = await axios.post(apiEndpoint, requestData);
      const result = response.data;

      if (result.status === 'success') {
        updateWorkflow(agentIndex, 'COMPLETE', `${agent.name} complete. ${result.message}`);
        return { success: true, data: result.data };
      } else {
        updateWorkflow(agentIndex, 'FAILED', `${agent.name} failed: ${result.message}`);
        setState(prev => ({ ...prev, status: 'FAILED' }));
        return { success: false };
      }
    } catch (error) {
      updateWorkflow(agentIndex, 'FAILED', `${agent.name} error: ${error.message}`);
      setState(prev => ({ ...prev, status: 'FAILED' }));
      return { success: false };
    }
  }, [workflow, updateWorkflow]);

  // === MAIN WORKFLOW ===
  const startWorkflow = async () => {
    if (status === 'RUNNING') return;
    setState({
      ...INITIAL_STATE,
      status: 'RUNNING',
      appName: state.appName,
      appType: state.appType,
      testUrl: state.testUrl,
      reqSource: state.reqSource,
      testTypes: state.testTypes,
      scope: state.scope,
      reasoningModel: state.reasoningModel,
      generationModel: state.generationModel,
      automationFramework: state.automationFramework
    });

    // 1. Perception Agent (Simulated locally - no API call needed)
    updateWorkflow(0, 'RUNNING', 'Perception Agent: Analyzing requirements...');
    await new Promise(resolve => setTimeout(resolve, 1500));
    updateWorkflow(0, 'COMPLETE', 'Perception Agent: Vectorized 15 docs, extracted 3 tables. Ready for planning.');

    // 2. Planner Agent (API Call)
    const plannerResult = await runAgent(1, '/api/planner', {
      appName: state.appName,
      appType: state.appType,
      testUrl: state.testUrl,
      scope: state.scope,
      testTypes: Array.from(state.testTypes),
      reasoningModel: state.reasoningModel,
    });
    if (!plannerResult.success) return;

    // 3. Generator Agent (API Call)
    const generatorResult = await runAgent(2, '/api/generator', {
      testPlan: plannerResult.data.testPlan,
      automationFramework: state.automationFramework,
      generationModel: state.generationModel,
    });
    if (!generatorResult.success) return;

    // 4. Execution Agent (Simulated locally)
    updateWorkflow(3, 'RUNNING', 'Execution Agent: Running tests...');
    await new Promise(resolve => setTimeout(resolve, 3000));
    const executionResult = Math.random() > 0.3
      ? 'Tests PASSED: 4/5 tests passed. One failure detected due to CSS selector change.'
      : 'Tests FAILED: 5/5 tests failed. Environment issue suspected.';
    updateWorkflow(3, 'COMPLETE', `Execution Agent: ${executionResult}`);

    // 5. Healer Agent (API Call)
    const healerResult = await runAgent(4, '/api/healer', {
      testScript: generatorResult.data.testScript,
      executionResult: executionResult,
      automationFramework: state.automationFramework,
    });

    if (healerResult.success) {
      setState(prev => ({
        ...prev,
        status: 'COMPLETE',
        finalReport: `Workflow Finished. ${healerResult.data.summary}`
      }));
    }
  };

  const handleConfigChange = (field, value) => {
    setState(prev => ({ ...prev, [field]: value }));
  };

  const handleTestTypeChange = (type) => {
    setState(prev => {
      const newTypes = new Set(prev.testTypes);
      if (newTypes.has(type)) {
        newTypes.delete(type);
      } else {
        newTypes.add(type);
      }
      return { ...prev, testTypes: newTypes };
    });
  };

  const isRunning = status === 'RUNNING';

  const AgentPill = ({ agent }) => (
    <div className={`p-3 rounded-xl shadow-md transition-all duration-300 ${
      agent.status === 'COMPLETE' ? 'bg-green-100 border-green-400' :
      agent.status === 'RUNNING' ? 'bg-amber-100 border-amber-400 animate-pulse' :
      agent.status === 'FAILED' ? 'bg-red-100 border-red-400' :
      'bg-white border-gray-200'
    } border-2 flex items-center space-x-3`}>
      <agent.icon className={`w-6 h-6 ${
        agent.status === 'COMPLETE' ? 'text-green-600' :
        agent.status === 'RUNNING' ? 'text-amber-600' :
        agent.status === 'FAILED' ? 'text-red-600' :
        'text-gray-500'
      }`} />
      <div className="flex-grow">
        <h4 className="font-semibold text-gray-800">{agent.name}</h4>
        <p className={`text-xs ${agent.status === 'PENDING' ? 'text-gray-500' : 'text-gray-600'}`}>
          {agent.log}
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#FDFBF8]">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Settings className="w-6 h-6 text-amber-600" />
              <span className="text-xl font-bold text-gray-800">QA AI Agent Platform</span>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setCurrentView('qa-agent')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 ${
                  currentView === 'qa-agent'
                    ? 'bg-amber-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Cpu className="w-4 h-4" />
                <span>QA Agents</span>
              </button>
              <button
                onClick={() => setCurrentView('cost-calculator')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 ${
                  currentView === 'cost-calculator'
                    ? 'bg-amber-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <DollarSign className="w-4 h-4" />
                <span>Cost Calculator</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Conditional Content Rendering */}
      {currentView === 'cost-calculator' ? (
        <CostCalculator />
      ) : (
        <div className="p-4 sm:p-8">
          <header className="max-w-7xl mx-auto mb-8 text-center">
            <h1 className="text-4xl font-bold text-gray-800">
              Multi-Agent QA Control Center
            </h1>
            <p className="text-gray-600 mt-2">Configure, execute, and monitor the automated cognitive testing pipeline.</p>
          </header>

      <div className="max-w-7xl mx-auto grid lg:grid-cols-3 gap-8">

        {/* === COLUMN 1: CONFIGURATION === */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <h2 className="text-xl font-semibold text-gray-700 mb-4 border-b pb-2">1. Target & Scope</h2>

            {/* App Name */}
            <label className="block mb-4">
              <span className="text-sm font-medium text-gray-600">Application Name/Service</span>
              <input
                type="text"
                value={state.appName}
                onChange={(e) => handleConfigChange('appName', e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                disabled={isRunning}
              />
            </label>

            {/* App Type */}
            <label className="block mb-4">
              <span className="text-sm font-medium text-gray-600">Application Type</span>
              <select
                value={state.appType}
                onChange={(e) => handleConfigChange('appType', e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 bg-white border"
                disabled={isRunning}
              >
                {['Web App', 'Desktop App', 'Mobile App', 'API Service'].map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </label>

            {/* Test URL */}
            <label className="block mb-4">
              <span className="text-sm font-medium text-gray-600">Test URL / Endpoint</span>
              <input
                type="text"
                value={state.testUrl}
                onChange={(e) => handleConfigChange('testUrl', e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                disabled={isRunning}
              />
            </label>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <h2 className="text-xl font-semibold text-gray-700 mb-4 border-b pb-2">2. Context & Requirements</h2>

            {/* Requirements Source */}
            <label className="block mb-4">
              <span className="text-sm font-medium text-gray-600">BRD/Requirements Source (Perception Agent Input)</span>
              <select
                value={state.reqSource}
                onChange={(e) => handleConfigChange('reqSource', e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 bg-white border"
                disabled={isRunning}
              >
                {REQUIREMENTS_SOURCES.map(source => (
                  <option key={source} value={source}>{source}</option>
                ))}
              </select>
            </label>

            {state.reqSource === 'Upload Document' && (
              <div className="mb-4 p-4 border-2 border-dashed rounded-lg text-center text-gray-500">
                <Upload className="w-5 h-5 mx-auto mb-1" />
                <p className="text-sm">Upload BRD/User Stories (Simulated)</p>
              </div>
            )}

            {/* Scope */}
            <label className="block mb-4">
              <span className="text-sm font-medium text-gray-600">Functionality Scope (Commit Diff/Feature Focus)</span>
              <textarea
                value={state.scope}
                onChange={(e) => handleConfigChange('scope', e.target.value)}
                rows="3"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                disabled={isRunning}
              />
            </label>

            {/* Test Types */}
            <div className="mb-4">
              <span className="text-sm font-medium text-gray-600 block mb-2">Test Types (Reasoning Agent Goal)</span>
              <div className="flex flex-wrap gap-2">
                {TEST_TYPES.map(type => (
                  <button
                    key={type}
                    onClick={() => handleTestTypeChange(type)}
                    className={`px-3 py-1 text-sm rounded-full transition-colors duration-200 ${
                      state.testTypes.has(type) ? 'bg-amber-600 text-white shadow-md' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                    disabled={isRunning}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* === COLUMN 2: WORKFLOW STATUS === */}
        <div className="lg:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 mb-6">
            <h2 className="text-xl font-semibold text-gray-700 mb-4 border-b pb-2">3. Cognitive Pipeline Status</h2>
            <div className="flex justify-between items-center mb-6">
              <h3 className={`text-2xl font-bold ${
                status === 'RUNNING' ? 'text-amber-600' :
                status === 'COMPLETE' ? 'text-green-600' :
                status === 'FAILED' ? 'text-red-600' : 'text-gray-800'
              }`}>
                {status === 'IDLE' ? 'Ready to Execute' : status}
              </h3>
              <button
                onClick={startWorkflow}
                disabled={isRunning}
                className={`flex items-center px-6 py-3 rounded-full font-bold shadow-lg transition-all duration-300 ${
                  isRunning ? 'bg-gray-400 cursor-not-allowed' : 'bg-amber-600 hover:bg-amber-700 text-white transform hover:scale-[1.02]'
                }`}
              >
                {isRunning ? (
                  <>
                    <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5 mr-2" />
                    Start Agent Run
                  </>
                )}
              </button>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {workflow.map((agent, index) => (
                <AgentPill key={index} agent={agent} />
              ))}
            </div>

            {finalReport && (
              <div className="mt-6 p-4 bg-green-50 text-green-800 border border-green-300 rounded-lg">
                <p className="font-bold">Final Report:</p>
                <p className="mt-1">{finalReport}</p>
              </div>
            )}
          </div>

          {/* LOG HISTORY */}
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 h-96 flex flex-col">
            <h2 className="text-xl font-semibold text-gray-700 mb-4 border-b pb-2">4. Event Log (Message Broker Trace)</h2>
            <div className="overflow-y-auto flex-grow text-sm space-y-1 bg-gray-50 p-3 rounded-lg border">
              {logHistory.length === 0 ? (
                <p className="text-gray-500 italic">Logs will appear here when the workflow starts, simulating Kafka events.</p>
              ) : (
                logHistory.map((log, index) => (
                  <div key={index} className={`font-mono text-xs ${
                    log.type === 'complete' ? 'text-green-700' :
                    log.type === 'running' ? 'text-amber-700' :
                    log.type === 'failed' ? 'text-red-700' : 'text-gray-700'
                  }`}>
                    <span className="font-bold mr-2">{log.agent}:</span> {log.message}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* === COLUMN 3: AGENT CONFIGURATION === */}
        <div className="lg:col-span-3">
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <h2 className="text-xl font-semibold text-gray-700 mb-4 border-b pb-2">5. Agent Configuration & Stack Selection</h2>
            <div className="grid md:grid-cols-3 gap-6">

              {/* Planner/Reasoning Agent Config */}
              <div className="p-4 border rounded-lg">
                <h3 className="font-semibold text-lg text-gray-800">Planner Agent (Reasoning)</h3>
                <p className="text-xs text-gray-500 mb-3">Core LLM for planning and risk analysis (LangChain/LangGraph).</p>
                <label className="block mb-3">
                  <span className="text-sm font-medium text-gray-600">LLM Model</span>
                  <select
                    value={state.reasoningModel}
                    onChange={(e) => handleConfigChange('reasoningModel', e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 bg-white border"
                    disabled={isRunning}
                  >
                    {AGENT_MODELS.map(model => (
                      <option key={model} value={model}>{model}</option>
                    ))}
                  </select>
                </label>
              </div>

              {/* Generator Agent Config */}
              <div className="p-4 border rounded-lg">
                <h3 className="font-semibold text-lg text-gray-800">Generator Agent (Code Writer)</h3>
                <p className="text-xs text-gray-500 mb-3">LLM for translating plans into code scripts.</p>
                <label className="block mb-3">
                  <span className="text-sm font-medium text-gray-600">LLM Model</span>
                  <select
                    value={state.generationModel}
                    onChange={(e) => handleConfigChange('generationModel', e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 bg-white border"
                    disabled={isRunning}
                  >
                    {AGENT_MODELS.map(model => (
                      <option key={model} value={model}>{model}</option>
                    ))}
                  </select>
                </label>
              </div>

              {/* Execution Agent Config */}
              <div className="p-4 border rounded-lg">
                <h3 className="font-semibold text-lg text-gray-800">Execution Agent (Runner)</h3>
                <p className="text-xs text-gray-500 mb-3">Select the underlying test automation framework.</p>
                <label className="block mb-3">
                  <span className="text-sm font-medium text-gray-600">Framework (MCP Server)</span>
                  <select
                    value={state.automationFramework}
                    onChange={(e) => handleConfigChange('automationFramework', e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 bg-white border"
                    disabled={isRunning}
                  >
                    {AUTOMATION_FRAMEWORKS.map(fw => (
                      <option key={fw} value={fw}>{fw}</option>
                    ))}
                  </select>
                </label>
              </div>

            </div>
          </div>
        </div>

      </div>
        </div>
      )}
    </div>
  );
};

export default App;
